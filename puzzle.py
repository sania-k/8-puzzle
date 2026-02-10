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
        Path cost

    h: int
        Heuristic

    manhattan_distance: bool
        If manhattan_distance is being used

    '''
    def __init__(self, node_state, parent_node=None, g=0, manhattan_distance=True):
        self.node_state = node_state
        self.parent_node = parent_node
        self.g = g
        if manhattan_distance:
            self.h = self.calculate_manhattan_distance()
        else:
            self.h = self.calculate_misplaced_tiles()

    def calculate_manhattan_distance(self):
        return 0

    def calculate_misplaced_tiles(self):
        return 0
    
    def get_cost(self):
        return self.g + self.h
    
    def get_neighbors(self):
        neighbors = []


    def __str__(self):
        result = ""
        for row in self.node_state:
            result += (f"{row[0]}  {row[1]}  {row[2]}\n")

        result += (f"Path Cost: {self.g}\nHeuristic: {self.h}\n")
        result += ("________________")
        return result


if __name__ == "__main__":    
    initial_state = [[1,2,3],[4,5,6],[7,8,0]]
    test = PuzzleNode(initial_state,manhattan_distance=False)
    print(test)