import heapq

class PuzzleNode:
    '''
    PuzzleNode

    Attributes
    ---
    node_state: 3x3 2d int array
        Represents the location of the numbers in the puzzle

    parent_node: PuzzleNode
        Node which spawned this one
        
    g: int
        Path cost value

    h: int
        Heuristic value

    hole_location: 2x1 int array
        Location of the hole (the 0) on the board
    
    '''
    def __init__(self, node_state, parent_node=None, h=0):
        self.node_state = node_state
        self.parent_node = parent_node        
        self.g = (parent_node.g + 1) if parent_node else 0
        self.h = h        

        self.hole_location = self.get_hole_location()

    def get_hole_location(self):
        '''
        Find the location of the hole (0) on the board
        '''
        for i in range(3):
            for j in range(3):
                if self.node_state[i][j] == 0:
                    return i, j
        raise ValueError("No blank tile found")
    
    def puzzle_rows(self):
        '''
        Return the puzzle board as a list of row strings with the g, h, and f of the node
        '''
        rows = [
            f"{row[0]}  {row[1]}  {row[2]}"
            for row in self.node_state
        ]

        measures = [f"g={self.g}", f"h={self.h}", f"f={self.g + self.h}"]

        return rows + measures

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)
    
    def __str__(self):
        result = ""
        for row in self.node_state:
            result += (f"{row[0]}  {row[1]}  {row[2]}\n")

        result += (f"Path Cost: {self.g}\nHeuristic: {self.h}\n")
        result += (f"f(n) = {self.g + self.h}\n")
        return result

class Problem:
    '''Creates 8 Puzzle problem
    
    Attributes
    ---
    goal_state: 3x3 int array

    use_manhattan: bool

    goal_positions: 9x2 int dict
        holds the positions of every tile in the goal configuration for heuristic
        calculations
    
    '''
    def __init__(self, goal_state=None, use_manhattan=True):
        self.goal_state = goal_state if goal_state else [[1,2,3],[4,5,6],[7,8,0]]
        self.use_manhattan = use_manhattan    

        # To find goal positions quickly for heuristic calculations
        self.goal_positions = {}
        for i in range(3):
            for j in range(3):
                tile = self.goal_state[i][j]
                self.goal_positions[tile] = (i,j)   

        self.nodes_expanded = 0
        self.nodes_generated = 0      

    def calculate_manhattan_distance(self, state):
        '''
        Returns heuristic value; compares given state to goal state to find the manhattan 
        distance of each tile compared to its desired position. 

        :param state: The state the heuristic is being calculated for
        '''
        h = 0
        for i in range(3):
            for j in range(3):
                tile = state[i][j]
                if tile!= 0:            # Don't count the hole/0 towards calculation                    
                    goal_i, goal_j = self.goal_positions[tile]
                    h += abs(i - goal_i) + abs(j - goal_j)
                    
        return h

    def calculate_misplaced_tiles(self, state):
        '''
        Returns heuristic value; compares given state to goal state to find how many tiles
        are in the wrong location
        
        :param state: The state the heuristic is being calculated for
        '''
        h = 0        
        for tile in range(1,9):         # Don't count the hole/0 towards calculation
            goal_i, goal_j = self.goal_positions[tile]
            if tile != state[goal_i][goal_j]:
                h +=1

        return h    
    
    def calculate_heuristic(self, state):
        '''
        Calculate heuristic depending on the desired measure for the problem. Either
        Manhattan Distance or Misplaced Tiles.
        
        :param state: The state the heuristic is being calculated for
        '''
        if self.use_manhattan:
            h = self.calculate_manhattan_distance(state)
        else:
            h = self.calculate_misplaced_tiles(state)

        return h
                
    def is_valid_move(self, i, j):
        '''
        Checks if a potential move is valid. Returns true if the coordinates are within
        the board space (between 0 and 3)

        :param i: Row coordinate
        :param j: Column coordinate
        '''
        return 0 <= i < 3 and 0 <= j < 3

    def get_neighbors(self, current_node):
        self.nodes_expanded += 1
        neighbors = []
        
        hole_i, hole_j = current_node.hole_location

        # For each possible move, confirm it is valid and then add it to the queue
        for delta_i, delta_j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_i, new_j = hole_i+delta_i, hole_j+delta_j
            if self.is_valid_move(new_i, new_j):
                new_state = [row[:] for row in current_node.node_state]

                # Moving a tile into the hole to create the new state
                new_state[hole_i][hole_j], new_state[new_i][new_j] = \
                    new_state[new_i][new_j], new_state[hole_i][hole_j]

                new_h = self.calculate_heuristic(new_state)
                
                # Setting current node as the parent to maintain branch structure
                new_node = PuzzleNode(new_state, current_node, h=new_h)

                neighbors.append(new_node)
                self.nodes_generated += 1
        return neighbors        

def construct_path(goal_state):
    '''
    Given the goal state, traverses up the tree to form the path and returns the result
    
    :param goal_state: PuzzleNode
    '''
    path = []
    current = goal_state
    # Adds parent nodes of each node to path until the initial state is reached (no parent)
    while current:
        path.append(current)
        current = current.parent_node
        
    path.reverse()
    return path

def a_star_solve(problem, initial_state):
    '''
    Given a problem and an initial state, will solve the problem and return the solution
    
    :param problem: Problem object
    :param initial_state: 3x3 int array
    '''
    initial_node = PuzzleNode(initial_state)
    initial_node.h = problem.calculate_heuristic(initial_state)

    frontier = [initial_node]

    # Putting frontier nodes in a heap, with the most promising nodes (lowest f) at the top
    heapq.heapify(frontier)   

    explored = set()
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))

        # Pop off the puzzle node with the lowest f value
        current_node = heapq.heappop(frontier)
        current_state_tuple = tuple(tuple(row) for row in current_node.node_state)
        
        # Check for goal state
        if current_node.node_state == problem.goal_state:         
            # If the goal has been found, compile the whole path and return
            return construct_path(current_node)
        
        # Find next possible moves and add current node to explored set 
        neighbors = problem.get_neighbors(current_node) 
        explored.add(current_state_tuple)

        # Confirm neighbors haven't already been explored and add to frontier heap
        for neighbor in neighbors:
            neighbor_state_tuple = tuple(tuple(row) for row in neighbor.node_state)
            if neighbor_state_tuple not in explored:
                heapq.heappush(frontier, neighbor)

    # If the frontier has been completely searched without finding the goal, no solution exists   
    return None

def print_solution(path, problem):
    grids_per_row = 5
        
    # Printing each move in the path horizontally, in columns of 5
    for start_idx in range(0, len(path), grids_per_row):
        end_idx = min(start_idx + grids_per_row, len(path))
        chunk = path[start_idx:end_idx]      
        
        move_labels = " ".join([f"Move {i+1}:    " for i in range(start_idx, end_idx)])
        print(f"\n{move_labels}")

        for row_idx in range(3):
            row_str = "    ".join([
                f"{node.node_state[row_idx][0]}  {node.node_state[row_idx][1]}  {node.node_state[row_idx][2]} "
                for node in chunk
            ])
            print(f"{row_str}")
                        
        g_scores = " ".join([f" g ={node.g:2d}     " for node in chunk])
        print(f"{g_scores}")
        
        h_scores = " ".join([f" h ={node.h:2d}     " for node in chunk])
        print(f"{h_scores}")

        f_scores = " ".join([f" f ={node.g + node.h:2d}     " for node in chunk])
        print(f"{f_scores}")
        
    print("\nStatistics:")
    print(f"Solution depth: {len(path) - 1}")
    print(f"Nodes expanded: {problem.nodes_expanded}")
    print(f"Nodes generated: {problem.nodes_generated}")
        
def get_puzzle_board_from_user(prompt="Enter puzzle board"):
    '''
    Prompts the user to enter a valid 8 puzzle board.
    The board must contain the digits 0-8 exactly once,
    arranged into a 3x3 grid.
    Returns the valid grid.

    :param prompt: Prompt to the user
    '''
    while True: # Loop until valid input
        # Explaining board rules to the user
        print(f"\n\n{prompt}")
        print("Enter a 8 puzzle board, with each tile value separated by spaces")
        print("Only values 0-8 are accepted, type out one row at a time, then press enter")
        print("Example: 1 2 3")
        print("\t 4 5 6")
        print("\t 7 8 0\n")

        user_row1 = input("Row 1: ").strip().split()
        user_row2 = input("Row 2: ").strip().split()
        user_row3 = input("Row 3: ").strip().split()

        rows = [user_row1, user_row2, user_row3]
        if any(len(row) != 3 for row in rows):
            print("Error: Each row must contain exactly 3 values")

        try:
            board = [list(map(int, row)) for row in rows]
        except ValueError:
            print("Error: All entries must be integers.")
            continue

        flat = [tile for row in board for tile in row]
        if set(flat) != set(range(9)):
            print("Error: Board must contain each number 0–8 exactly once.")
            continue

        print("Thank you!")
        return board

def get_heuristic_from_user():
    """
    Prompts the user to select a heuristic.
    Returns True for Manhattan Distance, False for Misplaced Tiles.
    """
    while True:
        print("\nSelect a heuristic:")
        print("[1] Misplaced Tiles")
        print("[2] Manhattan Distance")

        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            return False   # Misplaced Tiles
        elif choice == "2":
            return True    # Manhattan Distance
        else:
            print("Error: Invalid selection. Please enter 1 or 2.")


if __name__ == "__main__":   
    # Getting input from the user to define the problem
    initial_state = get_puzzle_board_from_user("INPUT THE INITIAL BOARD")
    goal_state = get_puzzle_board_from_user("INPUT THE GOAL BOARD")
    use_manhattan = get_heuristic_from_user()

    # Define the problem and solve
    puzzle_problem = Problem(goal_state, use_manhattan)
    solution = a_star_solve(puzzle_problem, initial_state)

    # Print results for the user
    if solution:
        print("Solution Found!")
        print_solution(solution, puzzle_problem)
    else:
        print("No Solution")
