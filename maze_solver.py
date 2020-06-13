import math
import time

import pygame

import DS as ds  # File with data structures

fps = 100
dim = (1000, 600)
caption = 'Maze Solver'
y_margin = 80

black = (0, 0, 0)
white = (255, 255, 255)
light_red = (255, 0, 0)
red = (200, 0, 0)
green = (0, 155, 0)
light_green = (0, 255, 0)
blue = (0, 0, 255)
light_yellow = (255, 255, 0)
yellow = (200, 200, 0)

box_size = 20
is_grid = True

no_solution = False

current_tool = 'pencil'
last_algo = None

rect_coords = set()
sol_coords = []
explored_coords = set()
start = None
destination = None

pygame.init()
gameDisplay = pygame.display.set_mode(dim)
pygame.display.set_caption(caption)
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 20, False, False)
medfont = pygame.font.SysFont("comicsansms", 30, False, False)
largefont = pygame.font.SysFont("comicsansms", 65, False, False)

tim = 0


def rect_list_init():
    global rect_coords
    global start
    global destination
    rect_list = []
    for x in rect_coords:
        rect_list.append(x)
    return rect_list


def neighbors(state):
    global rect_coords
    (x, y) = state
    candidates = [
        ("up", (x, y - box_size)),
        ("down", (x, y + box_size)),
        ("left", (x - box_size, y)),
        ("right", (x + box_size, y))
    ]

    result = []
    for action, (x, y) in candidates:
        if 0 <= x < dim[0] and y_margin <= y < dim[1] and (x, y) not in rect_coords:
            result.append((action, (x, y)))
    return result


def heuristic(x, y):
    global destination
    global start
    m_d = abs(destination[0] - x) + abs(destination[1] - y)
    a_d = abs(start[0] - x) + abs(start[1] - y)
    return m_d + a_d


def heuristic2(x, y):
    global destination
    global start
    m_d = (destination[0] - x) ** 2 + (destination[1] - y) ** 2
    a_d = (start[0] - x) ** 2 + (start[1] - y) ** 2
    return m_d + a_d


def neighbors_p(node):
    global rect_coords
    (x, y) = node.state
    candidates = [
        ("up", (x, y - box_size)),
        ("down", (x, y + box_size)),
        ("left", (x - box_size, y)),
        ("right", (x + box_size, y))
    ]

    result = []
    for action, (x, y) in candidates:
        if 0 <= x < dim[0] and y_margin <= y < dim[1] and (x, y) not in rect_coords:
            result.append((action, (x, y), heuristic(x, y)))
    return result


def Solve(type_search):
    global start
    global current_tool
    global destination
    global explored_coords
    global no_solution
    global last_algo
    # walls = rect_list_init()
    explored = set()
    num_explored = 0
    start_node = ds.Node(start, None, None)
    if type_search == 'BFS':
        frontier = ds.QueueFrontier()
        last_algo = 'BFS'
    if type_search == 'DFS':
        frontier = ds.StackFrontier()
        last_algo = 'DFS'
    frontier.add(start_node)
    if start is None or destination is None:
        print_grid()
        current_tool = 'pencil'
        return -1

    while True:
        node = frontier.remove()
        num_explored += 1

        if node is None:
            no_solution = True
            print_grid()
            return

        elif node.state == destination:
            actions = []
            cells = []
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            actions.reverse()
            cells.reverse()
            solution = (actions, cells)
            no_solution = False
            return solution

        explored.add(node.state)
        explored_coords = explored

        for action, state in neighbors(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = ds.Node(state=state, parent=node, action=action)
                frontier.add(child)


def A_Solve():
    global start
    global current_tool
    global destination
    global explored_coords
    global no_solution
    global last_algo

    explored = set()
    num_explored = 0

    last_algo = 'A'

    if start is None or destination is None:
        print_grid()
        current_tool = 'pencil'
        return -1

    frontier = ds.PriorityQueue()
    start_node = ds.PQ_Entry(start, None, None, math.inf)
    frontier.add(start_node)

    while True:
        latest_node = frontier.remove()
        num_explored += 1

        if latest_node is None:
            no_solution = True
            print_grid()
            return

        elif latest_node.state == destination:
            actions = []
            cells = []
            while latest_node.parent != None:
                actions.append(latest_node.action)
                cells.append(latest_node.state)
                latest_node = latest_node.parent
            actions.reverse()
            cells.reverse()
            solution = (actions, cells)
            no_solution = False
            return solution

        explored.add(latest_node.state)
        explored_coords = explored

        for action, state, priority in neighbors_p(latest_node):
            if not frontier.contains_state(state) and state not in explored:
                child = ds.PQ_Entry(state, action, latest_node, priority)
                frontier.add(child)


def print_solution(type_search):
    global destination
    global rect_coords
    global current_tool
    global sol_coords
    global tim

    t0 = time.perf_counter()

    if len(sol_coords) != 0:
        sol_coords.clear()
        explored_coords.clear()

    solution = Solve(type_search)
    if not no_solution:
        if solution == -1:
            return

        for (x, y) in solution[1]:
            sol_coords.append((x, y))
        print_grid()

        tim = round(time.perf_counter() - t0, 5)
    else:
        pass

    # current_tool = 'pencil'


def print_smart_solution():
    global destination
    global rect_coords
    global current_tool
    global sol_coords
    global tim

    if len(sol_coords) != 0:
        sol_coords.clear()
        explored_coords.clear()

    t0 = time.perf_counter()

    solution = A_Solve()
    if not no_solution:
        if solution == -1:
            return

        for (x, y) in solution[1]:
            sol_coords.append((x, y))
        print_grid()

        tim = round(time.perf_counter() - t0, 5)
    else:
        pass
    # current_tool = 'pencil'


def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
        textRect = textSurface.get_rect()
        return textSurface, textRect
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
        textRect = textSurface.get_rect()
        return textSurface, textRect
    elif size == 'large':
        textSurface = largefont.render(text, True, color)
        textRect = textSurface.get_rect()
        return textSurface, textRect


def button(msg, text_color, buttonx, buttony, buttonwidth, buttonheight, size, inactive_color, active_color,
           action=None):
    global current_tool
    global is_grid
    (x, y) = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if buttonx < x < buttonwidth + buttonx and buttony < y < buttonheight + buttony:
        pygame.draw.rect(gameDisplay, active_color, (buttonx, buttony, buttonwidth, buttonheight))
        if click[0] == 1 and action != None:
            if action == 'quit':
                pygame.quit()
                quit()
            elif action == 'controls':
                controls_page()
            elif action == 'play':
                GameLoop()
            elif action == 'starting_page':
                start_screen()
            # elif action == 'pause':
            # pause()
            elif action == 'set_pencil':
                current_tool = 'pencil'
            elif action == 'set_eraser':
                current_tool = 'eraser'
            elif action == 'set_clear':
                current_tool = 'clear'
            elif action == 'set_A':
                current_tool = 'setA'
            elif action == 'set_B':
                current_tool = 'setB'
            elif action == 'solve BFS':
                current_tool = 'solve BFS'
            elif action == 'solve DFS':
                current_tool = 'solve DFS'
            elif action == 'smart solve':
                current_tool = 'smart solve'
            elif action == 'options':
                options_page()
            elif action == 'maze':
                current_tool = 'maze'

            elif action == 'toggle grid':
                if is_grid == False:
                    is_grid = True
                else:
                    is_grid = False
            elif action == 'show stats':
                if len(sol_coords) != 0:
                    button(f'Path length(cells): {len(sol_coords)}', black, dim[0] // 2 - 50, 200, 350, 30, 'small',
                           light_yellow, light_yellow)
                    button(f'# Explored cells: {len(explored_coords)}', black, dim[0] // 2 - 50, 230, 350, 30, 'small',
                           light_yellow, light_yellow)
                    button(f'Time taken(s): {tim}', black, dim[0] // 2 - 50, 260, 350, 30,
                           'small',
                           light_yellow, light_yellow)
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (buttonx, buttony, buttonwidth, buttonheight))
    textSurface, textRect = text_objects(msg, text_color, size)
    textRect.center = buttonx + buttonwidth // 2, buttony + buttonheight // 2
    gameDisplay.blit(textSurface, textRect)


def pencil_tool():
    global current_tool
    global rect_coords
    global start
    global destination
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    x, y = (cur[0] // box_size) * box_size, (cur[1] // box_size) * box_size
    if click[0] == 1 and cur[1] > y_margin and (x, y) != start and (x, y) != destination:
        rect_coords.add((x, y))
        if (x, y) in sol_coords or (x, y) in explored_coords:
            sol_coords.clear()
            explored_coords.clear()
    print_grid()


def eraser_tool():
    global current_tool
    global rect_coords
    global start
    global destination
    global no_solution
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    x, y = (cur[0] // box_size) * box_size, (cur[1] // box_size) * box_size
    if click[0] == 1 and cur[1] > y_margin and (x, y) in rect_coords:
        rect_coords.remove((x, y))
    if click[0] == 1 and cur[1] > y_margin and (x, y) == start:
        start = None
    if click[0] == 1 and cur[1] > y_margin and (x, y) == destination:
        destination = None
    if click[0] == 1 and cur[1] > y_margin and (x, y) in sol_coords:
        sol_coords.remove((x, y))
    if click[0] == 1 and cur[1] > y_margin and (x, y) in explored_coords:
        explored_coords.remove((x, y))

    if no_solution:
        no_solution = False

    print_grid()


def clear_tool():
    global current_tool
    global rect_coords
    global start
    global destination
    global sol_coords
    global no_solution
    rect_coords.clear()
    sol_coords.clear()
    explored_coords.clear()
    start = None
    destination = None
    print_grid()
    current_tool = 'pencil'
    if no_solution:
        no_solution = False


def set_A_tool():
    global current_tool
    global rect_coords
    global start
    global sol_coords
    global explored_coords
    global no_solution

    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    x, y = (cur[0] // box_size) * box_size, (cur[1] // box_size) * box_size
    if click[0] == 1 and cur[1] > y_margin and (x, y) not in rect_coords:
        start = (x, y)
        sol_coords.clear()
        explored_coords.clear()
        if last_algo == 'BFS':
            print_solution('BFS')
        elif last_algo == 'DFS':
            print_solution('DFS')
        elif last_algo == 'A':
            print_smart_solution()
    print_grid()
    if no_solution:
        no_solution = False
    return


def set_B_tool():
    global current_tool
    global rect_coords
    global destination
    global start
    global no_solution
    global last_algo

    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    x, y = (cur[0] // box_size) * box_size, (cur[1] // box_size) * box_size
    if click[0] == 1 and cur[1] > y_margin and (x, y) not in rect_coords:
        destination = (x, y)
        if start is not None and len(sol_coords) != 0:
            sol_coords.clear()
            explored_coords.clear()
            if last_algo == 'BFS':
                print_solution('BFS')
            elif last_algo == 'DFS':
                print_solution('DFS')
            elif last_algo == 'A':
                print_smart_solution()
    print_grid()
    if no_solution:
        no_solution = False
    return


def print_grid():
    global current_tool
    global rect_coords
    global start
    global destination
    global sol_coords
    for x in rect_coords:
        pygame.draw.rect(gameDisplay, black,
                         ((x[0] // box_size) * box_size, (x[1] // box_size) * box_size, box_size, box_size))

    for cells in explored_coords:
        pygame.draw.rect(gameDisplay, light_yellow, (cells[0], cells[1], box_size, box_size))

    if len(sol_coords) != 0:
        for cells in sol_coords[0:-1]:
            pygame.draw.rect(gameDisplay, green, (cells[0], cells[1], box_size, box_size))

    if start is not None:
        pygame.draw.rect(gameDisplay, blue, (start[0], start[1], box_size, box_size))
    if destination is not None:
        pygame.draw.rect(gameDisplay, red, (destination[0], destination[1], box_size, box_size))


def message_to_screen(msg, color, y_displace=0, size='small'):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = dim[0] / 2, dim[1] / 2 + y_displace
    gameDisplay.blit(textSurface, textRect)
    pygame.display.update()


def start_screen():
    gameIntro = True
    gameDisplay.fill(white)
    while gameIntro:

        message_to_screen("Welcome to Maze Solver!", black, -50, 'large')

        button("Play", black, dim[0] // 2 - 50 - 150, 500, 100, 50, 'small', green, light_green, 'play')
        button("Controls", black, dim[0] // 2 - 50, 500, 100, 50, 'small', yellow, light_yellow, 'controls')
        button("Quit", black, dim[0] // 2 - 50 + 150, 500, 100, 50, 'small', red, light_red, 'quit')

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameIntro = False
                    pygame.quit()
                    quit()

                if event.key == pygame.K_c:
                    GameLoop()
                    gameIntro = False

            if event.type == pygame.QUIT:
                gameIntro = False
                pygame.quit()
                quit()

    clock.tick(5)


def options_page():
    options = True
    gameDisplay.fill(white)
    while options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if is_grid:
            button('Show Grid', black, dim[0] // 2 - 50, 100, 100, 30, 'small', light_green, light_green,
                   action='toggle grid')
        else:
            button('Show Grid', black, dim[0] // 2 - 50, 100, 100, 30, 'small', red, light_green, action='toggle grid')

        button('Show Stats', black, dim[0] // 2 - 50, 150, 120, 30, 'small', red, light_green, action='show stats')

        button('Go Back', black, dim[0] // 2 - 50, 400, 100, 30, 'small', red, light_green, action='play')

        pygame.display.update()
    clock.tick(30)


def controls_page():
    controls = True
    gameDisplay.fill(light_yellow)
    while controls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    controls = False
                    start_screen()

        button('Use the pencil tool to draw the maze', black, dim[0] // 2, 100, 10, 10, 'medium', light_yellow,
               light_yellow)
        button('Use Set A and Set B to chose starting and ending point respectively', black, dim[0] // 2, 150, 10, 10,
               'medium', light_yellow, light_yellow)
        button('Select the algorithm you want to use!', black, dim[0] // 2, 200, 10, 10, 'medium', light_yellow,
               light_yellow)
        button('Go Back', black, dim[0] // 2 - 50, 250, 100, 30, 'small', green, light_green, action='starting_page')
        pygame.display.update()
    clock.tick(5)


def GameLoop():
    global current_tool
    global rect_coords
    GameExit = False

    while not GameExit:

        gameDisplay.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameExit = True
                pygame.quit()
                quit()

        if current_tool == 'pencil':
            button('Pencil', black, 30, 20, y_margin, 30, 'small', light_green, light_green, 'set_pencil')
        else:
            button('Pencil', black, 30, 20, y_margin, 30, 'small', red, light_green, 'set_pencil')
        if current_tool == 'eraser':
            button('Eraser', black, 120, 20, y_margin, 30, 'small', light_green, light_green, 'set_eraser')
        else:
            button('Eraser', black, 120, 20, y_margin, 30, 'small', red, light_green, 'set_eraser')

        button('Clear', black, 210, 20, y_margin, 30, 'small', red, light_green, 'set_clear')

        if current_tool == 'setA':
            button('Set A', black, 300, 20, y_margin, 30, 'small', light_green, light_green, 'set_A')
        else:
            button('Set A', black, 300, 20, y_margin, 30, 'small', red, light_green, 'set_A')

        if current_tool == 'setB':
            button('Set B', black, 390, 20, y_margin, 30, 'small', light_green, light_green, 'set_B')
        else:
            button('Set B', black, 390, 20, y_margin, 30, 'small', red, light_green, 'set_B')

        button('DFS', black, 480, 20, y_margin, 30, 'small', red, light_green, action='solve DFS')

        button('BFS', black, 570, 20, y_margin, 30, 'small', red, light_green, action='solve BFS')

        button('A*', black, 660, 20, y_margin, 30, 'small', red, light_green, action='smart solve')

        button('Options', black, 750, 20, y_margin + 10, 30, 'small', red, light_green, 'options')

        # button('Maze', black, 840, 20, y_margin, 30,'small', red,light_green,'maze' )

        button('Quit', black, 900, 20, y_margin, 30, 'small', red, light_green, 'quit')

        if current_tool == 'pencil':
            pencil_tool()
        elif current_tool == 'eraser':
            eraser_tool()
        elif current_tool == 'clear':
            clear_tool()
        elif current_tool == 'setA':
            set_A_tool()
        elif current_tool == 'setB':
            set_B_tool()
        elif current_tool == 'solve BFS':
            print_solution('BFS')
        elif current_tool == 'solve DFS':
            print_solution('DFS')
        elif current_tool == 'smart solve':
            print_smart_solution()

            # print(len(explored_coords))
        # print(current_tool)
        # print(rect_coords)

        if is_grid:
            for i in range(y_margin, dim[1] + 1, box_size):
                pygame.draw.line(gameDisplay, black, (0, i), (dim[0], i))
            for j in range(0, dim[0] + 1, box_size):
                pygame.draw.line(gameDisplay, black, (j, y_margin), (j, dim[1]))

        if no_solution:
            button('No Solution!', black, dim[0] - 120, dim[1] - 30, 120, 30, 'small', red, red, )

        pygame.draw.line(gameDisplay, black, (0, y_margin), (dim[0], y_margin))

        pygame.display.update()
        clock.tick(fps)


start_screen()
pygame.quit()
quit()
