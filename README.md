# N-Puzzle Solver

A Python implementation that solves N-puzzle in an n×n grid using A* search algorithm. The program finds the optimal solution to rearrange square blocks into order with the fewest possible moves.

## Problem Description

- N-puzzle is played on an n×n grid with numbered squares from 1 to N and one blank space
- Numbers can be moved horizontally or vertically into the blank space
- Goal is to arrange numbers in ascending order with minimal moves
- Examples:
  - 8-puzzle: 3×3 grid labeled 1 through 8 plus blank
  - 15-puzzle: 4×4 grid labeled 1 through 15 plus blank

## Constraints

- Grid size (n) must be between 3 and 6 inclusive: 3 ≤ n ≤ 6
- Input file must follow specified format
- Only horizontal and vertical moves are allowed
- Program must find the optimal solution using A* search

## Input Format

The program reads from a file with the following format:
- n lines of input
- Each line contains n numbers separated by tab
- 0 represents the blank space
- Numbers 1 through n²-1 represent the tiles

Example input file (3×3 puzzle):
```
1   2   3
4   0   5
7   8   6
```

Example input file (4×4 puzzle):
```
1   2   3   4
5   6   0   8
9   10  7   11
13  14  15  12
```

## Usage

Run the program with an input file:
```bash
python src/puzzle.py <input_file>
```

Example:
```bash
python src/puzzle.py examples/n-puzzle.txt
```

## Implementation Details

The solution implements:
- A* search algorithm for finding optimal solution
- Manhattan distance heuristic for state evaluation
- Solvability check before attempting solution
- File input handling for various grid sizes
- Move validation for horizontal and vertical moves only

## Output

The program outputs:
1. Initial puzzle state
2. Number of moves in solution
3. Step-by-step solution path
4. "No solution exists" message if puzzle is unsolvable

Example output:
```
Initial State:
1 2 3
4 0 5
7 8 6

Puzzle solved in 2 moves!
Solution Path:
Move 1:
1 2 3
4 5 0
7 8 6

Move 2:
1 2 3
4 5 6
7 8 0
```

## Project Structure

```
n-puzzle-solver/
├── src/
│   ├── __init__.py
│   └── puzzle.py          # Main program code
├── examples/
│   └── n-puzzle.txt       # Example input file
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.8 or higher
- No additional dependencies required

## License

This project is licensed under the MIT License - see the LICENSE file for details.
