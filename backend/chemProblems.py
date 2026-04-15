"""Compatibility facade. Problem functions now live in src/problems/."""
import src.problems  # noqa: F401  triggers @problem registration
from src.problem_registry import (
    get_all_problems,
    get_modes,
    get_table_of_contents,
    invoke_problem,
)