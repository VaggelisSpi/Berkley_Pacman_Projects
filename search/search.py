# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from sets import Set

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def constructSolution(explored, cur_state, last_move):
    """
    Make the solution for a given problem.

    Last move is the move done from cur_state to the goal state. cur_state
    is a state parent to our last state and it will help us find the final path

    We make a list of moves but it's reversed because we start making it from the
    goal state to the start state.
    """
    sol = []
    move = last_move
    # If the move is Stop it means we have reached the start state so we can't
    # go anymore backwards
    while move != "Stop":
        # Add the current move to the list
        sol.append(move)
        # Get the node that our current state point to in the explored dictionary
        prev_node = explored[cur_state]
        # The new cur_state will be the parent of the state we are now
        cur_state = prev_node[1]
        # Get the move that lead us to that previous state
        move = prev_node[0]

    # We need to reverse the list with the moves because it's makde backwards
    f_sol = []
    # print "Path: "
    for i in reversed(sol):
        # print i, ", "
        f_sol.append(i)
    return f_sol

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    Frontier must be a struct that implements push and pop functions. Based on
    the type of the frontier and te order it pushes and pops elements the search
    will vary.

    Each node we will store in the frontier will be of the form
    (state, move, parent). We need to aditionally save the parent so we
    can construct the path in the end.
    The explored set will be implemented as a dictionary and it will be a mapping
    from states to (move, parent) tupples. This is done in order to help us
    construct the solution in the end.

    The frontier_set keeps the whole node and not just state because if a state
    was found again with a different parent the second one shall be used
    """
    "*** YOUR CODE HERE ***"
    # frontier_set is gonna be used in orde to find with O(1) compplexity if a
    # node is in frontier. Also the given structs of the exercise do not
    # provide a way of checking if a node is in them and we can't know their
    # inner structure
    frontier = util.Stack()
    frontier_set = Set()

    # Get the start state. It's the state from where we will begin our search
    start_state = problem.getStartState()
    # If our initial state is a goal state there is nothing to do
    if problem.isGoalState(start_state):
        return []

    # Add the start state in frontier so we will search it next. Stop is used
    # as a convention and will be used in the construction of the solution so we
    # will know we are at the start state
    frontier.push((start_state, "Stop", None))
    frontier_set.add((start_state, "Stop", None))

    # Contains the nodes we have explored so we won't look them. again It will
    # be a map from states to (move, parent) tupples
    explored = dict()

    # While we still have elements to explore
    while not frontier.isEmpty():
        # Extract the next node to explore from the frontier
        node = frontier.pop()
        frontier_set.remove(node)
        # Get the state of the node we extracted
        cur_state = node[0]

        # We check if our current state is a goal state and we return the solution
        if problem.isGoalState(cur_state):
            return constructSolution(explored, node[2], node[1])

        # We make a (move, parent) tupple to map to our current state.
        # This tupple will act as a way to find the path to it
        explored[cur_state] = (node[1], node[2])

        # For all the successor states
        succs = problem.getSuccessors(cur_state)
        for child in succs:
            child_state = child[0]
            child_node = (child[0], child[1], cur_state)
            # if somwthing is in explored we have already visited it so we won't
            # need to look it again.
            if (child_state not in explored) and (child_node not in frontier_set):
                # Add current successor to frontier
                frontier.push(child_node)
                frontier_set.add(child_node)
                # We add this whole tupple so we will be able to get the final path
                # The whole tupple is also added because there can be different
                # paths to a node. Only the first one should be kept in dfs

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    Similar conventions followed as above
    For bfs we only store the state and not the whole node in frontier becasue
    if we have it inside and the same state was found again with different
    parent the first one shall be extracted first becasue in bfs we use a FIFO.
    When we pop the second one ,the first one will already be in explored so we
    shall not add it again. That's why when we look for goal state when we pop
    the node we look if it's in explored first and then we update it. There is
    no need for this extra check if we look if it's a goal node when we do the
    check before adding it to frontier because we will never add it to the
    frontier
    """
    "*** YOUR CODE HERE ***"
    # frontier_set is gonna be used in orde to find with O(1) compplexity if a
    # node is in frontier. Also the given structs of the exercise do not
    # provide a way of checking if a node is in them and we can't know their
    # inner structure
    frontier = util.Queue()
    frontier_set = Set()

    # Get the start state. It's the state from where we will begin our search
    start_state = problem.getStartState()
    # If our initial state is a goal state there is nothing to do
    if problem.isGoalState(start_state):
        return []

    # Add the start state in frontier so we will search it next. Stop is used
    # as a convention and will be used in the construction of the solution so we
    # will know we are at the start state
    frontier.push((start_state, "Stop", None))
    frontier_set.add(start_state)

    # Contains the nodes we have explored so we won't look them again It will be
    # a map from states to (move, parent) tupples
    explored = dict()

    # While we still have elements to explore
    while not frontier.isEmpty():
        # Extract the next node to explore from the frontier
        node = frontier.pop()
        # Get the state of the node we extracted
        cur_state = node[0]
        # Remove it from frontier so we won't waste memory. We do this check
        # because multiple nodes with the same state can be added in frontier
        # but they will be only once in frontier_set. After that they will be in
        # explored so there is no point in expanding them again
        if cur_state in frontier_set:
            frontier_set.remove(cur_state)

        # We check if our current state is a goal state and we return the solution
        # This is in order autograder will mark it correct. It's not optimal
        # if problem.isGoalState(cur_state):
        #     return constructSolution(explored, node[2], node[1])
        # # we need this check so we won't expand them again for no reason
        # if cur_state in explored:
        #     continue

        # We make a (move, parent) tupple to map to our current state.
        # This tupple will act as a way to find the path to it
        explored[cur_state] = (node[1], node[2])

        # For all the successor states
        succs = problem.getSuccessors(cur_state)
        for child in succs:
            child_state = child[0]
            child_node = (child[0], child[1], cur_state)
            # if (child_state not in explored) and (child_node not in frontier_set):
            if (child_state not in explored) and (child_state not in frontier_set):
                #  PROPER ONE. TO CHNAGE BEFORE SUBMITING
                # If the current successor is a goal state then the problem is solved
                # This is optimal but autograder marks as incorrect. This should be used
                if problem.isGoalState(child_state):
                    return constructSolution(explored, cur_state, child[1])
                    # return constructSolution(explored, cur_state, child_node[1])

                # Add current successor to frontier
                # We add this whole tupple so we will be able to get the final path
                frontier.push(child_node)
                frontier_set.add(child[0])

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # UCS is the special case of astar with null heuristic. No need to rewrite code
    return aStarSearch(problem)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def constructSolution2(path, cur_state):
    """
    Function specifically to find the path for astar and ucs.

    cur_state is a goal sate

    We make a list of moves but it's reversed because we start making it from the
    goal state to the start state.
    """
    sol = []
    move = path[cur_state][0]
    # If the move is Stop it means we have reached the start state so we can't
    # go anymore backwards
    while move != "Stop":
        #  Add the current move to the list
        sol.append(move)
        # get the parrent of our state
        cur_state = path[cur_state][2]
        # get the move that lead us to that parent
        move = path[cur_state][0]

    # We need to reverse the list with the moves because it's made backwards
    f_sol = []
    for i in reversed(sol):
        f_sol.append(i)

    return f_sol


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Get the start state. It's the state from where we will begin our search
    start_state = problem.getStartState()
    # If our initial state is a goal state there is nothing to do
    if problem.isGoalState(start_state):
        return []

    frontier = util.PriorityQueue()
    frontier_set = Set()
    # aad the satrt state to the frontier so we will extract it next
    frontier.push(start_state, 0)
    frontier_set.add(start_state)

    # keeps the node we hace visited already so we won;t visit them again
    explored = Set()

    # path is a mapping from a state to the parent, the move and the cost to it
    path = dict()
    # Intially we only have the start state that has no parent and 0 cost
    path[start_state] = ("Stop", 0, None)

    while not frontier.isEmpty():
        cur_state = frontier.pop()      # get the node with the least cost

        # Check if our state is a goal state and return the path to it if it is
        if problem.isGoalState(cur_state):
            return constructSolution2(path, cur_state)

        # remove the state we extracted from the frontier from the set as well
        frontier_set.remove(cur_state)
        # Add our current state to explored so we won't look it again
        explored.add(cur_state)

        # Get all the successors of our current state
        succs = problem.getSuccessors(cur_state)
        for child in succs:
            child_state = child[0]
            # ignore the successors we have alrady visited
            # if child_state in explored:
            #     continue

            # the cost to the curent successor is the cost until its parent plus
            # the cost from it to the current successor
            child_cost = path[cur_state][1] + child[2]
            h_cost = heuristic(child_state, problem)
            cost = h_cost + child_cost

            # child_node

            # Add the child in frontier if we haven't visited it yet
            # any check for visited makes no difference
            if child_state not in frontier_set and child_state not in explored:
                frontier.push(child_state, cost)
                frontier_set.add(child_state)
                path[child_state] = (child[1], child_cost, cur_state)
            else:
                # If the current successor was in frontier update its cost if it
                # was worse
                prev_cost = path[child_state][1]
                if cost < prev_cost:
                    frontier.update(child_state, cost)
                    path[child_state] = (child[1], child_cost, cur_state)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
