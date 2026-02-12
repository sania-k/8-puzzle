import heapq
from importlib.resources import path

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

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def __str__(self):
        result = ""
        for row in self.node_state:
            result += (f"{row[0]}  {row[1]}  {row[2]}\n")

        result += (f"Path Cost: {self.g}\nHeuristic: {self.h}\n")
        result += ("________________")
        return result

class Problem:
    '''Creates 8 Puzzle problem
    
    Attributes
    ---
    goal_state: 3x3 int array

    use_manhattan: bool

    goal_positions: 9x2 int dict
        holds the positions of every tile in the goal configuration
    
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
        # print(self.goal_positions)

        self.nodes_expanded = 0
        self.nodes_generated = 0      

    def calculate_manhattan_distance(self, state):
        h = 0
        for i in range(3):
            for j in range(3):
                tile = state[i][j]
                if tile!= 0:                    
                    goal_i, goal_j = self.goal_positions[tile]
                    h += abs(i - goal_i) + abs(j - goal_j)
                    
        return h

    def calculate_misplaced_tiles(self, state):
        h = 0        
        for tile in range(1,9):
            goal_i, goal_j = self.goal_positions[tile]
            if tile != state[goal_i][goal_j]:
                h +=1

        return h    
    
    def calculate_heuristic(self, state):
        if self.use_manhattan:
            h = self.calculate_manhattan_distance(state)
        else:
            h = self.calculate_misplaced_tiles(state)

        return h
                
    def is_valid_move(self, i, j):
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

                new_state[hole_i][hole_j], new_state[new_i][new_j] = \
                    new_state[new_i][new_j], new_state[hole_i][hole_j]

                if self.use_manhattan:
                    new_h = self.calculate_manhattan_distance(new_state)
                else:
                    new_h = self.calculate_misplaced_tiles(new_state)
                
                new_node = PuzzleNode(new_state, current_node, h=new_h)
                # print(new_node) #TODO: delete new_node and directly append to neighbors ?(for debugging)

                neighbors.append(new_node)
                self.nodes_generated += 1
        # print("nodes expanded",self.nodes_expanded,"nodes generated",self.nodes_generated) #TODO: delete (for debugging)
        return neighbors        

def AStar(problem, initial_state):
    initial_node = PuzzleNode(initial_state)
    initial_node.h = problem.calculate_heuristic(initial_state)

    # print(initial_node) # for debugging
    
    # frontier = [problem.get_neighbors(initial_node)]
    # explored = []
    # TODO: complete A* algorithm
    frontier = [initial_node]
    heapq.heapify(frontier)
    explored = set()
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        current_node = heapq.heappop(frontier)
        current_state_tuple = tuple(tuple(row) for row in current_node.node_state)
        
        if current_node.node_state == problem.goal_state:
            print("Goal found!")
            print_solution(current_node, problem, max_frontier_size)
            return current_node
        
        explored.add(current_state_tuple)
        neighbors = problem.get_neighbors(current_node)

        for neighbor in neighbors:
            neighbor_state_tuple = tuple(tuple(row) for row in neighbor.node_state)
            if neighbor_state_tuple not in explored:
                heapq.heappush(frontier, neighbor)
                
    print("No solution found")
    return None

def print_solution(goal_node, problem, max_frontier_size):
    path = []
    current = goal_node
    while current:
        path.append(current)
        current = current.parent_node
        
    path.reverse()
    
    print("Solution found in", len(path) - 1, "steps:")
    
    grids_per_row = 5
    for start_idx in range(0, len(path), grids_per_row):
        end_idx = min(start_idx + grids_per_row, len(path))
        chunk = path[start_idx:end_idx]
        
        move_labels = "  ".join([f"  Move {i}  " for i in range(start_idx, end_idx)])
        print(f"\n{move_labels}")
        
        f_scores = "  ".join([f" f={node.g + node.h:2d} " for node in chunk])
        print(f"{f_scores}")
        
        for row_idx in range(3):
            row_str = "    ".join([
                f"{node.node_state[row_idx][0]}  {node.node_state[row_idx][1]}  {node.node_state[row_idx][2]}"
                for node in chunk
            ])
            print(f"{row_str}")
        
    print("\nStatistics:")
    print(f"Solution depth: {goal_node.g}")
    print(f"Nodes expanded: {problem.nodes_expanded}")
    print(f"Nodes generated: {problem.nodes_generated}")
    print(f"Max frontier size: {max_frontier_size}")
        
if __name__ == "__main__":   
    initial_state = [[0,2,3],[1,5,6],[4,7,8]]
    goal_state = [[1,2,3],[4,5,6],[7,8,0]]
    print("Using Manhattan Distance Heuristic:")
    test_problem = Problem(goal_state, use_manhattan=True)
    test_solve = AStar(test_problem, initial_state)
    print("\nUsing Misplaced Tiles Heuristic:")
    test_problem2 = Problem(goal_state, use_manhattan=False)
    test_solve2 = AStar(test_problem, initial_state)

    # TODO: implement user input for init and goal states, with checks to confirm valid states
    # Currently only coded to handle 3x3 boards and must also contain digits 0-8 with no repeats

    # Also might need to comment out the code more? no clue how strict grading will be on that
