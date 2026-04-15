"""
Central registry for all chemistry problem functions.
Each problem is registered via the @problem decorator and returns (question, answer).
"""
from dataclasses import dataclass
from typing import Callable

@dataclass
class ProblemEntry:
    number: int
    display_name: str
    category: str
    func: Callable
    accepts_rx_type: bool = False

_registry: dict[int, ProblemEntry] = {}

# Category constants
MATH_REVIEW = "Math Review"
CHEMICAL_NOMENCLATURE = "Chemical Nomenclature"
CHEMICAL_QUANTITIES = "Chemical Quantities"
CHEMICAL_REACTIONS = "Chemical Reactions"
STOICHIOMETRY = "Stoichiometry"
THERMOCHEMISTRY = "Thermochemistry"
GAS_LAWS = "Gas Laws"
ELECTRON_CONFIGURATION = "Electron Configuration"
PERIODIC_TRENDS_AND_BONDS = "Periodic Trends and Bonds"
SOLUTIONS = "Solutions"
RATES = "Rates"
EQUILIBRIUM = "Equilibrium"
THERMODYNAMICS = "Thermodynamics"
ACID_BASE = "Acid-Base"
ELECTROCHEMISTRY = "Electrochemistry"
NUCLEAR_CHEMISTRY = "Nuclear Chemistry"

CATEGORY_ORDER = [
    MATH_REVIEW, CHEMICAL_NOMENCLATURE, CHEMICAL_QUANTITIES,
    CHEMICAL_REACTIONS, STOICHIOMETRY, THERMOCHEMISTRY,
    GAS_LAWS, ELECTRON_CONFIGURATION, PERIODIC_TRENDS_AND_BONDS,
    SOLUTIONS, RATES, EQUILIBRIUM, THERMODYNAMICS,
    ACID_BASE, ELECTROCHEMISTRY, NUCLEAR_CHEMISTRY,
]


def problem(number: int, display_name: str, category: str, accepts_rx_type: bool = False):
    """Decorator to register a problem function."""
    def decorator(func: Callable) -> Callable:
        _registry[number] = ProblemEntry(
            number=number,
            display_name=display_name,
            category=category,
            func=func,
            accepts_rx_type=accepts_rx_type,
        )
        return func
    return decorator


def get_problem(number: int) -> ProblemEntry:
    return _registry[number]


def get_all_problems() -> dict[int, ProblemEntry]:
    return dict(_registry)


def get_modes() -> list[str]:
    """Display names ordered by problem number."""
    return [_registry[i].display_name for i in range(1, max(_registry) + 1)]


def get_table_of_contents() -> list[dict]:
    """Generate category groupings from registry metadata."""
    cat_to_nums: dict[str, list[int]] = {}
    for entry in _registry.values():
        cat_to_nums.setdefault(entry.category, []).append(entry.number)
    for nums in cat_to_nums.values():
        nums.sort()

    all_ids = sorted(_registry.keys())
    categories = [{"id": 0, "name": "All", "questionIds": all_ids}]

    semester_one_cats = {MATH_REVIEW, CHEMICAL_NOMENCLATURE, CHEMICAL_QUANTITIES,
                         CHEMICAL_REACTIONS, STOICHIOMETRY, THERMOCHEMISTRY}

    for cat_id, cat_name in enumerate(CATEGORY_ORDER, start=1):
        categories.append({"id": cat_id, "name": cat_name, "questionIds": cat_to_nums.get(cat_name, [])})
        if cat_name == THERMOCHEMISTRY:
            sem1_ids = sorted(n for e in _registry.values() if e.category in semester_one_cats for n in [e.number])
            categories.append({"id": 7, "name": "Semester One", "questionIds": sem1_ids})

    return categories


def invoke_problem(number: int, rx_type: str = ""):
    """Call a problem by number. Returns (question_text, answer)."""
    entry = _registry[number]
    if entry.accepts_rx_type:
        return entry.func(rx_type)
    return entry.func()
