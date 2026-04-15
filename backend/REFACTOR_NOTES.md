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

### I. Replace `"RANDOM"` magic sentinel entirely — **next up**

Constructor at [compound.py:31](src/models/compound.py#L31) still accepts both `None` and `"RANDOM"`. Drop `"RANDOM"`, grep and migrate the few remaining call sites. Low priority, mechanical.

### J. `refresh()` audit — [compound.py:219-222](src/models/compound.py#L219-L222)

Re-parses `self.equation` and re-computes `self.compound`. Now that `_rebuild_dict()` exists, `refresh()` should call it. Also: given the new canonical constructor, is `refresh()` even needed? Check `multCompound` — it mutates `self.compound` in place and updates `compoundDict` separately, which could just re-call `_rebuild_dict()`.

---

## Architectural notes / decisions made

- **Kept `compoundDict` as a stored field, not a `@cached_property`.** Reason: 20+ call sites read it, and the mutation-in-place paths (`multCompound`, `refresh`) would fight a cache. Single rebuild helper is enough.
- **Kept `self.equation` as the original input string** (with charge suffix stripped). Rebuilding it from `compoundToString(self.compound)` loses parentheses and reorders elements. Consumers rely on `"(" in self.equation` and ordering.
- **Legacy `"X_+N"` form preserved in `parse_formula`.** Removing it would require migrating all call sites in one shot, which is a separate (mechanical) task. See TODO G.
- **Did not touch `getNameFromEq` yet** — it's the single largest unit of risk in the file. Needs a golden-output test harness first. See TODO A.

---

## How to resume

1. Re-read this file.
2. `python test/test_all_problems.py` — confirm still at 68+/73. Current stable range is **68–70/73**; all failing problems are pre-existing flakies at 92–99% pass rate (62 Equilibrium Concentrations, 72 Electroplating, 73 Nuclear Decay, plus intermittent single-run flakes on 13/14/15/21/49/50/51/54).
3. `python test/test_naming_golden.py` — must be **44/44**. Any mismatch is a user-visible regression.
4. Next tasks in order: **I** (drop `"RANDOM"` sentinel — mechanical) → **J** (audit `refresh()`) → then consider removing the underscore branch in `parse_formula` now that TODO G is done.
5. Run the full suite after **every** change in [compound.py](src/models/compound.py) — it's a hotspot and regressions show up immediately.