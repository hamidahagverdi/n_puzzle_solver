import heapq
import copy
import math
import sys

class NPuzzle:
    def __init__(self, initial_state):
        """
        Initialize the N-puzzle with the given initial state
        initial_state is a 2D list representing the puzzle
        """
        # Debug print to understand the initial state
        print("Initial State:")
        for row in initial_state:
            print(row)
        
        self.initial_state = initial_state
        self.n = len(initial_state)
        self.goal_state = self.create_goal_state()
        
    def create_goal_state(self):
        """
        Create the goal state based on the puzzle size
        Numbers will be in ascending order, with blank space at the end
        """
        goal = []
        total_nums = self.n * self.n
        current_num = 1
        
        for i in range(self.n):
            row = []
            for j in range(self.n):
                if current_num < total_nums:
                    row.append(current_num)
                    current_num += 1
                else:
                    row.append(' ')  # Blank space at the end
            goal.append(row)
        
        return goal
    
    def find_blank(self, state):
        """
        Find the position of the blank square
        """
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == ' ':
                    return i, j
        raise ValueError(f"No blank square found in state: {state}")
    
    def get_possible_moves(self, state):
        """
        Generate possible moves by moving the blank square
        """
        blank_row, blank_col = self.find_blank(state)
        moves = []
        
        # Possible move directions: up, down, left, right
        directions = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]
        
        for dr, dc in directions:
            new_row, new_col = blank_row + dr, blank_col + dc
            
            # Check if the new position is within the grid
            if 0 <= new_row < self.n and 0 <= new_col < self.n:
                # Create a new state by swapping blank with the adjacent square
                new_state = copy.deepcopy(state)
                new_state[blank_row][blank_col] = new_state[new_row][new_col]
                new_state[new_row][new_col] = ' '
                moves.append(new_state)
        
        return moves
    
    def manhattan_distance(self, state):
        """
        Calculate Manhattan distance heuristic
        """
        # Debug print
        print("Calculating Manhattan Distance for state:")
        for row in state:
            print(row)
        
        distance = 0
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] != ' ':
                    # Find the target position for this number
                    target_num = state[i][j]
                    target_row = (target_num - 1) // self.n
                    target_col = (target_num - 1) % self.n
                    
                    # Calculate Manhattan distance
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance
    
    def is_solvable(self, state):
        """
        Determine if the puzzle is solvable
        Based on inversions count
        """
        # Flatten the state
        flat_state = [num for row in state for num in row if num != ' ']
        
        # Count inversions
        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        
        # Solvability depends on grid size and number of inversions
        if self.n % 2 == 1:
            # Odd grid size: solvable if inversions is even
            return inversions % 2 == 0
        else:
            # Even grid size: find blank row from bottom
            blank_row = self.n - self.find_blank(state)[0]
            
            # Solvability based on blank position and inversions
            if blank_row % 2 == 1:
                return inversions % 2 == 0
            else:
                return inversions % 2 == 1
    
    def solve(self):
        """
        Solve the puzzle using A* search algorithm
        """
        # Debug print initial state dimensions
        print(f"Puzzle size: {self.n}x{self.n}")
        print(f"Grid dimensions: {len(self.initial_state)} rows x {len(self.initial_state[0])} columns")
        
        if not self.is_solvable(self.initial_state):
            return None
        
        # Define a wrapper class for comparison
        class StateWrapper:
            def __init__(self, f, g, state, path):
                self.f = f
                self.g = g
                self.state = state
                self.path = path
            
            def __lt__(self, other):
                return self.f < other.f
        
        # Priority queue for A* search
        start_node = StateWrapper(
            self.manhattan_distance(self.initial_state),  # f_score
            0,  # g_score
            self.initial_state,  # current state
            []  # path of moves
        )
        
        # Set to keep track of visited states to avoid cycles
        visited = set(tuple(map(tuple, self.initial_state)))
        
        # Heap to manage frontier
        frontier = [start_node]
        heapq.heapify(frontier)
        
        while frontier:
            current_node = heapq.heappop(frontier)
            current_state = current_node.state
            
            # Check if current state is goal state
            if current_state == self.goal_state:
                return current_node.path
            
            # Generate possible moves
            for move in self.get_possible_moves(current_state):
                # Convert move to hashable tuple for visited check
                move_tuple = tuple(map(tuple, move))
                
                # Skip if state has been visited
                if move_tuple in visited:
                    continue
                
                # Mark as visited
                visited.add(move_tuple)
                
                # Calculate new scores
                new_g = current_node.g + 1
                new_f = new_g + self.manhattan_distance(move)
                
                # Add to frontier
                new_path = current_node.path + [move]
                new_node = StateWrapper(new_f, new_g, move, new_path)
                heapq.heappush(frontier, new_node)
        
        # No solution found
        return None

def read_puzzle_from_file(filename):
    """
    Read puzzle configuration from a file with consistent grid parsing
    """
    with open(filename, 'r') as f:
        # Read all lines and split into values
        lines = f.readlines()
        
        # Find the maximum number of columns
        max_cols = max(len(line.strip().split()) for line in lines)
        
        # Parse puzzle ensuring consistent grid
        puzzle = []
        for line in lines:
            row = []
            vals = line.strip().split()
            
            # Pad the row to ensure consistent length
            for val in vals:
                val = val.strip()
                if val == '':
                    row.append(' ')
                else:
                    try:
                        row.append(int(val))
                    except ValueError:
                        row.append(' ')
            
            # Pad row to max columns if needed
            while len(row) < max_cols:
                row.append(' ')
            
            # Only add rows with content
            if row:
                puzzle.append(row)
        
        return puzzle

def main():
    # Check if filename is provided as command-line argument
    if len(sys.argv) < 2:
        print("Usage: python puzzle.py <input_file>")
        sys.exit(1)
    
    # Read puzzle from file
    puzzle_file = sys.argv[1]
    initial_state = read_puzzle_from_file(puzzle_file)
    
    # Create puzzle solver
    puzzle = NPuzzle(initial_state)
    
    # Solve the puzzle
    solution = puzzle.solve()
    
    # Output results
    if solution is None:
        print("No solution exists for this puzzle.")
    else:
        print(f"Puzzle solved in {len(solution)} moves!")
        print("Solution Path:")
        for i, state in enumerate(solution, 1):
            print(f"Move {i}:")
            for row in state:
                print(' '.join(str(val) for val in row))
            print()

if __name__ == "__main__":
    main()
