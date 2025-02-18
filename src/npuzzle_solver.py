import heapq
import copy
import sys

class NPuzzle:
    """
    A class to solve N-Puzzle problems using A* search algorithm.
    
    Attributes:
        initial_state (list): The starting configuration of the puzzle
        n (int): Size of the puzzle grid
        goal_state (list): The target configuration of the puzzle
    """

    def __init__(self, initial_state):
        """
        Initialize the N-puzzle with the given initial state.

        Args:
            initial_state (list): 2D list representing the puzzle configuration
        """
        self.initial_state = initial_state
        self.n = len(initial_state)
        self.goal_state = self._create_goal_state()
    
    def _create_goal_state(self):
        """
        Create the goal state based on the puzzle size.

        Returns:
            list: Goal state configuration
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
    
    def _find_blank(self, state):
        """
        Find the position of the blank square.

        Args:
            state (list): Current puzzle state

        Returns:
            tuple: Row and column of the blank square
        
        Raises:
            ValueError: If no blank square is found
        """
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == ' ':
                    return i, j
        raise ValueError(f"No blank square found in state: {state}")
    
    def _get_possible_moves(self, state):
        """
        Generate possible moves by moving the blank square.

        Args:
            state (list): Current puzzle state

        Returns:
            list: Possible next states
        """
        blank_row, blank_col = self._find_blank(state)
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
    
    def _manhattan_distance(self, state):
        """
        Calculate Manhattan distance heuristic.

        Args:
            state (list): Current puzzle state

        Returns:
            int: Manhattan distance heuristic value
        """
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
    
    def is_solvable(self):
        """
        Determine if the puzzle is solvable.

        Returns:
            bool: True if the puzzle is solvable, False otherwise
        """
        # Flatten the state
        flat_state = [num for row in self.initial_state for num in row if num != ' ']
        
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
            blank_row = self.n - self._find_blank(self.initial_state)[0]
            
            # Solvability based on blank position and inversions
            if blank_row % 2 == 1:
                return inversions % 2 == 0
