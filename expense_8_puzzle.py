# -*- coding: utf-8 -*-
"""A1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VQxXHp9uNH3K7S3VRUc-US0UK1h0XP5P
"""

import argparse
from collections import deque
import heapq
import itertools

def move(state, direction):
    empty_slot = state.index(0)
    x, y = empty_slot // 3, empty_slot % 3
    new_state = state[:]

    if direction == "up" and x > 0:
        swap_idx = (x-1)*3 + y
    elif direction == "down" and x < 2:
        swap_idx = (x+1)*3 + y
    elif direction == "left" and y > 0:
        swap_idx = x*3 + (y-1)
    elif direction == "right" and y < 2:
        swap_idx = x*3 + (y+1)
    else:
        return None, 0

    move_cost = new_state[swap_idx]
    new_state[empty_slot], new_state[swap_idx] = new_state[swap_idx], new_state[empty_slot]
    return new_state, move_cost

def invert_direction(direction):
    if direction == "up":
        return "down"
    elif direction == "down":
        return "up"
    elif direction == "left":
        return "right"
    elif direction == "right":
        return "left"


def log_to_file(message):
    with open("dump.txt", "a") as file:
        file.write(message + "\n")

def breadth_first_search(initial, goal, dump=False):
    # Clear dump.txt content if dump is enabled
    if dump:
        with open("dump.txt", "w") as file:
            file.write("=== BFS START ===\n")

    metrics = {
        'nodes_popped': 0,
        'nodes_generated': 0,
        'max_fringe_size': 0,
        'nodes_expanded': 0
    }

    root = {'state': initial, 'path': [], 'cost': 0}

    if root['state'] == goal:
        if dump:
            log_to_file("Initial state is the goal!")
        return root['path'], root['cost'], metrics

    frontier = deque([root])
    explored = set()

    while frontier:
        node = frontier.popleft()
        metrics['nodes_popped'] += 1

        if tuple(node['state']) in explored:
            continue

        explored.add(tuple(node['state']))

        if dump:
            # Log the current state details
            log_to_file(f"\nProcessing Node: {node['state']} with cost {node['cost']}")
            log_to_file(f"Path: {' -> '.join(node['path'])}")
            log_to_file(f"Frontier Size: {len(frontier)} | Explored Set Size: {len(explored)}")
            log_to_file("Generating successors:")

        successors = []
        goal_found = False
        goal_child = None

        for action in ["up", "down", "left", "right"]:
            child_state, move_cost = move(node['state'], action)

            if child_state and tuple(child_state) not in explored:
                move_tile = move_cost
                child = {
                    'state': child_state,
                    'path': node['path'] + [f"Move {move_tile} {invert_direction(action).capitalize()}"],
                    'cost': node['cost'] + move_cost
                }
                metrics['nodes_generated'] += 1
                successors.append(child)
                frontier.append(child)
                if child_state == goal:
                    goal_found = True
                    goal_child = child

        if dump:
            # Log successor details
            for successor in successors:
                log_to_file(f"    Successor: state = {successor['state']}, cost = {successor['cost']}, path = {successor['path']}")

        if goal_found:
            if dump:
                log_to_file("Goal found!")
                log_to_file(f"Solution Path: {' -> '.join(goal_child['path'])}")
                log_to_file("=== BFS COMPLETED ===")
            return goal_child['path'], goal_child['cost'], metrics

        metrics['nodes_expanded'] += 1
        metrics['max_fringe_size'] = max(metrics['max_fringe_size'], len(frontier))

    if dump:
        log_to_file("No solution found!")
        log_to_file("=== BFS COMPLETED ===")
    return None, 0, metrics




def depth_first_search(initial, goal, dump=False):
    # Clear dump.txt content if dump is enabled
    if dump:
        with open("dump.txt", "w") as file:
            file.write("=== DFS START ===\n")

    metrics = {
        'nodes_popped': 0,
        'nodes_expanded': 0,
        'nodes_generated': 0,
        'max_fringe_size': 0
    }

    root = {'state': initial, 'path': [], 'cost': 0}

    if root['state'] == goal:
        if dump:
            log_to_file("Initial state is the goal!")
            log_to_file("=== DFS COMPLETED ===")
        return root['path'], root['cost'], metrics

    frontier = deque([root])  #  stack
    explored = set()

    while frontier:
        node = frontier.pop()  # Pop from stack
        metrics['nodes_popped'] += 1
        explored.add(tuple(node['state']))

        if dump:
            # Log the current state details
            log_to_file(f"\nProcessing Node: {node['state']} with cost {node['cost']}")
            log_to_file(f"Path: {' -> '.join(node['path'])}")
            log_to_file(f"Frontier Size: {len(frontier)} | Explored Set Size: {len(explored)}")
            log_to_file("Generating successors:")

        successors = []
        goal_found = False
        goal_child = None

        for action in ["up", "down", "left", "right"]:
            child_state, move_cost = move(node['state'], action)

            if child_state and tuple(child_state) not in explored:
                move_tile = move_cost
                child = {
                    'state': child_state,
                    'path': node['path'] + [f"Move {move_tile} {invert_direction(action).capitalize()}"],
                    'cost': node['cost'] + move_cost
                }
                metrics['nodes_generated'] += 1
                successors.append(child)
                frontier.append(child)  # Push to stack
                if child_state == goal:
                    goal_found = True
                    goal_child = child

        if dump:
            # Log successor details
            for successor in successors:
                log_to_file(f"    Successor: state = {successor['state']}, cost = {successor['cost']}, path = {successor['path']}")

        if goal_found:
            if dump:
                log_to_file("Goal found!")
                log_to_file(f"Solution Path: {' -> '.join(goal_child['path'])}")
                log_to_file("=== DFS COMPLETED ===")
            return goal_child['path'], goal_child['cost'], metrics

        metrics['nodes_expanded'] += 1
        metrics['max_fringe_size'] = max(metrics['max_fringe_size'], len(frontier))

    if dump:
        log_to_file("No solution found!")
        log_to_file("=== DFS COMPLETED ===")
    return None, 0, metrics



def depth_limited_search(initial, goal, depth_limit, dump=False):
    # Clear dump.txt content if dump is enabled
    if dump:
        with open("dump.txt", "w") as file:
            file.write("=== DLS START ===\n")

    metrics = {
        'nodes_popped': 0,
        'nodes_generated': 0,
        'nodes_expanded': 0,
        'max_fringe_size': 0
    }

    root = {'state': initial, 'path': [], 'cost': 0, 'depth': 0}

    if root['state'] == goal:
        if dump:
            log_to_file("Initial state is the goal!")
            log_to_file("=== DLS COMPLETED ===")
        return root['path'], root['cost'], metrics

    frontier = deque([root])
    explored = set()

    while frontier:
        node = frontier.pop()
        metrics['nodes_popped'] += 1

        if tuple(node['state']) in explored:
            continue

        explored.add(tuple(node['state']))

        if dump:
            # Log the current state details
            log_to_file(f"\nProcessing Node: {node['state']} with cost {node['cost']} and depth {node['depth']}")
            log_to_file(f"Path: {' -> '.join(node['path'])}")
            log_to_file(f"Frontier Size: {len(frontier)} | Explored Set Size: {len(explored)}")
            log_to_file("Generating successors:")

        successors = []

        if node['depth'] < depth_limit:
            goal_found = False
            goal_child = None
            for action in ["up", "down", "left", "right"]:
                child_state, move_cost = move(node['state'], action)

                if child_state and tuple(child_state) not in explored:
                    move_tile = move_cost
                    child = {
                        'state': child_state,
                        'path': node['path'] + [f"Move {move_tile} {invert_direction(action).capitalize()}"],
                        'cost': node['cost'] + move_cost,
                        'depth': node['depth'] + 1
                    }
                    metrics['nodes_generated'] += 1
                    successors.append(child)
                    frontier.append(child)
                    if child_state == goal:
                        goal_found = True
                        goal_child = child

            if dump:
                # Log successor details
                for successor in successors:
                    log_to_file(f"    Successor: state = {successor['state']}, cost = {successor['cost']}, depth = {successor['depth']}, path = {successor['path']}")

            if goal_found:
                if dump:
                    log_to_file("Goal found!")
                    log_to_file(f"Solution Path: {' -> '.join(goal_child['path'])}")
                    log_to_file("=== DLS COMPLETED ===")
                return goal_child['path'], goal_child['cost'], metrics

        metrics['nodes_expanded'] += 1
        metrics['max_fringe_size'] = max(metrics['max_fringe_size'], len(frontier))

    if dump:
        log_to_file("No solution found within the given depth limit!")
        log_to_file("=== DLS COMPLETED ===")
    return None, 0, metrics



# Get depth limit from user
#depth_limit = int(input("Enter the depth limit: "))



def iterative_deepening_search(initial, goal, dump=False):
    # Clear dump.txt content if dump is enabled
    if dump:
        with open("dump.txt", "w") as file:
            file.write("=== IDS START ===\n")

    depth = 0
    while True:
        if dump:
            log_to_file(f"\n--- Starting search with depth limit: {depth} ---\n")

        result, total_cost, metrics = depth_limited_search(initial, goal, depth, dump)

        if result:
            if dump:
                log_to_file(f"Goal found at depth {depth}!")
                log_to_file(f"Solution Path: {' -> '.join(result)}")
                log_to_file("=== IDS COMPLETED ===")
            return result, total_cost, metrics

        if dump:
            log_to_file(f"Depth {depth} completed without finding a solution. Increasing depth...\n")

        depth += 1










def uniform_cost_search(initial, goal, dump=False):
    # Clear dump.txt content if dump is enabled
    if dump:
        with open("dump.txt", "w") as file:
            file.write("=== UCS START ===\n")

    metrics = {
        'nodes_popped': 0,
        'nodes_generated': 0,
        'max_fringe_size': 0,
        'nodes_expanded': 0
    }

    root = {'state': initial, 'path': [], 'cost': 0}
    counter = itertools.count()

    if root['state'] == goal:
        if dump:
            log_to_file("Initial state is the goal!")
            log_to_file("=== UCS COMPLETED ===")
        return root['path'], root['cost'], metrics

    frontier = [(0, next(counter), root)]
    explored = set()

    while frontier:
        _, _, node = heapq.heappop(frontier)
        metrics['nodes_popped'] += 1

        if tuple(node['state']) in explored:
            continue

        explored.add(tuple(node['state']))

        if dump:
            log_to_file(f"\nProcessing Node: state = {node['state']}, cost = {node['cost']}")
            log_to_file(f"Path: {' -> '.join(node['path'])}")
            log_to_file(f"Frontier Size: {len(frontier)} | Explored Set Size: {len(explored)}")
            log_to_file("Generating successors:")

        successors = []

        for action in ["up", "down", "left", "right"]:
            child_state, move_cost = move(node['state'], action)

            if child_state and tuple(child_state) not in explored:
                move_tile = move_cost
                child = {
                    'state': child_state,
                    'path': node['path'] + [f"Move {move_tile} {invert_direction(action).capitalize()}"],
                    'cost': node['cost'] + move_cost
                }
                metrics['nodes_generated'] += 1
                successors.append(child)
                if child_state == goal:
                    if dump:
                        log_to_file("Goal found!")
                        log_to_file(f"Solution Path: {' -> '.join(child['path'])}")
                        log_to_file("=== UCS COMPLETED ===")
                    return child['path'], child['cost'], metrics
                heapq.heappush(frontier, (child['cost'], next(counter), child))

        if dump:
            for successor in successors:
                log_to_file(f"    Successor: state = {successor['state']}, cost = {successor['cost']}, path = {successor['path']}")
                if successor['state'] == goal:
                    log_to_file("Goal found!")
                    log_to_file(f"Solution Path: {' -> '.join(successor['path'])}")
                    log_to_file("=== UCS COMPLETED ===")
                    return successor['path'], successor['cost'], metrics

        metrics['nodes_expanded'] += 1
        metrics['max_fringe_size'] = max(metrics['max_fringe_size'], len(frontier))

    if dump:
        log_to_file("No solution found!")
        log_to_file("=== UCS COMPLETED ===")
    return None, 0, metrics






# Manhattan distance
def manhattan_distance(state, goal):
    distance = 0
    for number in range(1, 9):
        x1, y1 = divmod(state.index(number), 3)
        x2, y2 = divmod(goal.index(number), 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def greedy_search(initial, goal, dump=False):
    if dump:
        with open("dump.txt", "w") as file:
            file.write("=== Greedy Search START ===\n")

    metrics = {
        'nodes_popped': 0,
        'nodes_generated': 0,
        'max_fringe_size': 0,
        'nodes_expanded': 0
    }

    root = {'state': initial, 'path': [], 'cost': 0}
    counter = itertools.count()

    if root['state'] == goal:
        if dump:
            log_to_file("Initial state is the goal!")
            log_to_file("=== Greedy Search COMPLETED ===")
        return root['path'], root['cost'], metrics

    frontier = [(manhattan_distance(initial, goal), next(counter), root)]
    explored = set()

    while frontier:
        _, _, node = heapq.heappop(frontier)
        metrics['nodes_popped'] += 1

        if tuple(node['state']) in explored:
            continue

        explored.add(tuple(node['state']))

        if dump:
            log_to_file(f"\nProcessing Node: state = {node['state']}, cost = {node['cost']}")
            log_to_file(f"Path: {' -> '.join(node['path'])}")
            log_to_file(f"Frontier Size: {len(frontier)} | Explored Set Size: {len(explored)}")
            log_to_file("Generating successors:")

        successors = []

        for action in ["up", "down", "left", "right"]:
            child_state, move_cost = move(node['state'], action)

            if child_state and tuple(child_state) not in explored:
                move_tile = move_cost
                child = {
                    'state': child_state,
                    'path': node['path'] + [f"Move {move_tile} {invert_direction(action).capitalize()}"],
                    'cost': node['cost'] + move_cost
                }
                metrics['nodes_generated'] += 1
                successors.append(child)
                if child_state == goal:
                    if dump:
                        log_to_file("Goal found!")
                        log_to_file(f"Solution Path: {' -> '.join(child['path'])}")
                        log_to_file("=== Greedy Search COMPLETED ===")
                    return child['path'], child['cost'], metrics
                heapq.heappush(frontier, (manhattan_distance(child_state, goal), next(counter), child))

        if dump:
            for successor in successors:
                log_to_file(f"    Successor: state = {successor['state']}, cost = {successor['cost']}, path = {successor['path']}")
                if successor['state'] == goal:
                    log_to_file("Goal found!")
                    log_to_file(f"Solution Path: {' -> '.join(successor['path'])}")
                    log_to_file("=== Greedy Search COMPLETED ===")
                    return successor['path'], successor['cost'], metrics

        metrics['nodes_expanded'] += 1
        metrics['max_fringe_size'] = max(metrics['max_fringe_size'], len(frontier))

    if dump:
        log_to_file("No solution found!")
        log_to_file("=== Greedy Search COMPLETED ===")
    return None, 0, metrics



def a_star_search(initial, goal, dump=False):
    if dump:
        with open("dump.txt", "w") as file:
            file.write("=== A* Search START ===\n")

    metrics = {
        'nodes_popped': 0,
        'nodes_generated': 0,
        'max_fringe_size': 0,
        'nodes_expanded': 0
    }

    root = {'state': initial, 'path': [], 'cost': 0}
    counter = itertools.count()

    if root['state'] == goal:
        if dump:
            log_to_file("Initial state is the goal!")
            log_to_file("=== A* Search COMPLETED ===")
        return root['path'], root['cost'], metrics

    frontier = [(manhattan_distance(initial, goal), next(counter), root)]
    explored = set()

    while frontier:
        _, _, node = heapq.heappop(frontier)
        metrics['nodes_popped'] += 1

        if tuple(node['state']) in explored:
            continue

        explored.add(tuple(node['state']))

        if dump:
            log_to_file(f"\nProcessing Node: state = {node['state']}, cost = {node['cost']}")
            log_to_file(f"Path: {' -> '.join(node['path'])}")
            log_to_file(f"Frontier Size: {len(frontier)} | Explored Set Size: {len(explored)}")
            log_to_file("Generating successors:")

        successors = []

        for action in ["up", "down", "left", "right"]:
            child_state, move_cost = move(node['state'], action)

            if child_state and tuple(child_state) not in explored:
                move_tile = move_cost
                child = {
                    'state': child_state,
                    'path': node['path'] + [f"Move {move_tile} {invert_direction(action).capitalize()}"],
                    'cost': node['cost'] + move_cost
                }
                metrics['nodes_generated'] += 1
                successors.append(child)
                if child_state == goal:
                    if dump:
                        log_to_file("Goal found!")
                        log_to_file(f"Solution Path: {' -> '.join(child['path'])}")
                        log_to_file("=== A* Search COMPLETED ===")
                    return child['path'], child['cost'], metrics
                f = child['cost'] + manhattan_distance(child_state, goal)
                heapq.heappush(frontier, (f, next(counter), child))

        if dump:
            for successor in successors:
                log_to_file(f"    Successor: state = {successor['state']}, cost = {successor['cost']}, path = {successor['path']}")
                if successor['state'] == goal:
                    log_to_file("Goal found!")
                    log_to_file(f"Solution Path: {' -> '.join(successor['path'])}")
                    log_to_file("=== A* Search COMPLETED ===")
                    return successor['path'], successor['cost'], metrics

        metrics['nodes_expanded'] += 1
        metrics['max_fringe_size'] = max(metrics['max_fringe_size'], len(frontier))

    if dump:
        log_to_file("No solution found!")
        log_to_file("=== A* Search COMPLETED ===")
    return None, 0, metrics




def read_puzzle_from_file(filename):
    """Read the puzzle from a file."""
    with open(filename, 'r') as file:
        lines = file.readlines()

        # Ignore "END OF FILE" or any trailing data after the puzzle
        lines = [line.strip() for line in lines if line.strip() != "END OF FILE"]

        puzzle = []
        for line in lines:
            puzzle.extend(map(int, line.split()))

    return puzzle


def parse_args():
    parser = argparse.ArgumentParser(description="8-puzzle solver")
    parser.add_argument('initial_file', help="File containing the initial state")
    parser.add_argument('goal_file', help="File containing the goal state")
    parser.add_argument('algorithm', nargs='?', default='astar', choices=['bfs', 'dfs', 'dls', 'idds', 'ucs', 'greedy', 'astar'],
                        help="The algorithm to use for solving. Defaults to a_star if not specified.")
    parser.add_argument('dump', type=bool, nargs='?', default=False, help="If True, will dump paths to dump.txt")
    #parser.add_argument('algorithm', choices=['bfs', 'dfs', 'dls', 'idds', 'ucs', 'greedy', 'astar'],
                        #help="The algorithm to use for solving")

    return parser.parse_args()


def main():
    args = parse_args()
    initial = read_puzzle_from_file(args.initial_file)
    goal = read_puzzle_from_file(args.goal_file)

    
    

    if args.algorithm == 'bfs':
        result, total_cost, metrics = breadth_first_search(initial, goal, args.dump)
    elif args.algorithm == 'dfs':
        result, total_cost, metrics = depth_first_search(initial, goal, args.dump)
    elif args.algorithm == 'dls':
        depth_limit = int(input("Enter the depth limit for Depth Limited Search: "))
        result, total_cost, metrics = depth_limited_search(initial, goal, depth_limit, args.dump)
    elif args.algorithm == 'idds':
        result, total_cost, metrics = iterative_deepening_search(initial, goal, args.dump)
    elif args.algorithm == 'ucs':
        result, total_cost, metrics = uniform_cost_search(initial, goal, args.dump)
    elif args.algorithm == 'greedy':
        result, total_cost, metrics = greedy_search(initial, goal, args.dump)
    elif args.algorithm == 'astar':
         result, total_cost, metrics = a_star_search(initial, goal, args.dump)


    if result:
        print("Steps:")
        for step in result:
            print("\t", step)
        print("Nodes Popped:", metrics['nodes_popped'])
        print("Nodes Expanded:", metrics['nodes_expanded'])  # Nodes expanded is the same as nodes popped
        print("Nodes Generated:", metrics['nodes_generated'])
        print("Max Fringe Size:", metrics['max_fringe_size'])
        print(f"Solution Found at depth: {len(result)} with cost: {total_cost}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()

"""# New section"""