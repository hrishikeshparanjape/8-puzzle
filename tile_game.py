"""
8 Puzzle problem using A-star algorithm
Author: Hrishikesh Paranjape (Rishi)
Homework problem of Dr. Pollett's AI class
Date: 02/11/2012

Guideline followed from: "http://www.python.org/dev/peps/pep-0008/"

Guidelines followed for:
1. code lay-out
2. imports
3. Whitespace in Expressions and Statements
4. Comments

"""

#libraries to import
import sys
import math
import copy
import random

OPENLIST = []       #list to keep track of unexplored states
CLOSEDLIST = []     #list to keep track of already explored states

#parse the input file
def get_input():
    if (len(sys.argv)) !=2:
        print "supply enough arguments"
        raise SystemExit(1)
    f = open(sys.argv[1])
    lines = f.readlines()
    f.close()
    grid = []
    for i in range(len(lines)):
        grid.append(list(lines[i][:-1]))
    return grid

#find out goal state from the input
def get_goalstate(grid):
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            try:
                if (count < int(grid[i][j])):
                    count=int(grid[i][j])
            except:
                pass
    goal = []
    for i in range(len(grid)):
        row = ""
        for j in range(len(grid[i])):
            if ((i*len(grid[i]))+ (j+1) <= count ):
                row = row + str((i*len(grid[0]))+ (j+1))
            elif (grid[i][j]!='#'):
                row = row + '.'
            else:
                row = row + '#'
        goal.append(list(row))
    return goal

#Helper function for find_manhattan_distance
def distance_from_goal(i,j,elem,goalstate):
    for i1 in range(len(goalstate)):
        for j1 in range(len(goalstate[i])):
            if (elem == goalstate[i1][j1]):
                return int(math.fabs(i1-i) + math.fabs(j1-j))
            
#Find manhattan distance from current state and goal state
def find_manhattan_distance(state,goalstate):
    distance = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            try:
                int(state[i][j])
                distance = (distance + 
                    distance_from_goal(i,j,state[i][j],goalstate))
            except:
                pass
    return distance

#Find possible next states by movement of one of the empty tiles
#A tile can move up/down/left/right
def current_possible_states(state,i,j):
    nextstates = []
    try:
        if (state[i-1][j]!='#' and state[i-1][j]!='.' and i!=0):
            tempstate = copy.deepcopy(state)
            temptile = tempstate[i][j]
            tempstate[i][j] = tempstate[i-1][j]
            tempstate[i-1][j] = temptile
            nextstates.append(tempstate)
    except:
        pass
    try:
        if (state[i+1][j]!='#' and state[i+1][j]!='.'):
            tempstate = copy.deepcopy(state)
            temptile = tempstate[i][j]
            tempstate[i][j] = tempstate[i+1][j]
            tempstate[i+1][j] = temptile
            nextstates.append(tempstate)
    except:
        pass
    try:
        if (state[i][j-1]!='#' and state[i][j-1]!='.' and j!=0):
            tempstate = copy.deepcopy(state)
            temptile = tempstate[i][j]
            tempstate[i][j] = tempstate[i][j-1]
            tempstate[i][j-1] = temptile
            nextstates.append(tempstate)
    except:
        pass
    try:
        if (state[i][j+1]!='#' and state[i][j+1]!='.'):
            tempstate = copy.deepcopy(state)
            temptile = tempstate[i][j]
            tempstate[i][j] = tempstate[i][j+1]
            tempstate[i][j+1] = temptile
            nextstates.append(tempstate)
    except:
        pass
    return nextstates

# find all possible next moves from the current state
def find_possible_next_moves(state):
    all_possible_states = []
    for i in range(len(state)):
        for j in range(len(state[i])):
            current_states = []
            if (state[i][j] == "."):
                current_states = current_possible_states(state,i,j)
                for k in range(len(current_states)):
                    all_possible_states.append(current_states[k])
    return all_possible_states
           
#This is my try before googling the algorithm...pretty close
"""def solve_problem(prev, current, goal):
    if (current == goal):
        print "This is the goal state"
        raise SystemExit(1) 
    OPENLIST.append(current)
           
    possible_moves = find_possible_next_moves(current)
    current_manhatten_value = find_manhatten_distance(current,goal)
    distances = []
    for i in (range(len(possible_moves))):
        distances.append(find_manhatten_distance(possible_moves[i],goal))
    next_move = possible_moves[distances.index(min(distances))]
    if (next_move == prev):
        print "next move same as previous"
        print possible_moves
        print distances
        print [i for i, x in enumerate(distances) if x == min(distances)][1]
        #raise SystemExit(1)        
        next_move = possible_moves[[i \
            for i, x in enumerate(distances) if x != min(distances)][0]]
    print next_move
    solve_problem(current, next_move, goal)   
"""
def solve(goal):
    global OPENLIST
    global CLOSEDLIST

    while(True):
        if (len(OPENLIST)==0):
            print "Failed to solve this problem"
            return

        lowindex = 0
        low = OPENLIST[0]['f']
        for i in range(len(OPENLIST)):
            number = OPENLIST[i]['f']
            if (number<low):
                lowindex = i
                low = number
        n = OPENLIST[lowindex] # n is current state
        """
        # code block to print states explored

        for i in range(len(n['state'])):
            print ''.join(n['state'][i])
        print n
        """
        OPENLIST.pop(lowindex)
        
        if (n['state']==goal):      #print path to goal when goal is found
            temptrav = n
            path_to_goal = []
            while (temptrav!=None):
                path_to_goal.append(temptrav)
                temptrav = temptrav['ancestor']
            while (len(path_to_goal)!=0):
                pathnode =  path_to_goal.pop()
                for i in range(len(pathnode['state'])):
                    print ''.join(pathnode['state'][i])
                print "\n"
            print "this is goal"
            return

        m = []                  #list of next possible moves
        m = find_possible_next_moves(n['state'])
        M = []                  #calculate heuristic function for possible moves
        for i in range(len(m)):
            tempdict =  {
                'state': m[i],
                'f': 0,
                'g': n['g']+1,
                'h': find_manhattan_distance(m[i],goal),
                'ancestor': n
            }
            tempdict['f'] = tempdict['g'] + tempdict['h']
            M.append(tempdict)

        for i in range(len(M)):
            if (CLOSEDLIST.count(M[i])==0):
                OPENLIST.append(M[i])
        CLOSEDLIST.append(n)

#Required calls to above functions        
grid = get_input()
goal = get_goalstate(grid)
initialstate =  {
    'state': grid,
    'f': find_manhattan_distance(grid,goal),
    'g': 0,
    'h': find_manhattan_distance(grid,goal),
    'ancestor': None
}

OPENLIST.append(initialstate)
solve(goal)
