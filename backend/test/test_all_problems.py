"""
Runs every problem function in chemProblems.py multiple times and reports which ones error.
Captures stdout so print output doesn't flood the terminal.
"""
import sys, io, traceback
from inflect import engine
from chemProblems import *

inflector = engine()

# Problems 12-14, 17, 21, 57 accept rxType; rest ignore it
TOTAL_PROBLEMS = 73
RUNS_PER_PROBLEM = 10

def run_problem(num):
    """Run problem number `num` once. Returns (success, error_msg)."""
    name = inflector.number_to_words(num).replace("-", "").replace(" ", "")
    func = globals().get(name)
    if func is None:
        return False, f"function '{name}' not found"

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        func(rxType="")
        return True, None
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
    finally:
        sys.stdout = old_stdout

def main():
    results = {}
    for num in range(1, TOTAL_PROBLEMS + 1):
        name = inflector.number_to_words(num).replace("-", "").replace(" ", "")
        successes = 0
        errors = []
        for run in range(RUNS_PER_PROBLEM):
            ok, err = run_problem(num)
            if ok:
                successes += 1
            else:
                errors.append(err)
        results[num] = (name, successes, errors)

    # Summary
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

    print(f"PASSING: {len(passing)}/{TOTAL_PROBLEMS}")
    print(f"FAILING: {len(failing)}/{TOTAL_PROBLEMS}\n")

    if failing:
        print(f"{'#':<5} {'Function':<25} {'Pass Rate':<12} First Error")
        print("-" * 80)
        for num, name, successes, errors in failing:
            unique_errors = list(set(errors))
            print(f"{num:<5} {name:<25} {successes}/{RUNS_PER_PROBLEM:<10} {unique_errors[0]}")
            for err in unique_errors[1:]:
                print(f"{'':>43}{err}")

if __name__ == "__main__":
    main()
