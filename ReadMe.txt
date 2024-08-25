
8-Puzzle Solver

This project provides a solution for the 8-puzzle problem, a classic artificial intelligence problem. The 8-puzzle is a sliding puzzle that consists of a 3?3 frame of numbered square tiles in random order with one tile missing.

Programming Language Used: Python 3.9.7
Features:
- Multiple search algorithms to solve the puzzle.
- Extract puzzle from a text file.
- Command-line interface for easy usage.
- Option to dump the search process to an external file.

Search Algorithms Supported:

- **Breadth First Search (BFS)**
- **Depth First Search (DFS)**
- **Depth Limited Search (DLS)**
- **Iterative Deepening Depth Search (IDDS)**
- **Uniform Cost Search (UCS)**
- **Greedy Search**
- **A* Search**

Code Structure:

1. Utility Functions:
   
   - `move(state, direction)`: Moves the empty tile in the given direction and returns the new state and the cost of the move.
   
2. File Handling:
   - `read_puzzle_from_file(filename)`: Reads a puzzle state from a specified file and returns it as a list.

3. Command-Line Argument Parsing:
   - `parse_args()`: Parses command-line arguments to get the initial puzzle file, goal puzzle file, search algorithm to use, and the dump flag.

4. Search Algorithms:
      - Breadth-First Search: `breadth_first_search(initial, goal, dump)`
      - Depth-First Search: `depth_first_search(initial, goal, dump)`
      - Depth-Limited Search: `depth_limited_search(initial, goal, depth_limit, dump)`
      - Iterative Deepening Depth Search: `iterative_deepening_search(initial, goal, dump)`
      - Uniform-Cost Search: `uniform_cost_search(initial, goal, dump)`
      - Greedy Search: `greedy_search(initial, goal, dump)`
      - A* Search: `a_star_search(initial, goal, dump)`


Usage:

Command Line Arguments:
python3 expense_8_puzzle.py <start.txt> <goal.txt> [algorithm] [dump]

Arguments:
For BFS: python3 expense_8_puzzle.py start.txt goal.txt bfs
For DFS: python3 expense_8_puzzle.py start.txt goal.txt dfs
For DLS: python3 expense_8_puzzle.py start.txt goal.txt dls
For IDDS: python3 expense_8_puzzle.py start.txt goal.txt idds
For UCS: python3 expense_8_puzzle.py start.txt goal.txt ucs
For Greedy: python3 expense_8_puzzle.py start.txt goal.txt greedy
For A-Star: python3 expense_8_puzzle.py start.txt goal.txt astar

To create a dump file, set the dump flag to true
Example:
python search.py start.txt goal.txt bfs true

The above command will use the BFS algorithm and dump the search process to `dump.txt`. Similarly, you can create dump file for other algorithms as well.

***Note: When using Iterative Deepening Search with dump flag set to true, my IDS function will call Depth Limited Search function, so the dump file starts with Depth Limited Search being initiated, and at the end of the file we will Depth Limited Search complete at a certain depth, showing the solution path, finally indicating that the Iterative Deepening Search has also completed. 

***And for every algorithm ran with dump flag true, the previous dump file is deleted and starts with a new one.
Metrics:

For each search method, the following metrics are displayed:
- `nodes_popped`: Number of nodes removed from the frontier.
- `nodes_generated`: Number of successor nodes generated.
- `max_fringe_size`: Maximum number of nodes in the frontier at any point.
- `nodes_expanded`: Number of nodes expanded.

File Outputs:

If the `dump` argument is set to true, a detailed step-by-step log of the search process is written to `dump.txt`.

.
