import random
import tkinter as tk
from queue import PriorityQueue
from tkinter import font

# Maze generation
def generate_maze(width, height):
    maze = [['0' for _ in range(width)] for _ in range(height)]
    for row in range(height):
        for col in range(width):
            if random.random() < 0.3:  # Adjust the obstacle density as desired
                maze[row][col] = '#'
    return maze

# Heuristic function (Manhattan distance)
def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

from queue import PriorityQueue

def astar(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1, '>'), (0, -1, '<'), (1, 0, 'v'), (-1, 0, '^')]  # (dx, dy, symbol) for (right, left, down, up)

    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {pos: float('inf') for row in maze for pos in row}
    g_score[start] = 0
    f_score = {pos: float('inf') for row in maze for pos in row}
    f_score[start] = heuristic(start, goal)

    visited_cells = set()

    while not open_set.empty():
        current = open_set.get()[1]
        visited_cells.add(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited_cells

        for dx, dy, symbol in directions:
            neighbor = current[0] + dx, current[1] + dy
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] != '#':
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    open_set.put((f_score[neighbor], neighbor))

    return None, visited_cells  # No path found


# Dijkstra's algorithm
def dijkstra(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1, '>'), (0, -1, '<'), (1, 0, 'v'), (-1, 0, '^')]  # (dx, dy, symbol) for (right, left, down, up)

    # Data structures for open set, closed set, and parent pointers
    open_set = PriorityQueue()
    open_set.put((0, start))  # priority queue ordered by distance
    came_from = {}
    distance = {pos: float('inf') for row in maze for pos in row}
    distance[start] = 0

    visited_cells = set()

    while not open_set.empty():
        current = open_set.get()[1]
        visited_cells.add(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited_cells

        for direction in directions:
            dx, dy, symbol = direction
            neighbor = current[0] + dx, current[1] + dy
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] != '#':
                tentative_distance = distance[current] + 1
                if tentative_distance < distance.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    distance[neighbor] = tentative_distance
                    open_set.put((distance[neighbor], neighbor))

    return None, visited_cells  # No path found


# Create the GUI window
window = tk.Tk()
window.title("Maze Solver")

# Global variables
maze = []
MAZE_WIDTH = 0
MAZE_HEIGHT = 0
CELL_SIZE = 20
start_node = None
goal_node = None


# Function to generate a new maze
def generate_new_maze():
    global MAZE_WIDTH, MAZE_HEIGHT, maze, CELL_SIZE, start_node, goal_node

    # Read the size values from the input boxes
    width_value = width_input.get()
    height_value = height_input.get()

    # Check if width and height values are provided
    if width_value == '' or height_value == '':
        print("Please enter valid width and height values.")
        return

    # Convert the values to integers
    try:
        MAZE_WIDTH = int(width_value)
        MAZE_HEIGHT = int(height_value)
    except ValueError:
        print("Invalid width or height value.")
        return

    # Calculate the maximum dimension of the maze
    max_dimension = max(MAZE_WIDTH, MAZE_HEIGHT)

    # Calculate the new cell size based on the window size and maximum dimension
    CELL_SIZE = max(400 // max_dimension, 20)

    # Calculate the new window dimensions based on the maze size and new cell size
    WINDOW_WIDTH = MAZE_WIDTH * CELL_SIZE
    WINDOW_HEIGHT = MAZE_HEIGHT * CELL_SIZE

    # Generate a new maze
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)

    # Configure the canvas size
    canvas.config(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

    # Clear the canvas
    canvas.delete("all")

    # Draw the maze on the canvas
    for row in range(MAZE_HEIGHT):
        for col in range(MAZE_WIDTH):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            if maze[row][col] == '#':
                canvas.create_rectangle(x1, y1, x2, y2, fill='black')
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white')

    start_node = None
    goal_node = None

# Global variable to store the path objects
path_objects = []

# Function to solve the maze and visualize the path
def solve_maze():
    global start_node, goal_node

    if start_node is None or goal_node is None:
        print("Please select the start and goal nodes.")
        return

    # Solve the maze using A* algorithm
    path, visited_cells = astar(maze, start_node, goal_node)

    # Clear the previous path objects

    # Visualize the visited cells in light blue
    for cell in visited_cells:
        row, col = cell
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill='olive drab')

    if path is not None:
        # Draw the path on the canvas
        for cell in path:
            row, col = cell
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            path_objects.append(canvas.create_rectangle(x1, y1, x2, y2, fill='RoyalBlue2'))
    
    x = path[0][1] 
    y = path[0][0] 

    x1 = x * CELL_SIZE
    y1 = y * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    X = path[len(path)-1][1]
    Y = path[len(path)-1][0]

    X1 = X * CELL_SIZE
    Y1 = Y * CELL_SIZE
    X2 = X1 + CELL_SIZE
    Y2 = Y1 + CELL_SIZE

    canvas.create_rectangle(x1, y1, x2, y2, fill='green')
    canvas.create_rectangle(X1, Y1, X2, Y2, fill='red')

    print("\n")
    print("A* visits these cells: ")
    print(visited_cells)
    print("\n")

    print("Shortest Path: ")
    print(path)
    print("\n")

    print("no. of visited cells in A*: " + str(len(visited_cells)))
    print("\n")
   



# Function to solve the maze using Dijkstra's algorithm and visualize the path
def solve_maze_dijkstra():
    global start_node, goal_node

    if start_node is None or goal_node is None:
        print("Please select the start and goal nodes.")
        return

    # Solve the maze using Dijkstra's algorithm
    path, visited_cells = dijkstra(maze, start_node, goal_node)

    # Clear the previous path objects

    if path is not None:
        # Draw the path on the canvas
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            x1_pixel = x1 * CELL_SIZE 
            y1_pixel = y1 * CELL_SIZE 
            x2_pixel = x2 * CELL_SIZE 
            y2_pixel = y2 * CELL_SIZE 

    # Visualize the visited cells
    for cell in visited_cells:
        row, col = cell
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill='gold')

    for i in range(len(path)):
        u = path[i][1]
        v = path[i][0]

        u1 = u * CELL_SIZE
        v1 = v * CELL_SIZE
        u2 = u1 + CELL_SIZE
        v2 = v1 + CELL_SIZE

        canvas.create_rectangle(u1, v1, u2, v2, fill='RoyalBlue2')



    x = path[0][1] 
    y = path[0][0] 

    x1 = x * CELL_SIZE
    y1 = y * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    X = path[len(path)-1][1]
    Y = path[len(path)-1][0]
    
    X1 = X * CELL_SIZE
    Y1 = Y * CELL_SIZE
    X2 = X1 + CELL_SIZE
    Y2 = Y1 + CELL_SIZE

    canvas.create_rectangle(x1, y1, x2, y2, fill='green')
    canvas.create_rectangle(X1, Y1, X2, Y2, fill='red')

    print("\n")
    print("Dijkstra visits these cells: ")
    print(visited_cells)
    print("\n")

    print("Shortest Path: ")
    print(path)
    print("\n")

    print("no. of visited cells in Dijkstra: " + str(len(visited_cells)))
    print("\n")



# Function to clear the previous path from the canvas
def clear_path():
    global path_objects
    for path_object in path_objects:
        canvas.delete(path_object)


# Function to handle mouse clicks on the canvas
def canvas_click(event):
    global start_node, goal_node

    # Calculate the row and column of the clicked cell
    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE

    if maze[row][col] == '#':
        return

    # Calculate the pixel coordinates of the clicked cell
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    # Check if a start node is already selected
    if start_node is None:
        # Draw a green rectangle to represent the start node
        start_node = (row, col)
        canvas.create_rectangle(x1, y1, x2, y2, fill='green')

    # Check if a goal node is already selected
    elif goal_node is None:
        # Draw a red rectangle to represent the goal node
        goal_node = (row, col)
        canvas.create_rectangle(x1, y1, x2, y2, fill='red')

    # If both start and goal nodes are selected, clear the canvas and redraw the maze
    elif start_node is not None and goal_node is not None:
        canvas.delete("all")
        for row in range(MAZE_HEIGHT):
            for col in range(MAZE_WIDTH):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                if maze[row][col] == '#':
                    canvas.create_rectangle(x1, y1, x2, y2, fill='black')
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill='white')

        # Reset the start and goal nodes
        start_node = None
        goal_node = None

# Create the GUI window
window.title("Maze Solver")
window.configure(bg='white')

# Set the font
label_font = font.Font(family="Tekton Pro", size=15)
button_font = font.Font(family="Tekton Pro", size=15)

# Create the GUI elements with the specified font
width_label = tk.Label(window, text="Width:", font=label_font)
width_label.grid(row=0, column=0)
width_input = tk.Entry(window)
width_input.grid(row=0, column=1)

height_label = tk.Label(window, text="Height:", font=label_font)
height_label.grid(row=0, column=2)
height_input = tk.Entry(window)
height_input.grid(row=0, column=3)

generate_button = tk.Button(window, text="Generate Maze", font=button_font, command=generate_new_maze)
generate_button.grid(row=0, column=4)

solve_button = tk.Button(window, text="Solve (A*)", font=button_font, command=solve_maze)
solve_button.grid(row=0, column=5)

solve_dijkstra_button = tk.Button(window, text="Show (Dijkstra) visits", font=button_font, command=solve_maze_dijkstra)
solve_dijkstra_button.grid(row=0, column=6)

canvas = tk.Canvas(window, width=400, height=400)
canvas.grid(row=1, column=0, columnspan=7)  # Place the canvas widget below the buttons
canvas.bind("<Button-1>", canvas_click)


# Run the GUI main loop
window.mainloop()


# legit
