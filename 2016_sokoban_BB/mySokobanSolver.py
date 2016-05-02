from cab320_search import iterative_deepening_search, Problem, ida_star_search_elementary,\
    astar_search, ida_star_search, iterative_deepening_search, ida_star_search_limited

import cab320_sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SokobanPuzzle(Problem):
    """
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the module  cab320_search
    """

    def __init__(self, puzzleFileName):
        self.warehouse = cab320_sokoban.Warehouse()
        self.warehouse.read_warehouse_file(puzzleFileName)
        self.goal = self.getGoalState()
        # Extract worker and box locations for initial state tuple
        initial = list(self.warehouse.boxes)
        # Worker at 0 tuple pos
        initial.insert(0, self.warehouse.worker)
        self.initial = tuple(initial)
        self.taboo = self.getTabooCells()

    def goal_test(self, state):
        """
        Checks whether the current box positions are on the targets
        :param state: current state of warehouse, first tuple is the worker
        :return: boolean
        """
        state = list(state)
        del state[0]  # Remove the worker, only need to check boxes
        for box in state:
            if box not in self.warehouse.targets:
                return False
        return True

    def actions(self, state):
        """
        State is a tuple of tuples where the first element is the worker.
        Preceding elements represent boxes.
        :param state:
        :return: actions list of legal actions from the current state
        """
        state = list(state)
        actions = list()

        # Worker positions to check
        (w_x, w_y) = state.pop(0)
        w_x_left = w_x - 1
        w_x_right = w_x + 1
        w_y_up = w_y - 1
        w_y_down = w_y + 1

        # check if left move is legal
        if (w_x_left, w_y) not in self.warehouse.walls:  # no walls
            if (w_x_left, w_y) in state:  # box in new position?
                (b_x, b_y) = (w_x_left, w_y)
                b_x_left = b_x - 1
                if (b_x_left, b_y) not in self.warehouse.walls and (b_x_left, b_y) not in state\
                        and (b_x_left, b_y) not in self.taboo:  # box not pushed in taboo/wall/another_box
                    actions.append('Left')
            else:
                actions.append('Left')
        if (w_x_right, w_y) not in self.warehouse.walls:
            if (w_x_right, w_y) in state:
                (b_x, b_y) = (w_x_right, w_y)
                b_x_right = b_x + 1
                if (b_x_right, b_y) not in self.warehouse.walls and (b_x_right, b_y) not in state\
                        and (b_x_right, b_y) not in self.taboo:
                    actions.append('Right')
            else:
                actions.append('Right')
        if (w_x, w_y_down) not in self.warehouse.walls:
            if (w_x, w_y_down) in state:
                (b_x, b_y) = (w_x, w_y_down)
                b_y_down = b_y + 1
                if (b_x, b_y_down) not in self.warehouse.walls and (b_x, b_y_down) not in state\
                        and (b_x, b_y_down) not in self.taboo:
                    actions.append('Down')
            else:
                actions.append('Down')
        if (w_x, w_y_up) not in self.warehouse.walls:
            if (w_x, w_y_up) in state:
                (b_x, b_y) = (w_x, w_y_up)
                b_y_up = b_y - 1
                if (b_x, b_y_up) not in self.warehouse.walls and (b_x, b_y_up) not in state\
                        and (b_x, b_y_up) not in self.taboo:
                    actions.append('Up')
            else:
                actions.append('Up')

        return actions

    def result(self, state, action):
        # convert state to list, separate worker form boxes
        state = list(state)
        (w_x, w_y) = state.pop(0)  # Pop out the worker

        if action == 'Left':
            w_x1 = w_x - 1
            if (w_x1, w_y) in state:
                (b_x, b_y) = (w_x1, w_y)
                state[state.index((b_x, b_y))] = (b_x - 1, b_y)  # Move pushed box left
            state.insert(0, (w_x1, w_y))

        elif action == 'Right':
            w_x1 = w_x + 1
            if (w_x1, w_y) in state:
                (b_x, b_y) = (w_x1, w_y)
                state[state.index((b_x, b_y))] = (b_x + 1, b_y)  # Move pushed box right
            state.insert(0, (w_x1, w_y))
        elif action == 'Down':
            w_y1 = w_y + 1
            if (w_x, w_y1) in state:
                (b_x, b_y) = (w_x, w_y1)
                state[state.index((b_x, b_y))] = (b_x, b_y + 1)  # Move pushed box left
            state.insert(0, (w_x, w_y1))

        elif action == 'Up':
            w_y1 = w_y - 1
            if (w_x, w_y1) in state:
                (b_x, b_y) = (w_x, w_y1)
                state[state.index((b_x, b_y))] = (b_x, b_y - 1)  # Move pushed box left
            state.insert(0, (w_x, w_y1))
        elif isinstance(action, list):  # We have a macro action
            print "macro action detected" # @TODO Macro action
        return tuple(state)

    def getGoalState(self):
        #
        goalState = self.warehouse.visualize()
        goalState = goalState.replace("$", " ").replace(".", "*").replace("@", " ")
        return goalState

    def getTabooCells(self):
        walls_y = [b for (a,b) in self.warehouse.walls]
        walls_x = [a for (a,b) in self.warehouse.walls]

        walls_x_start = min(walls_x)
        walls_x_end = max(walls_x)

        wall_y_start = min(walls_y)
        wall_y_end = max(walls_y)
        
        taboo = list()

        for row in xrange(wall_y_start + 1, wall_y_end):

            # get the walls above, below and on the current row
            row_above_walls = [a for (a,b) in self.warehouse.walls if b == row - 1]
            row_below_walls = [a for (a,b) in self.warehouse.walls if b == row + 1]
            row_current_walls = [a for (a,b) in self.warehouse.walls if b == row]

            # determine which pos can be accessed by boxes
            accessible_cells = list()

            # determine accessible warehouse positions
            for pos in xrange(row_current_walls[0],row_current_walls[-1] + 1):
                if pos not in row_current_walls:
                    if accessible_cells:  # not empty list
                        if (accessible_cells[-1] != '*') and ((pos - accessible_cells[-1]) != 1):
                            accessible_cells.append('*')
                        accessible_cells.append(pos)
                    else:
                        accessible_cells.append(pos)

            # process the accessible cells sub lists of continuous accessible cells
            accessible_segments = [[]]
            segment = 0

            for cell in accessible_cells:
                if cell == '*':
                    accessible_segments.append([])
                    segment += 1
                else:
                    accessible_segments[segment].append(cell)

            # check if any of the segments are empty, this is bad
            for segment in accessible_segments:
                if not segment:
                    raise ValueError("accessible segment is empty")

            # Begin determining taboo cells
            # Check if the cells are bounded by a U shape
            for segment in accessible_segments:
                bounded_upper_wall = True
                bounded_lower_wall = True
                target_in_segment = False  # Check if there is a target in segment
                for pos in segment:
                    if pos not in row_above_walls:
                        bounded_upper_wall = False
                    if pos not in row_below_walls:
                        bounded_lower_wall = False
                    if (pos, row) in self.warehouse.targets:  # target in segment, don't taboo it
                        target_in_segment = True

                if (bounded_upper_wall or bounded_lower_wall) and not target_in_segment:
                    for pos in segment:
                        taboo.append((pos, row))
                else:
                    for pos in segment:
                        if ((pos - 1) in row_current_walls or (pos + 1) in row_current_walls) and (pos in
                        row_below_walls or pos in row_above_walls):
                            taboo.append((pos, row))

        for col in xrange(walls_x_start + 1, walls_x_end):
            row_left_walls = [b for (a,b) in self.warehouse.walls if a == col - 1]
            row_right_walls = [b for (a,b) in self.warehouse.walls if a == col + 1]
            row_current_walls = [b for (a,b) in self.warehouse.walls if a == col]

            # determine which pos can be accessed by boxes
            accessible_cells = list()

            # determine accessible warehouse positions (y position)
            for pos in xrange(row_current_walls[0],row_current_walls[-1] + 1):
                if pos not in row_current_walls:
                    if accessible_cells:  # not empty list
                        if (accessible_cells[-1] != '*') and ((pos - accessible_cells[-1]) != 1):
                            accessible_cells.append('*')
                        accessible_cells.append(pos)
                    else:
                        accessible_cells.append(pos)

            # process the accessible cells sub lists of continuous accessible cells
            accessible_segments = [[]]
            segment = 0

            for cell in accessible_cells:
                if cell == '*':
                    accessible_segments.append([])
                    segment += 1
                else:
                    accessible_segments[segment].append(cell)

            # check if any of the segments are empty, this is bad
            for segment in accessible_segments:
                if not segment:
                    raise ValueError("accessible segment is empty")

            # Begin determining taboo cells
            # Check if the cells are bounded by a U shape
            for segment in accessible_segments:
                bounded_left_wall = True
                bounded_right_wall = True
                target_in_segment = False  # Check if there is a target in segment
                for pos in segment:
                    if pos not in row_left_walls:
                        bounded_left_wall = False
                    if pos not in row_right_walls:
                        bounded_right_wall = False
                    if (col, pos) in self.warehouse.targets:  # target in segment, don't taboo it
                        target_in_segment = True

                if (bounded_left_wall or bounded_right_wall) and not target_in_segment:
                    for pos in segment:
                        taboo.append((col, pos))
                else:
                    for pos in segment:
                        if ((pos - 1) in row_current_walls or (pos + 1) in row_current_walls) and (pos in
                        row_left_walls or pos in row_right_walls):
                            taboo.append((col, pos))

            taboo_with_targets = [t for t in taboo if t not in self.warehouse.targets]

        return taboo_with_targets

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def print_solution(self, goal_node):
        actions = []
        if goal_node == None:
            print "No solution found"
        elif goal_node == 'cuttoff':
            print "cuttoff"
        else:
            # path is list of nodes from initial state (root of the tree)
            # to the goal_node
            path = goal_node.path()
            # print the solution
            print "Solution takes {0} steps from the initial state".format(len(path)-1)
            print path[0].state
            print "to the goal state"
            print path[-1].state
            print "\nBelow is the sequence of moves\n"
            for node in path:
                if node.action is not None:
                    print "{0}".format(node.action)
                # print node.state, " path_cost: ", node.path_cost
                    actions.append(node.action)
            return actions

    def __dead_state__(self, (new_b_x, new_b_y), state):
        """
        Check if pushing a box, will lead to it being adjacent to another box.
        Rendering both boxes immovable.
        :param state:
        :return:
        """

    def h(self, node):
        """
        Manhattan distances for boxes to targets
        :param node:
        :return:
        """

        state = list(node.state)
        state.pop(0)  # remove the worker
        dist = 0

        for i in xrange(len(state)):
            dist_each_box = []
            if state[i] not in self.warehouse.targets:
                for j in xrange(len(self.warehouse.targets)):
                    b_x, b_y = state[i]
                    t_x, t_y = self.warehouse.targets[j]
                    dist_to_box = abs(b_x - t_x) + abs(b_y - t_y)
                    dist_each_box.append(dist_to_box)
                dist += min(dist_each_box)
        return dist


class SokobanPuzzleMacro(SokobanPuzzle):

    # def __get_adjacent_box__(self, w_x, w_y, state_of_boxes):
    #     for b_x, b_y in state_of_boxes:
    #         if w_x == b_x:
    #             if abs(w_y - b_y) == 1:
    #                 # the box is adjacent to the worker (either above or below)
    #                 return b_x, b_y
    #         if w_y == b_y:
    #             if abs(w_x - b_x) == 1:
    #                 # the box is adjacent to the worker (left or right)
    #                 return b_x, b_y

    def worker_adjacent_to_move_able_box(self, worker, state_of_boxes):
        """
        Is the worker near a moveable box?
            If so, don't need to perform a macro action
        Else
            Need to get in position to a moveable box
        :param worker: worker coords
        :param state_of_boxes: coordinates of all boxes
        :return True or False
        """
        w_x, w_y = worker
        w_x_left = w_x - 1
        w_x_right = w_x + 1
        w_y_up = w_y - 1
        w_y_down = w_y + 1

        # left of worker has a box
        if (w_x_left, w_y) in state_of_boxes:
            # check if that box can be moved
            b_x_left = w_x_left - 1
            b_y = w_y
            if (b_x_left, b_y) not in self.warehouse.walls and (b_x_left, b_y) not in state_of_boxes\
                    and (b_x_left, b_y) not in self.taboo:
                return True
        if (w_x_right, w_y) in state_of_boxes:
            # check if that box can be moved
            b_x_right = w_x_right + 1
            b_y = w_y
            if (b_x_right, b_y) not in self.warehouse.walls and (b_x_right, b_y) not in state_of_boxes\
                    and (b_x_right, b_y) not in self.taboo:
                return True
        if (w_x, w_y_up) in state_of_boxes:
            # check if that box can be moved
            b_x = w_x
            b_y_up = w_y_up - 1
            if (b_x, b_y_up) not in self.warehouse.walls and (b_x, b_y_up) not in state_of_boxes\
                    and (b_x, b_y_up) not in self.taboo:
                return True
        if (w_x, w_y_down) in state_of_boxes:
            # check if that box can be moved
            b_x = w_x
            b_y_down = w_y_down + 1
            if (b_x, b_y_down) not in self.warehouse.walls and (b_x, b_y_down) not in state_of_boxes\
                    and (b_x, b_y_down) not in self.taboo:
                return True
        return False

    def get_macro_end_points(self, (b_x, b_y), (w_x, w_y), state):
        """

        :param state:
        :param (b_x, b_y): coords of a moveable box
        :return: list of coords for a worker to move to in order to start moving this box
        """
        b_x_left = b_x - 1
        b_x_right = b_x + 1
        b_y_up = b_y - 1
        b_y_down = b_y + 1

        macro_end_point = list()
        # No walls or boxes on the left or right of the box of interest
        if (b_x_left, b_y) not in self.warehouse.walls and (b_x_left, b_y) not in state\
                and (b_x_right, b_y) not in self.warehouse.walls and (b_x_right, b_y) not in state:

            # if the worker is already next to the box, we don't need a macro action
            if (b_x_left, b_y) != (w_x, w_y):

                # will pushing it right lead to anything?
                if (b_x_right, b_y) not in self.taboo:
                    macro_end_point.append((b_x_left, b_y))  # left of the box

            if (b_x_right, b_y) != (w_x, w_y):

                # will pushing it left, lead to taboo cells etc?
                if (b_x_left, b_y) not in self.taboo:
                    macro_end_point.append((b_x_right, b_y))

        if (b_x, b_y_up) not in self.warehouse.walls and (b_x, b_y_up) not in state\
                and (b_x, b_y_down) not in self.warehouse.walls and (b_x, b_y_down) not in state:

                # if the worker is already next to box, don't need a macro action...
                if (b_x, b_y_up) != (w_x, w_y):

                    # will pushing it down, lead to taboo cell etc?
                    if (b_x, b_y_down) not in self.taboo:
                        macro_end_point.append((b_x, b_y_up))
                if (b_x, b_y_down) != (w_x, w_y):

                    if (b_x, b_y_up) not in self.taboo:
                        macro_end_point.append((b_x, b_y_down))
        return macro_end_point

    def worker_to_macro_end_point(self, macro_end_point, worker, state):
        """
        Solves a sub problem, using astar

        :param state: current state of the warehouse
        :return: list of actions
        """
        pass

    def actions(self, state):
        """
        Case 1: worker is adjacent to a moveable box, this will result in a normal action
        Case 2: worker is not adjacent to a moveable box, this will result in a macro action
        :param state:
        :return:
        """
        state = list(state)
        actions = list()

        w_x, w_y = state.pop(0)
        w_x_left = w_x - 1
        w_x_right = w_x + 1
        w_y_up = w_y - 1
        w_y_down = w_y + 1

        require_macro_action = self.worker_adjacent_to_move_able_box((w_x, w_y), state)

        if require_macro_action:
            pass
        else:
            pass

    def result(self, state, action):
        pass

    def sub_problem_actions(self, node):
        """
        Given the solution of a sub problem, return a list of "Macro" actions
        :param node:
        :return:
        """
        actions = []
        if node is None:
            return None
        else:
            # path is list of nodes from initial state (root of the tree)
            # to the goal_node
            path = node.path()
            # print the solution
            for node in path:
                if node.action is not None:
                    actions.append(node.action)
            return actions


class ShortestPath(Problem):
    """
    Sub Problem class of the Sokoban puzzle
    Shortest path between a worker and a target location (macro action end point)
    """

    def __init__(self, worker, walls, boxes, target_location):
        """
        
        :param worker: 
        :param walls: 
        :param boxes: 
        :param target_location: 
        :return: 
        """
        self.initial = worker
        self.walls = walls
        self.boxes = boxes
        self.target_location = target_location


    def actions(self, state):
        """
        :param state: tuple of worker coords (w_x, w_y)
        :return actions: list of legal actions for the worker
        """

        actions = list()

        (w_x, w_y) = state  # get worker coords
        w_x_left = w_x - 1
        w_x_right = w_x + 1
        w_y_up = w_y - 1
        w_y_down = w_y + 1
        
        # check if left move is legal
        if (w_x_left, w_y) not in self.walls and (w_x_left, w_y) not in self.boxes:  # no walls and boxes
                actions.append('Left')
        if (w_x_right, w_y) not in self.walls and (w_x_right, w_y) not in self.boxes:
                actions.append('Right')
        if (w_x, w_y_down) not in self.walls and (w_x, w_y_down) not in self.boxes:
                actions.append('Down')
        if (w_x, w_y_up) not in self.walls and (w_x, w_y_up) not in self.boxes:
                actions.append('Up')
        return actions

    def result(self, state, action):
        """

        :param state:
        :param action:
        :return:
        """

        (w_x, w_y) = state
        if action == 'Left':
            return w_x - 1, w_y
        elif action == 'Right':
            return w_x + 1, w_y
        elif action == 'Up':
            return w_x, w_y - 1
        elif action == 'Down':
            return w_x, w_y + 1
        else:
            raise ValueError("Invalid action given")

    def goal_test(self, state):
        return state == self.target_location

    def h(self, node):
        """
        Manhattan distance
        :param node:
        :return:
        """
        (w_x, w_y) = node.state
        (t_x, t_y) = self.target_location
        dist = abs(w_x - t_x) + abs(w_y - t_y)
        return dist


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def checkActions(puzzleFileName, actionSequence):
        """
        This is a function called by the automatic marker.

        Your implementation should load a Sokoban puzzle from a text file,
        then try to apply the sequence of actions listed in actionSequence.

        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @param actionSequence: a sequence of actions.
               For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
        @return:
            The string 'Failure', if one of the move was not successul.
               For example, if the agent tries to push two boxes,
                            or push into to push into a wall.
            Otherwise, if all moves were successful return                 
                   A string representing the state of the puzzle after applying
                   the sequence of actions.  This should be the same string as the
                   string returned by the method  WarehouseHowever.visualize()
        """

        soko = SokobanPuzzle(puzzleFileName)
        boxes = list(soko.warehouse.boxes)
        w_x, w_y = soko.warehouse.worker
        walls = soko.warehouse.walls

        for action in actionSequence:
            w_x0, w_y0 = w_x, w_y
            if action is "Left":
                # Check what is to the "Left"
                w_x1 = w_x0 - 1
                # check if wall is in the way
                if (w_x1, w_y0) in walls:
                    return "Failure"
                elif (w_x1, w_y0) in boxes:
                    s_x0, s_y0 = w_x1, w_y0
                    s_x1 = s_x0 - 1
                    if (s_x1, s_y0) in walls or (s_x1, s_y0) in boxes:
                        return "Failure"
                    else:
                        w_x = w_x1
                        boxes[boxes.index((s_x0, s_y0))] = (s_x1, s_y0)
                else:
                        w_x = w_x1
            elif action is "Right":
                # Check what is to the "Left"
                w_x1 = w_x0 + 1

                # check if wall is in the way
                if (w_x1, w_y0) in walls:
                    return "Failure"
                elif (w_x1, w_y0) in boxes:
                    s_x0, s_y0 = w_x1, w_y0
                    s_x1 = s_x0 + 1
                    if (s_x1, s_y0) in walls or (s_x1, s_y0) in boxes:
                        return "Failure"
                    else:
                        w_x = w_x1
                        boxes[boxes.index((s_x0, s_y0))] = (s_x1, s_y0)
                else:
                    w_x = w_x1

                # print soko.warehouse.visualize()
            elif action is "Down":
                # Check what is to the "Left"
                w_y1 = w_y0 + 1

                # check if wall is in the way
                if (w_x0, w_y1) in walls:
                    return "Failure"
                elif (w_x0, w_y1) in boxes:
                    s_x0, s_y0 = w_x0, w_y1
                    s_y1 = s_y0 + 1
                    if (s_x0, s_y1) in walls or (s_x0, s_y1) in boxes:
                        return "Failure"
                    else:
                        w_y = w_y1
                        boxes[boxes.index((s_x0, s_y0))] = (s_x0, s_y1)

                else:
                    w_y = w_y1


                # print soko.warehouse.visualize()
            elif action is "Up":
                w_y1 = w_y0 - 1
                if (w_x0, w_y1) in walls:
                    return "Failure"
                elif (w_x0, w_y1) in boxes:
                    s_x0, s_y0 = w_x0, w_y1
                    s_y1 = s_y0 - 1
                    if (s_x0, s_y1) in walls or (s_x0, s_y1) in boxes:
                        return "Failure"
                    else:
                        w_y = w_y1
                        boxes[boxes.index((s_x0, s_y0))] = (s_x0, s_y1)
                else:
                    w_y = w_y1
            else:
                raise ValueError("Invalid action given")
        soko.warehouse.worker = (w_x, w_y)
        soko.warehouse.boxes = boxes
        return soko.warehouse.visualize()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def tabooCells(puzzleFileName):
        """
        This is a function called by the automatic marker.

        Your implementation should load a Sokoban puzzle from a text file,
        then identify the cells that should be avoided in the sense that if
        a box get pushed on such a cell then the puzzle becomes unsolvable.

        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @return:
                   A string representing the puzzle with the taboo cells marked with an 'X'.
                   Apart from the 'X's, the string should follows the same format as the
                   string returned by the method  Warehouse.visualize()
        """
        s = SokobanPuzzle(puzzleFileName)
        walls_y = [b for (a,b) in s.warehouse.walls]
        walls_x = [a for (a,b) in s.warehouse.walls]

        walls_x_start = min(walls_x)
        walls_x_end = max(walls_x)

        wall_y_start = min(walls_y)
        wall_y_end = max(walls_y)
        taboo = list()

        for row in xrange(wall_y_start + 1, wall_y_end):

            # get the walls above, below and on the current row
            row_above_walls = [a for (a,b) in s.warehouse.walls if b == row - 1]
            row_below_walls = [a for (a,b) in s.warehouse.walls if b == row + 1]
            row_current_walls = [a for (a,b) in s.warehouse.walls if b == row]

            # determine which pos can be accessed by boxes
            accessible_cells = list()

            # determine accessible warehouse positions (x position)
            for pos in xrange(row_current_walls[0],row_current_walls[-1] + 1):
                if pos not in row_current_walls:
                    if accessible_cells:  # not empty list
                        if (accessible_cells[-1] != '*') and ((pos - accessible_cells[-1]) != 1):
                            accessible_cells.append('*')
                        accessible_cells.append(pos)
                    else:
                        accessible_cells.append(pos)

            # process the accessible cells sub lists of continuous accessible cells
            accessible_segments = [[]]
            segment = 0

            for cell in accessible_cells:
                if cell == '*':
                    accessible_segments.append([])
                    segment += 1
                else:
                    accessible_segments[segment].append(cell)

            # check if any of the segments are empty, this is bad
            for segment in accessible_segments:
                if not segment:
                    raise ValueError("accessible segment is empty")

            # Begin determining taboo cells
            # Check if the cells are bounded by a U shape
            for segment in accessible_segments:
                bounded_upper_wall = True
                bounded_lower_wall = True
                target_in_segment = False  # Check if there is a target in segment
                for pos in segment:
                    if pos not in row_above_walls:
                        bounded_upper_wall = False
                    if pos not in row_below_walls:
                        bounded_lower_wall = False
                    if (pos, row) in s.warehouse.targets:  # target in segment, don't taboo it
                        target_in_segment = True

                if (bounded_upper_wall or bounded_lower_wall) and not target_in_segment:
                    for pos in segment:
                        taboo.append((pos, row))
                else:
                    for pos in segment:
                        if ((pos - 1) in row_current_walls or (pos + 1) in row_current_walls) and (pos in
                        row_below_walls or pos in row_above_walls):
                            taboo.append((pos, row))

        for col in xrange(walls_x_start + 1, walls_x_end):
            row_left_walls = [b for (a,b) in s.warehouse.walls if a == col - 1]
            row_right_walls = [b for (a,b) in s.warehouse.walls if a == col + 1]
            row_current_walls = [b for (a,b) in s.warehouse.walls if a == col]

            # determine which pos can be accessed by boxes
            accessible_cells = list()

            # determine accessible warehouse positions (y position)
            for pos in xrange(row_current_walls[0],row_current_walls[-1] + 1):
                if pos not in row_current_walls:
                    if accessible_cells:  # not empty list
                        if (accessible_cells[-1] != '*') and ((pos - accessible_cells[-1]) != 1):
                            accessible_cells.append('*')
                        accessible_cells.append(pos)
                    else:
                        accessible_cells.append(pos)

            # process the accessible cells sub lists of continuous accessible cells
            accessible_segments = [[]]
            segment = 0

            for cell in accessible_cells:
                if cell == '*':
                    accessible_segments.append([])
                    segment += 1
                else:
                    accessible_segments[segment].append(cell)

            # check if any of the segments are empty, this is bad
            for segment in accessible_segments:
                if not segment:
                    raise ValueError("accessible segment is empty")

             # Begin determining taboo cells
            # Check if the cells are bounded by a U shape
            for segment in accessible_segments:
                bounded_left_wall = True
                bounded_right_wall = True
                target_in_segment = False  # Check if there is a target in segment
                for pos in segment:
                    if pos not in row_left_walls:
                        bounded_left_wall = False
                    if pos not in row_right_walls:
                        bounded_right_wall = False
                    if (col, pos) in s.warehouse.targets:  # target in segment, don't taboo it
                        target_in_segment = True

                if (bounded_left_wall or bounded_right_wall) and not target_in_segment:
                    for pos in segment:
                        taboo.append((col, pos))
                else:
                    for pos in segment:
                        if ((pos - 1) in row_current_walls or (pos + 1) in row_current_walls) and (pos in
                        row_left_walls or pos in row_right_walls):
                            taboo.append((col, pos))


        def visualize_taboo_cells(walls, targets, boxes, taboo):
            X,Y = zip(*walls)  # pythonic version of the above
            x_size, y_size = 1+max(X), 1+max(Y)

            vis = [[" "] * x_size for y in range(y_size)]
            for (x,y) in walls:
                vis[y][x] = "#"
            for (x,y) in targets:
                vis[y][x] = "."
            for (x,y) in taboo:
                vis[y][x] = "X"
            return "\n".join(["".join(line) for line in vis])
        taboo_with_targets = [t for t in taboo if t not in s.warehouse.targets]

        return visualize_taboo_cells(s.warehouse.walls, s.warehouse.targets, s.warehouse.boxes, taboo_with_targets)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solveSokoban_elementary(puzzleFileName, timeLimit = None):
        """
        This is a function called by the automatic marker.

        This function should solve the puzzle defined in a file.

        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @param timeLimit: The time limit for this agent in seconds .
        @return:
            A list of strings.
            If timeout return  ['Timeout']
            If puzzle cannot be solved return ['Impossible']
            If a solution was found, return a list of elementary actions that solves
                the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
                For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
                If the puzzle is already in a goal state, simply return []
        """
        soko_problem = SokobanPuzzle(puzzleFileName)

        answer = astar_search(soko_problem)
        return answer
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def testSolver(puzzleFileName):
    soko_problem = SokobanPuzzle(puzzleFileName)
    answer = iterative_deepening_search(soko_problem)
    return answer

def solveSokoban_macro(puzzleFileName, timeLimit = None):
        """
        This is a function called by the automatic marker.
        
        This function has the same purpose as 'solveSokoban_elementary', but 
        it should internally use macro actions as suggested 
        in the assignment description. Although it internally uses macro 
        actions, this function should return a sequence of 
        elementary  actions.


        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @param timeLimit: The time limit for this agent in seconds .
        @return:
            A list of strings.
            If timeout return  ['Timeout']
            If puzzle cannot be solved return ['Impossible']
            If a solution was found, return a list elementary actions that solves
                the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
                For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
                If the puzzle is already in a goal state, simply return []
        """

        raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  -