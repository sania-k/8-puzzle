"""
Quick test script for IDE
Run this to quickly test your puzzle solver with various cases
Automatically saves results to quick_test_results.txt
"""

import sys
from timeit import default_timer as timer
from puzzle import Problem, a_star_solve, print_solution

TEST_CASES = [
    {
        'name': 'Test 1 - Easy',
        'initial': [[1,2,3],[4,5,6],[7,0,8]],
        'goal': [[1,2,3],[4,5,6],[7,8,0]]
    },
    {
        'name': 'Test 2 - Easy',
        'initial': [[1,2,3],[5,0,6],[4,7,8]],
        'goal': [[1,2,3],[4,5,6],[7,8,0]]
    },
    {
        'name': 'Test 3 - Easy',
        'initial': [[0,1,2],[4,5,3],[7,8,6]],
        'goal': [[1,2,3],[4,5,6],[7,8,0]]
    },
    {
        'name': 'Test 4 - Medium',
        'initial': [[1,3,6],[5,0,2],[4,7,8]],
        'goal': [[1,2,3],[4,5,6],[7,8,0]]
    },
    {
        'name': 'Test 5 - Medium',
        'initial': [[4,1,2],[5,8,3],[7,0,6]],
        'goal': [[1,2,3],[4,5,6],[7,8,0]]
    },
    {
        'name': 'Test 6 - Hard',
        'initial': [[1,3,6],[5,0,7],[4,8,2]],
        'goal': [[1,2,3],[4,5,6],[7,8,0]]
    },
    {
        'name': 'Test 7 - Hard',
        'initial': [[8,1,3],[4,0,2],[7,6,5]],
        'goal': [[1,2,3],[4,5,6],[7,8,0]]
    },
    {
        'name': 'Test 8 - UNSOLVABLE',
        'initial': [[1,2,3],[4,5,6],[8,7,0]],
        'goal': [[1,2,3],[4,5,6],[7,8,0]]
    }
]

def run_test_case(test_case, show_path=False):
    """
    Run a single test case with both heuristics
    
    :param test_case: Dictionary with 'name', 'initial', and 'goal'
    :param show_path: If True, print the solution path
    """
    name = test_case['name']
    initial = test_case['initial']
    goal = test_case['goal']
    
    print(f"{'='*70}")
    print(f"{name}")
    print(f"{'='*70}")
    print(f"Initial: {initial[0]}")
    print(f"         {initial[1]}")
    print(f"         {initial[2]}\n")
    print(f"Goal:    {goal[0]}")
    print(f"         {goal[1]}")
    print(f"         {goal[2]}")
    
    # Test with Manhattan Distance
    print(f"\n--- Manhattan Distance Heuristic ---")
    problem_manhattan = Problem(goal, use_manhattan=True)
    start = timer()
    solution_manhattan = a_star_solve(problem_manhattan, initial)
    end = timer()

    if solution_manhattan:
        print(f"[SOLVED] Solution found in {len(solution_manhattan) - 1} moves")
        if show_path:
            print_solution(solution_manhattan, problem_manhattan)
    else:
        print("[NO SOLUTION] No solution found")
        print(f"  Nodes expanded: {problem_manhattan.nodes_expanded}")
        print(f"  Nodes generated: {problem_manhattan.nodes_generated}")
    
    print(f"  Execution Time: {end - start} seconds")

    # Test with Misplaced Tiles
    print(f"\n--- Misplaced Tiles Heuristic ---")
    problem_misplaced = Problem(goal, use_manhattan=False)
    start = timer()
    solution_misplaced = a_star_solve(problem_misplaced, initial)
    end = timer()
    
    if solution_misplaced:
        print(f"[SOLVED] Solution found in {len(solution_misplaced) - 1} moves")
        if show_path:
            print_solution(solution_misplaced, problem_misplaced)
    else:
        print("[NO SOLUTION] No solution found")
        print(f"  Nodes expanded: {problem_misplaced.nodes_expanded}")
        print(f"  Nodes generated: {problem_misplaced.nodes_generated}")
    
    print(f"  Execution Time: {end - start} seconds")

def quick_test(show_paths=False):
    """
    Run quick tests on test cases
    
    :param show_paths: If True, print solution paths for all tests
    """
    print("=" * 70)
    print("8-PUZZLE SOLVER - QUICK TEST")
    
    
    # Run test cases
    print("TEST CASES")
    for test in TEST_CASES:
        run_test_case(test, show_path=show_paths)
    
class DualOutput:
    """Write to both file and terminal simultaneously"""
    def __init__(self, file, terminal):
        self.terminal = terminal
        self.file = file
    
    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)
    
    def flush(self):
        self.terminal.flush()
        self.file.flush()

if __name__ == "__main__":
    # Set show_paths=True to see the solution paths
    # Set show_paths=False for just statistics
    show_paths = True
    
    output_file = "quick_test_results.txt"
    original_stdout = sys.stdout
    
    # Run tests with output to both console and file
    # Use UTF-8 encoding to handle special characters on Windows
    with open(output_file, 'w', encoding='utf-8') as f:
        sys.stdout = DualOutput(f, original_stdout)
        quick_test(show_paths=show_paths)
        sys.stdout = original_stdout
    
    print(f"\nResults saved to {output_file}")