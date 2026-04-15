# Problems Table of Contents

Quick reference: which problem number/name lives in which file. All functions are registered via `@problem(num, display_name, CATEGORY)` and collected by `src/problem_registry.py`. Functions taking a reaction type use `accepts_rx_type=True`.

## math_review.py
| # | Display Name | Function |
|---|---|---|
| 1 | SI Units | `si_units` |

## chemical_nomenclature.py
| # | Display Name | Function |
|---|---|---|
| 2 | Average atomic mass | `average_atomic_mass` |
| 3 | Missing Isotope Percentage | `missing_isotope_percentage` |
| 4 | Formula to Name | `formula_to_name` |
| 5 | Name to Formula | `name_to_formula` |

## chemical_quantities.py
| # | Display Name | Function |
|---|---|---|
| 6 | Molar Conversions | `molar_conversions` |
| 7 | Calculate Percent Composition | `percent_composition` |
| 8 | Percent Composition to Equation | `percent_comp_to_equation` |
| 9 | Mass of One Element in a Compound | `mass_of_element_in_compound` |
| 10 | Complex Percent Composition to Equation | `complex_percent_comp_to_equation` |

## chemical_reactions.py
| # | Display Name | Function |
|---|---|---|
| 11 | Solubility Rules | `solubility_rules` |
| 12 | Writing Chemical Equations | `writing_chemical_equations` (rx) |

## stoichiometry.py
| # | Display Name | Function |
|---|---|---|
| 13 | Basic Stoichiometry | `basic_stoichiometry` (rx) |
| 14 | Percent Yield/Limiting Reagent | `percent_yield_limiting_reagent` (rx) |

## thermochemistry.py
| # | Display Name | Function |
|---|---|---|
| 15 | Heat of Physical Change | `heat_of_physical_change` |
| 16 | Coffee Cup Calorimetry | `coffee_cup_calorimetry` |
| 17 | Bomb Calorimetry | `bomb_calorimetry` (rx) |

## gas_laws.py
| # | Display Name | Function |
|---|---|---|
| 18 | Average Kinetic Energy | `average_kinetic_energy` |
| 19 | Effusion Rates | `effusion_rates` |
| 20 | Gas Laws | `gas_laws_problem` |
| 21 | Gas Stoichiometry | `gas_stoichiometry` (rx) |

## electron_configuration.py
| # | Display Name | Function |
|---|---|---|
| 22 | Electron configuration | `electron_config` |
| 23 | Nobel Gas Shorthand | `noble_gas_shorthand` |
| 24 | Paramagnetic vs Diamagnetic | `paramagnetic_vs_diamagnetic` |
| 25 | Quantum Numbers | `quantum_numbers_problem` |
| 26 | Basic Waves | `basic_waves` |
| 27 | Bohr's Law | `bohrs_law` |
| 28 | De Broglie for electrons | `de_broglie_electrons` |
| 29 | De Broglie in general | `de_broglie_general` |
| 30 | Heisenburg uncertainty principle | `heisenberg_uncertainty` |
| 31 | Identifying types of waves | `identifying_wave_types` |
| 32 | Harder Bohr's Law | `harder_bohrs_law` |

## periodic_trends_and_bonds.py
| # | Display Name | Function |
|---|---|---|
| 33 | Atomic Size | `atomic_size` |
| 34 | Ion Size | `ion_size` |
| 35 | Ionization Energy | `ionization_energy` |
| 36 | Electronegativity | `electronegativity_trend` |
| 37 | Electron Affinity | `electron_affinity` |
| 38 | All Periodic Trends | `all_periodic_trends` (calls 33-37) |
| 39 | Lattice Energy | `lattice_energy` |
| 40 | Lewis Dot Structure | `lewis_dot_structure` |
| 41 | VSEPR | `vsepr` |
| 42 | Bond Order | `bond_order` |
| 43 | Sigma and Pi Bonds | `sigma_and_pi_bonds` |
| 44 | Bond Energies | `bond_energies` |
| 45 | Enthalpy from Bond Energies | `enthalpy_from_bond_energies` |

## solutions.py
| # | Display Name | Function |
|---|---|---|
| 46 | Solubility Calculations | `solubility_calculations` |
| 47 | Determining Saturation | `determining_saturation` |
| 48 | Dilution | `dilution` |
| 49 | Solutions Unit Conversions (Aqueous) | `solution_conversions_aqueous` |
| 50 | Solutions Unit Conversions (general) | `solution_conversions_general` |
| 51 | Colligative Properties | `colligative_properties` |
| 52 | Molar Mass From bp/fp | `molar_mass_from_bp_fp` |
| 53 | Henry's Law | `henrys_law` |
| 54 | Reactions with Solubility Units | `reactions_with_solubility_units` |
| 55 | Hydrates | `hydrates` |
| 56 | Polar vs Nonpolar | `polar_vs_nonpolar` |

## rates.py
| # | Display Name | Function |
|---|---|---|
| 57 | Basic Concentration | `basic_concentration` |
| 58 | Method of Initial Rates | `method_of_initial_rates` |

## equilibrium.py
| # | Display Name | Function |
|---|---|---|
| 59 | Determining the Equilibrium Expression | `equilibrium_expression` |
| 60 | Missing Equilibrium Concentration | `missing_equilibrium_concentration` |
| 61 | Calculating K_eq | `calculating_keq` |
| 62 | Calculating Equilibrium Concentrations from Initial | `equilibrium_from_initial` |

## thermodynamics.py
| # | Display Name | Function |
|---|---|---|
| 63 | More Thermodynamics | `more_thermodynamics` |

## acid_base.py
| # | Display Name | Function |
|---|---|---|
| 64 | pH Conversions | `ph_conversions` |
| 65 | pH from Molarity | `ph_from_molarity` |
| 66 | pH with Common Ion Effect | `ph_common_ion_effect` |
| 67 | Neutralization/Tritation Reactions | `neutralization_titration` |
| 68 | Solubility Products | `solubility_products` |

## electrochemistry.py
| # | Display Name | Function |
|---|---|---|
| 69 | Oxidation Numbers | `oxidation_numbers` |
| 70 | Balancing Redox (WIP) | `balancing_redox` |
| 71 | Reaction Potential (WIP) | `reaction_potential` |
| 72 | Electroplating | `electroplating` |

## nuclear_chemistry.py
| # | Display Name | Function |
|---|---|---|
| 73 | Nuclear Decay | `nuclear_decay` |

---
*(rx) = function accepts a reaction type argument (`accepts_rx_type=True`).*