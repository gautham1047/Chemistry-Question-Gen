# Compound Class Refactor Notes

Persistent working doc for the compound-class rewrite. Survives /compact. Update in place as work progresses.

**Baseline test**: `python test/test_all_problems.py` — target is **≥ 68/73 passing**. Remaining flaky problems (13, 54, 62, 72, 73) are pre-existing and not in compound-construction paths; don't chase them as part of this refactor.

---

## Done

### 1. Canonical formula parser — [src/utils/parsing.py](src/utils/parsing.py)

New `parse_formula(s) -> (atoms, charge)`. Single entry point for turning any string into atoms + signed int charge. Accepts:

- `"H2O"`, `"Cu(NO3)2"` — neutral
- `"OH-"`, `"Na+"` — trailing +/− (implicit 1)
- `"SO4^2-"`, `"Fe^3+"` — explicit multi-charge
- `"H_+1"`, `"OH_-1"` — legacy underscore form (kept for back-compat with reaction.py/solution.py)
- `"e-"` — returns `([], -1)`

Delegates atom-parsing to the existing `atomsInCompound` (which already handles parens). `atoms` is `[[sym, count], ...]` in insertion order.

### 2. `compound.__init__` rewrite — [src/models/compound.py](src/models/compound.py)

Single normalization path. Input shapes handled **explicitly**:

1. `compound` instance → copy-construct (fixes latent bug at [reaction.py:204](src/models/reaction.py#L204) where a compound was being passed into `compound()`)
2. `"e-"` sentinel → electron
3. `None` / `"RANDOM"` → delegates to `getRandomCompound()`
4. `list` input:
   - `[symbol, count, "element"]` — the element-list form used by `reaction.py` for activity-series metals/halogens. `[1]` is a *count*, not a formula.
   - `[name, equation, type]` — the normal compound-list form from `getRandomCompound()`.
5. `str` input → `parse_formula` + strip charge suffix from `self.equation`

`self.equation` is now **always the raw formula string with charge suffix stripped** (parens preserved — earlier attempt to rebuild via `compoundToString` flattened `Cu(NO3)2` → `CuN2O6` and broke a dozen consumers).

`self.compound` is **always** `[[sym, count], ...]`. The dual flat/nested shape invariant is gone.

`self.compoundDict` is rebuilt via `_rebuild_dict()` helper — single source so `refresh()` won't drift.

The old "element upgrade" branch (`H → H2`, `Hg2 → Hg`, diatomic fixups) is kept for `type == "element"` inputs but simplified to just rewrite `self.equation` before calling `atomsInCompound`.

### 3. `__eq__` and `__hash__`

Based on `(equation, charge)`. This fixes silent correctness bugs at:
- [solution.py:98](src/models/solution.py#L98) — `self.solvent == compound("H2O")`
- [solutions.py:220](src/problems/solutions.py#L220) — `compound("NO2") in soluableProducts`

Both were previously identity comparisons, always False, so the `in`/`remove` calls were no-ops.

### 4. Bug fixes

- **`getEq`** — previously iterated over `compoundDict` keys and did `eq += i[0] + str(num)`, grabbing only the first character of multi-letter symbols (`"Cl"` → `"C"`). Now delegates to `compoundToString(self.compound)`.
- **`percentComposition`** — same `i[0]` bug. Now iterates `self.compoundDict.items()` cleanly.
- **`getMolarMass`** — dead dual-shape fallback (`self.compound[0]` as string) removed; now a single sum comprehension.

### 5. `solubility_rx` / `_dissociate` cleanup

Was building `"X_+N"` / `"X_-N"` strings to pass to `make_compound` because the old parser needed them. Extracted the dissociation logic into `_dissociate()` which returns `((cation_sym, cation_charge), (anion_sym, anion_charge))` tuples and calls `make_compound(sym, charge)` directly. Fallback branches (`(NH4)X`, `NH4X`, binary) now use `self.compound` / `self.compoundDict` instead of `self.equation[6:]` slicing. Bare `except:` → `except Exception`.

### 6. `oxidation_numbers` charge round-trip cleanup

Previously did `compound("_".join([sym, str(-n)])).oxidation_numbers()` to recursively handle the polyatomic ion. Now just `compound(sym, charge=-n).oxidation_numbers()`. Same behavior, no string round-trip.

---

## TODO — ordered by priority

### ~~A. `getNameFromEq` extraction~~ ✅ Done

Moved to [src/utils/naming.py](src/utils/naming.py). Entry point `name_from_atoms(atoms, equation)` takes the already-parsed canonical form. Split into per-class helpers: `_name_element`, `_name_hydrohalic_acid`, `_name_binary_ionic`, `_name_binary_molecular`, `_name_ternary_acid`, `_name_ternary_ionic`. `SpecialCmpds` and `DIATOMICS` live as module-level dicts. `compound.getNameFromEq()` is now a 3-line delegate.

Behavior pinned in [test/test_naming_golden.py](test/test_naming_golden.py) — 44 cases covering every branch plus known fall-throughs (CO2/SO3/N2O5/P2O5, HC2H3O2, NH4Cl, H2CO3). Full problem suite: 71/73 (same two pre-existing flakies #72/#73 as baseline).

Notes:
- The binary-molecular branch still uses character-by-character parsing — preserved verbatim to match the quirky "coefficients must equal ideal charges" check. Safe to rewrite against the atoms list in a later pass, but would need to re-pin goldens.
- Bare `except:` in the ternary-ionic fallback is now `except Exception`.
- The binary-ionic TM charge heuristic still indexes `atoms[0]`/`atoms[1]` positionally — this is an existing assumption (metal first, nonmetal second) carried forward unchanged.

### ~~B. `isTernaryIonic` is broken~~ ✅ Deleted

No callers; removed alongside `hasPeroxide`.

### ~~C. `hasPeroxide` is incomplete~~ ✅ Deleted

Dead code; no callers. Removed.

### ~~D. `isElement`, `isAcid`, `isIonic` edge cases~~ ✅ Mostly done

- **`isAcid`**: rewritten to use `compoundDict` + `compoundToString` of non-H atoms. No more string-index crashes on single-letter formulas. Still restricted to *polyatomic* acids to match original semantics (hydrohalic acids like HCl are NOT detected; callers rely on that routing).
- **`isIonic`**: rewritten to iterate `compoundDict` — correctly detects `NH4Cl`, compounds where the metal isn't the first symbol, etc. Also handles NH4 as an implicit cation.
- **`isElement`**: left alone. The old definition ("equation has no uppercase after position 0") turns out to be semantically distinct from "has one unique element" — callers want "monatomic" (Na, Fe) and treat H2/P4 as molecular. Added **`hasSingleElement()`** as a new method for the len(compoundDict)==1 definition; use it when you actually want "distinct elements == 1".

### ~~E. Bare `except:` cleanup~~ ✅ Done

All bare `except:` in compound.py narrowed:
- `covalentBonds` / `getCovalentBonds` → `except Exception`
- Inner `getCovalentBonds` bond-append → `except (NameError, UnboundLocalError)` (covers the unbound `num`/`top`/`bottom` case)
- `bondEnergy` bond-order reorder fallback → `except TypeError`
- `VESPR` bond-type lookup → `except KeyError`
- `isPolar` → `except Exception`
- `oxidation_numbers` zero-index fallback → `except ValueError`
- `getAtoms` dual-shape hack deleted — canonical shape means it can't trigger; now a 2-line sum.

### ~~F. `getName` `"\ "` escape warning~~ ✅ Deleted

No data file contains `\ `. Block removed; `getName` is now a trivial accessor. SyntaxWarning gone.

### ~~G. Migrate call sites off legacy charge-string form~~ ✅ Done

- [reaction.py:711,716](src/models/reaction.py#L711): `compound("H_+1")` → `compound("H", 1)`
- [solution.py:157-158](src/models/solution.py#L157): `compound("H3O_1")`/`compound("OH_-1")` → two-arg form.
- [solution.py:214](src/models/solution.py#L214) `addCommonIon` check: the old list `["OH_-1", "H3O_1", ...]` was **always dead** because `self.equation` gets its charge suffix stripped in `__init__`. Updated the comparison to `["OH", "H3O", "H"]` and fixed the latent bug it exposed (see below).
- [solution.py:263-270](src/models/solution.py#L263) `base.__init__`: the string-concatenation building of `c_acid = base_eq[:-2] + "_+1"` etc. replaced with explicit `(eq, charge)` pairs passed to `compound(...)` directly.

**Latent bug fix** — activating `addCommonIon`'s product-index check surfaced a numerical issue: after adding a large common-ion concentration, the weak-acid/weak-base equilibrium solver can drive `prodEqConcs[0]` arbitrarily close to 0, and then `pH()` crashes in `log10`. Fixed by flooring `HConc()` to `1e-20` in the weak-acid/weak-base path ([solution.py:191](src/models/solution.py#L191)). Problem #66 "pH with Common Ion Effect" now passes again.

The underscore branch in `parse_formula` can now be removed — but wait until a clean run confirms no remaining call sites in the broader codebase (frontend? tests? scripts?).

### ~~H. `numElements` vs `len(self.compound)` confusion~~ ✅ Done

`numElements` was a misnomer — it summed atom counts, not distinct elements. Renamed to `totalAtoms()` with a docstring contrasting it against `len(self.compoundDict)`. Two call sites updated:
- [compound.py:387](src/models/compound.py#L387) `bondEnergy` monatomic check
- [solution.py:142](src/models/solution.py#L142) `particlesPerSolute`

### ~~I. Replace `"RANDOM"` magic sentinel entirely~~ ✅ Done

No external callers passed `"RANDOM"` — just dropped the branch from `__init__`. Constructor now only accepts `None` for "give me a random compound".

### ~~J. `refresh()` audit~~ ✅ Done

Several changes:

1. **`__init__` now eagerly populates `self.name`** for string-constructed compounds via `name_from_atoms(...)`. Previously it left `self.name = "Unknown"` and relied on external callers to call `refresh()`. Eager naming means `cmpd.name` is always meaningful right after construction.

2. **`refresh()` simplified** — keeps the re-parse of `self.equation` (for callers that mutate it directly) but now goes through `_rebuild_dict()` and `name_from_atoms()` instead of the legacy string-parsing code path. Docstring warns against calling it after `multCompound` (which would undo the in-place mutation by re-parsing equation).

3. **`name_from_atoms` made crash-safe** — added a top-level `try/except` that returns `equation` as fallback. The internal dispatch was moved to `_dispatch()`. Needed because eager naming in `__init__` started exercising formulas like `"H3O"` that the original monolithic method never got called on (e.g. `acidNames.get("O")` returns `None`, which the original code would have crashed on too, but only in unreachable paths). The legacy method had an equivalent safety net via its trailing bare-except.

### Bonus — legacy `_+N` branch removal from `parse_formula`

Now that TODO G is done and no call sites use `compound("H_+1")`-style strings, the underscore branch is gone from [parsing.py:parse_formula](src/utils/parsing.py#L5) and from the equation-stripping code in [compound.py](src/models/compound.py). Docstring updated. Only `^N+` / `+-` / bare forms remain.

---

## Architectural notes / decisions made

- **Kept `compoundDict` as a stored field, not a `@cached_property`.** Reason: 20+ call sites read it, and the mutation-in-place paths (`multCompound`, `refresh`) would fight a cache. Single rebuild helper is enough.
- **Kept `self.equation` as the original input string** (with charge suffix stripped). Rebuilding it from `compoundToString(self.compound)` loses parentheses and reorders elements. Consumers rely on `"(" in self.equation` and ordering.
- **Legacy `"X_+N"` form preserved in `parse_formula`.** Removing it would require migrating all call sites in one shot, which is a separate (mechanical) task. See TODO G.
- **Did not touch `getNameFromEq` yet** — it's the single largest unit of risk in the file. Needs a golden-output test harness first. See TODO A.

---

### K. Dead-method + dead-field audit ✅ Done

Full audit of compound.py methods and fields. Net: **603 → 510 lines** (−93 across two sub-passes).

**Methods deleted** (all with zero or redundant callers):
- `__str__` — Python default already delegates to `__repr__`
- `getParticles` — trivial `moles * 6.02e23` wrapper; inlined into `getAtoms`
- `hasSingleElement`, `setEq`, `isAqOrGas` — zero callers anywhere
- `gen_K_sp` — single caller (`solubility_rx`); inlined
- `refresh` — all 4 callers ([stoichiometry.py:31,73](src/problems/stoichiometry.py#L31), [thermochemistry.py:17](src/problems/thermochemistry.py#L17), [generators.py:462](src/utils/generators.py#L462)) were immediately post-construction with no intervening `self.equation` mutation, so redundant with eager naming in `__init__`. All 4 calls removed, then method deleted.
- `getNameFromEq` + `hydrate.getNameFromEq` — since `__init__` eagerly populates `self.name` via `name_from_atoms`, `getNameFromEq()` and `getName()` return identical values for base `compound`. The `eqOveride`/`cmpdOverride` params were only used by hydrate's override. Migrated all 23 callers across 6 files (`gas_laws`, `solutions`, `stoichiometry`, `thermochemistry`, `_helpers`, `test_naming_golden`) to `.getName()`. Hydrate now sets `self.name` directly in `__init__`: `self.name = self.name + " " + prefixes.get(numWater) + "hydrate"` (super already populated the anhydrous name).

**Fields deleted**:
- `self.type` — the only external read was [gas_laws.py:56](src/problems/gas_laws.py#L56) `j.type == "diatomic"`, which was **always False** because no code path ever assigned `"diatomic"` (a latent bug; intent was clearly "is H2/N2/etc"). Fixed to `j.isDiatomic()`. Internal use (`self.type == "element"` in __init__ diatomic-upgrade branch) replaced with a local `is_element` bool. `hydrate.type = "hydrate"` was write-only. All assignments removed.
- `hydrate.anhydrousCmpd` — was only read by the now-deleted `hydrate.getNameFromEq`. Gone.

**Bonus fix**: added a missing `self._rebuild_dict()` call in `hydrate.__init__` after the in-place water-atom mutation — `compoundDict` was previously stale post-construction for hydrates.

### L. `multCompound` state-consistency fix ✅ Done

`multCompound` was a landmine: it mutated `self.compound` and `self.compoundDict` but left `self.equation` and `self.name` stale. Both current callers ([chemical_quantities.py:50](src/problems/chemical_quantities.py#L50), [solutions.py:173](src/problems/solutions.py#L173)) dodged it by using `getEq()` / `getMolarMass()` / `percentComposition()` (all compound-list-driven) and never touching `.name` or `.equation` post-multiply. Reading `chemical_quantities.py:45` — `str(mult * myCompound.getMolarMass())` pre-computes the multiplied molar mass *before* the mutation — suggests the author hit the inconsistency and worked around it.

Fixed by having `multCompound` rebuild equation + name via `compoundToString` and `name_from_atoms`. Compound is now fully consistent post-call.

### M. `raiseTemp` / `heat` streamline ✅ Done

Both methods were classic phase-walk state machines drowning in if/elif branches.

**`raiseTemp`** (37 → 13 lines): rewrote as a cumulative-enthalpy function. `heat = enthalpy(T_final) - enthalpy(T_start)` where `enthalpy(T)` bakes the fusion/vaporization discontinuities into the cumulative sum at `fp`/`bp`. Side-effect: **fixes two latent bugs** in the original (missing liquid-segment contribution on solid↔gas transitions; wrong sign on liquid→gas vaporization). Problem #15 pass rate 99/100 → 100/100.

**`heat`** (~75 → ~40 lines): replaced the mirrored heating/cooling if-ladders with two short segment-walk loops driven by a `transitions` list `[(phase, boundary, phase_change_joules, next_phase), ...]`. Preserves exact edge-case semantics (heating uses `<=` on phase-change budget check, cooling uses `<`; zero-solid-SH falls back to fp).

### N. reaction.py API cleanup + problem migration ✅ Done

Dead code removed: `skeletonStr`, `enthalpyFromThermData`, `gibbsFromThermData`, `entropyFromThermData`, `eqConcsFromMissing`, plus a dead pre-try block in `enthalpyFromBonds`.

**Memoization**: `SkeletonEquation()` and `balanceEq()` now cache on `self._skele_cache` / `self._coeffs_cache` (implementations moved to `_computeSkeleton` / `_computeBalance`). These are the two hot paths that previously recomputed on every call site.

**New canonical API**: `rx.reactants()` and `rx.products()` both return `[[compound, coeff], ...]` pairs. `allCompounds()` returns a flat list. `formatRxList()` is now a legacy shim (still used internally by `reaction.py` + `solution.py`; kept for now).

**Problem-file migration**: all external `rx.SkeletonEquation()[0]` / `[1]` and `rx.formatRxList()` usage is gone. Migrated files: `stoichiometry.py`, `chemical_reactions.py`, `solutions.py`, `gas_laws.py`, `thermochemistry.py`, `rates.py`. Special-type qualifier text (old `len(separatedCmpds) == 3` check) now reads `rx.typeRx == "special"` + `rx.misc[2]`. Tests held at 70/73 (same three pre-existing flakies).

### Audit summary — what's left in compound.py is all live

Every remaining method has confirmed callers:
- `raiseTemp` → `thermochemistry.py:43`
- `heat` → `thermochemistry.py:206`
- `isSoluable` → `chemical_reactions.py`, `generators.py`, `solution.py`, `reaction.py`
- `bondOrder`, `sigmaBonds`, `piBonds`, `VESPR`, `bondEnergy`, `covalentBonds` → `periodic_trends_and_bonds.py`, `reaction.py`, `generators.py`
- `oxidation_numbers`, `solubility_rx` → redox + solubility problem paths
- etc.

---

## How to resume

Compound.py is audited end-to-end (TODOs A–K done). Next useful moves:

1. **Investigate the three pre-existing flakies** — `#62 Calculating Equilibrium Concentrations from Initial`, `#72 Electroplating`, `#73 Nuclear Decay`. Occasionally `#15 Heat of Physical Change` also flakes when `random.randint` bounds invert for compounds whose bp < -100 (C6H6 seen once). None in compound code path.
2. **Move on to other files** — [reaction.py](src/models/reaction.py) and [solution.py](src/models/solution.py) are the next big targets; reaction.py especially has bare-except and string-splicing patterns similar to what compound.py had before.

### Session hygiene

- `python test/test_all_problems.py` — target **68+/73**, current stable range **68–70/73**.
- `python test/test_naming_golden.py` — must be **44/44**. Any mismatch is a user-visible regression in question text.
- Run both suites after any compound.py / naming.py / parsing.py change.