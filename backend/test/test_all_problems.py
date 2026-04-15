"""
Runs every registered problem function multiple times and reports errors.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import src.problems  # triggers registration
from src.problem_registry import get_all_problems

RUNS_PER_PROBLEM = 100


def run_problem(entry):
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        if entry.accepts_rx_type:
            entry.func("")
        else:
            entry.func()
        return True, None
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
    finally:
        sys.stdout.close()
        sys.stdout = old_stdout


def main():
    registry = get_all_problems()
    total = len(registry)
    results = {}

    for num in sorted(registry.keys()):
        entry = registry[num]
        successes = 0
        errors = []
        for _ in range(RUNS_PER_PROBLEM):
            ok, err = run_problem(entry)
            if ok:
                successes += 1
            else:
                errors.append(err)
        results[num] = (entry.display_name, successes, errors)

    print(f"\n{'='*60}")
    print(f"  TEST RESULTS ({RUNS_PER_PROBLEM} runs per problem)")
    print(f"{'='*60}\n")

    passing = []
    failing = []
    for num, (name, successes, errors) in results.items():
        if successes == RUNS_PER_PROBLEM:
            passing.append(num)
        else:
            failing.append((num, name, successes, errors))

    print(f"PASSING: {len(passing)}/{total}")
    print(f"FAILING: {len(failing)}/{total}\n")

    if failing:
        print(f"{'#':<5} {'Problem':<45} {'Pass Rate':<12} First Error")
        print("-" * 95)
        for num, name, successes, errors in failing:
            unique_errors = list(set(errors))
            print(f"{num:<5} {name:<45} {successes}/{RUNS_PER_PROBLEM:<10} {unique_errors[0]}")
            for err in unique_errors[1:]:
                print(f"{'':>63}{err}")


if __name__ == "__main__":
    main()
