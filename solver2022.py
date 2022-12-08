#%%
#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: [kartik Bharadwaj 2000913109 karbhar@iu.edu]
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys  
from queue import PriorityQueue

ROWS=5
COLS=5
#%%
def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

def rot_row(curr_map,row, dirr):
    if dirr == 'R':
        curr_map[row] = [curr_map[row][-1]] + list(curr_map[row][:-1])
    elif dirr == 'L':
        curr_map[row] = list(curr_map[row][1:]) + [curr_map[row][0]]  
    return curr_map 

def rot_col(curr_map,col,dirr):
    curr_map = list(map(list, zip(*curr_map)))
    if dirr == 'U':
        curr_map = rot_row(curr_map, col, 'L')
    elif dirr == 'D':
        curr_map = rot_row(curr_map, col, 'R')      
    return  list(map(list, zip(*curr_map)))

def rot_outer_ring(curr_map,dirr):
    # idea of storing in a single list : https://www.codeproject.com/Questions/5299028/Rotatematrixrings-given-matrix-of-orderm-N-and-a-v
    # storing all values in a single list
    values = curr_map[0][:-1] + [x[-1] for x in curr_map][:-1] + curr_map[-1][::-1][:-1] + [x[0] for x in curr_map][::-1][:-1]
    
    if dirr == 'c':
        values  = [values[-1]] + values[:-1]
    
    elif dirr == 'cc':
        values  = values[1:] + [values[0]]
    
    # setting first and third side
    curr_map[0] = values[:len(curr_map[0])]
    curr_map[-1] = values[len(curr_map[0]) + len(curr_map)-2: len(curr_map[0]) + len(curr_map)- 2 + len(curr_map[0])][::-1]
    # setting second and fourth side
    curr_map = list(map(list, zip(*curr_map)))
    curr_map[-1] = values[len(curr_map[0]) - 1: len(curr_map[0]) + len(curr_map)-1]
    curr_map[0] = [curr_map[0][0]] + values[len(curr_map[0]) + len(curr_map) - 2+ len(curr_map[0]) -1 : ][::-1]
    curr_map = list(map(list, zip(*curr_map)))
  
    return curr_map

def rot_inner_ring(curr_map,dirr):
    # extracting inner matrix
    in_map = list(map(list, zip(*list(map(list, zip(*curr_map[1:-1])))[1:-1])))
    in_map = rot_outer_ring(in_map, dirr)
    
    in_map.append(curr_map[-1][1:-1])
    in_map.insert(0, curr_map[0][1:-1])

    in_map = list(map(list,zip(*in_map)))
    curr_map = list(map(list,zip(*curr_map)))
    
    in_map.append(curr_map[-1])
    in_map.insert(0, curr_map[0])

    in_map = list(map(list,zip(*in_map)))
    
    return in_map

#%%
def manhatten_dist(p1,p2, N):
    # implementation of modified manhatten distance 
    # that covers the corner cases for the problem
    x = abs(p1[0] - p2[0])
    y = abs(p1[1] - p2[1])
    
    d1 = x + y
    d2 = abs(N -  x) + y
    d3 = x + abs(N - y)
    d4 = abs(N -  x) + abs(N - y)

    return min(d1,d2, d3, d4)
    

def heuristic(curr_map, sol_loc):

    # modified manhatten distance
    dist_mh = []
    for i in range(len(curr_map)):
        for j in range(len(curr_map[0])):
            if sol_loc[curr_map[i][j]] != (i,j):
                dist = manhatten_dist((i,j), (sol_loc[curr_map[i][j]]), len(curr_map))
                dist_mh += [dist]

    # getting the weighted average of manhatten distance as the heuristic
    sm = sum(dist_mh)
    if sm != 0:
        sm /= len(dist_mh)
    else:
        sm = 0

    return sm  
#%%
# return a list of possible successor states
def successors(state):
    moves = []
    # successor of rows
    for i in range(1,len(state)+1):
        moves.append((rot_row(list(map(list, state[:])),i-1,'L'), 'L_' + str(i)))
        moves.append((rot_row(list(map(list, state[:])),i-1,'R'), 'R_' + str(i)))
    # successor of colums
    for i in range(1,len(state[0])+1):
        moves.append((rot_col(list(map(list, state[:])),i-1,'U'), 'U_' + str(i)))
        moves.append((rot_col(list(map(list, state[:])),i-1,'D'), 'D_' + str(i)))
    
    moves.extend([
        (rot_outer_ring(list(map(list, state[:])), 'c'), 'O_c'), 
        (rot_outer_ring(list(map(list, state[:])), 'cc'), 'O_cc'), 
        (rot_inner_ring(list(map(list, state[:])), 'c'), 'I_c'), 
        (rot_inner_ring(list(map(list, state[:])), 'cc') , 'I_cc')
    ])

    return moves

# check if we've reached the goal
def is_goal(state,sol):
    return True if state == sol else False


def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    initial_board = [initial_board[5*i:5*(i+1)] for i in range(5)]
    sol = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,25]]    
    # generating the actual position of each value
    sol_loc = {}
    for i in range(len(sol)):
        for j in range(len(sol[0])):
            sol_loc[sol[i][j]] = (i,j)

    # generating the priority queue
    fringe = PriorityQueue()
    fringe.put((0, initial_board, []))
    visited = []

    while not fringe.empty():
        (curr_cost, curr_map, curr_path)=fringe.get()
        visited.append(curr_map)

        # checking the goal state
        if is_goal(curr_map,sol):
            return ([x.replace('_', '') for x in curr_path])
        
        for move in successors(curr_map):
            if move[0] not in visited:
                temp_cost =  heuristic(move[0], sol_loc)
                # generating f(s) = path_travelled per tile + avg manhatten distance per tile
                # g(s) = path_travelled per tile
                # h(s) = avg manhatten distance per tile
                temp_cost += len(curr_path)/25
                fringe.put((temp_cost,  move[0], curr_path + [move[1]]))

    return []


#%%
# Please don't modify anything below this line

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
