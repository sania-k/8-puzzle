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
        print(self.goal_positions)

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
                print(new_node) #TODO: delete new_node and directly append to neighbors ?(for debugging)

                neighbors.append(new_node)
                self.nodes_generated += 1
        print("nodes expanded",self.nodes_expanded,"nodes generated",self.nodes_generated) #TODO: delete (for debugging)
        return neighbors        

def AStar(problem, initial_state):
    initial_node = PuzzleNode(initial_state)
    initial_node.h = problem.calculate_heuristic(initial_state)

    print(initial_node) # for debugging
    
    frontier = [problem.get_neighbors(initial_node)]
    explored = []
    # TODO: complete A* algorithm



if __name__ == "__main__":   
    initial_state = [[0,2,3],[1,5,6],[4,7,8]]
    goal_state = [[1,2,3],[4,5,6],[7,8,0]]
    test_problem = Problem(goal_state, use_manhattan=True)
    test_solve = AStar(test_problem, initial_state)

    # TODO: implement user input for init and goal states, with checks to confirm valid states
    # Currently only coded to handle 3x3 boards and must also contain digits 0-8 with no repeats

    # Also might need to comment out the code more? no clue how strict grading will be on that
