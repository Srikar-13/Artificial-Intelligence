#
# raichu.py : Play the game of Raichu
#
# Nithin Varadharajan - nvaradha@iu.edu
# Saiabhinav Chekka   - schekka@iu.edu
# Sai Kaluri         - saik@iu.edu

# Based on skeleton code by D. Crandall, Oct 2021
#
from ntpath import join
import sys
import time
import copy

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def board_to_array(str_board, N):
    return [ [ x for x in str_board[i:i+N]  ] for i in range(0, len(str_board), N) ]
def array_to_board(arr_board, N):
    return "".join(["".join(i) for i in arr_board])

def chk_win(board_arr):

    board = array_to_board(board_arr, N)

    white_cnt = board.count('w') + board.count('W') + board.count('@')
    black_cnt = board.count('b') + board.count('B') + board.count('$')

    if ((white_cnt == 0) and (black_cnt != 0)):
        return True, 'b'
    elif ((white_cnt != 0) and (black_cnt == 0)):
        return True, 'w'
    else:
        return False, None

def heuristic_func(board_arr, player):

    board = array_to_board(board_arr, N)

    if ( player == 'w'):
        val = (1 * (board.count('w') - board.count('b'))) +  (2 * (board.count('W') - board.count('B'))) + (4 * (board.count('@') - board.count('$')))
    else:
        val = (1 * (board.count('b') - board.count('w'))) +  (2 * (board.count('B') - board.count('W'))) + (4 * (board.count('$') - board.count('@')))

    return val

def successor_func(board_arr, player, N):

    new_boards = []

    if(player == 'w'):   # player is white

        for row in range(N):      # iterate through all board indcies
            for col in range(N):
                
                if board_arr[row][col] == 'w':  # find white pichu

                    # Basic forward diag move white pichu
                    directions = ['forward_diag_l', 'forward_diag_r']
                    for direction in directions:
                      
                        if direction == 'forward_diag_l':
                            new_row = row + 1
                            new_col = col - 1
                        elif direction == 'forward_diag_r':
                            new_row = row + 1
                            new_col = col + 1
                       
                    
                        if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                            if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move
        
                                new_board[row][col] = '.'            # move operation

                                if new_row == N-1: # pichu is eligible for raichu evolution
                                    new_board[new_row][new_col] = '@'
                                else: # else just move it normally
                                    new_board[new_row][new_col] = 'w' 

                                new_boards.append(new_board) # append to list of successsor baord states
                        

                    # Jump case white pichu
                    directions = ['forward_diag_l', 'forward_diag_r']
                    for direction in directions:
                        if direction == 'forward_diag_l':
                            new_row = row + 2
                            new_col = col - 2
                            new_jumped_piece_row = row + 1
                            new_jumped_piece_col = col - 1
                        elif direction == 'forward_diag_r':
                            new_row = row + 2
                            new_col = col + 2
                            new_jumped_piece_row = row + 1
                            new_jumped_piece_col = col + 1

                        if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                            if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                if board_arr[new_jumped_piece_row][new_jumped_piece_col] == 'b': # chk if new jumped piece is a black pichu

                                    new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move

                                    new_board[row][col] = '.'                                      # jump operation
                                    new_board[new_jumped_piece_row][new_jumped_piece_col] = '.'

                                    if new_row == N-1: # pichu is eligible for raichu evolution
                                        new_board[new_row][new_col] = '@'
                                    else: # else just move it normally
                                        new_board[new_row][new_col] = 'w' 

                                    new_boards.append(new_board) # append to list of successsor baord states



                elif board_arr[row][col] == 'W':  # find white pikachu

                    # Basic move white pikachu
                    directions = ['forward', 'left', 'right']
                    for direction in directions:
                        for i in range(1,3):
                            if direction == 'forward':
                                new_row = row + i
                                new_col = col 
                            elif direction == 'left':
                                new_row = row 
                                new_col = col - i
                            elif direction == 'right':
                                new_row = row 
                                new_col = col + i

                            if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                                if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                    new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move
               
                                    new_board[row][col] = '.'            # move operation

                                    if new_row == N-1: # pikachu is eligible for raichu evolution
                                        new_board[new_row][new_col] = '@'
                                    else: # else just move it normally
                                        new_board[new_row][new_col] = 'W' 

                                    new_boards.append(new_board) # append to list of successsor baord states
                                else:
                                    break
                            else:
                                break

                    # jump white pikachu
                    directions = ['forward', 'left', 'right']
                    for direction in directions:
                        for i in range(1,3):  # possible location of jumped piece
                            if direction == 'forward':
                                new_jumped_row = row + i
                                new_jumped_col = col 
                            elif direction == 'left':
                                new_jumped_row = row 
                                new_jumped_col = col - i
                            elif direction == 'right':
                                new_jumped_row = row 
                                new_jumped_col = col + i

                            # Sending out feeler until piece is found to jump
                            if (0 <= new_jumped_row <= N-1) and (0 <= new_jumped_col <= N-1):  # chk if valid move pos
                                if board_arr[new_jumped_row][new_jumped_col] in "bB":   # chk if new jump loc is valid jump piece

                                    for j in range(i+1,4):        # iterate over final jump positions 
                                        if direction == 'forward':
                                            new_row = row + j
                                            new_col = col 
                                        elif direction == 'left':
                                            new_row = row 
                                            new_col = col - j
                                        elif direction == 'right':
                                            new_row = row 
                                            new_col = col + j

                                        if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                                            if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                                new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move

                                                new_board[row][col] = '.'                                      # jump operation
                                                new_board[new_jumped_row][new_jumped_col] = '.'

                                                if new_row == N-1: # pikachu is eligible for raichu evolution
                                                    new_board[new_row][new_col] = '@'
                                                else: # else just move it normally
                                                    new_board[new_row][new_col] = 'W' 
                                                new_boards.append(new_board) # append to list of successsor baord states
                                            else:
                                                break
                                        else:
                                            break
                                    
                                    break # done with this direction 
                                elif board_arr[new_jumped_row][new_jumped_col] == '.': # if empty continue checking
                                    continue
                                else: # if invalid piece is found then break to new direction
                                    break
                            else: # if invalid loc is found then break to new direction
                                break


                elif board_arr[row][col] == '@':  # find white raichu

                    # Basic move white raichu
                    directions = ['forward', 'backward', 'left', 'right', 'diag_1', 'diag_2', 'diag_3', 'diag_4']
                    for direction in directions:
                        for i in range(1,N):
                            if direction == 'forward':
                                new_row = row + i
                                new_col = col 
                            elif direction == 'backward':
                                new_row = row - i
                                new_col = col 
                            elif direction == 'left':
                                new_row = row 
                                new_col = col - i
                            elif direction == 'right':
                                new_row = row 
                                new_col = col + i

                            elif direction == 'diag_1':
                                new_row = row - i
                                new_col = col + i

                            elif direction == 'diag_2':
                                new_row = row + i
                                new_col = col - i
                            
                            elif direction == 'diag_3':
                                new_row = row - i
                                new_col = col - i
                            
                            elif direction == 'diag_4':
                                new_row = row + i
                                new_col = col + i

                            if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                                if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                    new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move
               
                                    new_board[row][col] = '.'            # move operation

                                    # just move it normally
                                    new_board[new_row][new_col] = '@' 

                                    new_boards.append(new_board) # append to list of successsor baord states
                                else:
                                    break
                            else:
                                break

                    # jump white raichu
                    directions = ['forward', 'backward', 'left', 'right', 'diag_1', 'diag_2', 'diag_3', 'diag_4']
                    for direction in directions:
                        for i in range(1,N-1): 
                            if direction == 'forward':
                                new_jumped_row = row + i
                                new_jumped_col = col 
                            elif direction == 'backward':
                                new_jumped_row = row - i
                                new_jumped_col = col 
                            elif direction == 'left':
                                new_jumped_row = row 
                                new_jumped_col = col - i
                            elif direction == 'right':
                                new_jumped_row = row 
                                new_jumped_col = col + i

                            elif direction == 'diag_1':
                                new_jumped_row = row - i
                                new_jumped_col = col + i

                            elif direction == 'diag_2':
                                new_jumped_row = row + i
                                new_jumped_col = col - i
                            
                            elif direction == 'diag_3':
                                new_jumped_row = row - i
                                new_jumped_col = col - i
                            
                            elif direction == 'diag_4':
                                new_jumped_row = row + i
                                new_jumped_col = col + i

                            # Sending out feeler until piece is found to jump
                            if (0 <= new_jumped_row <= N-1) and (0 <= new_jumped_col <= N-1):  # chk if valid move pos
                                if board_arr[new_jumped_row][new_jumped_col] in "bB$":   # chk if new jump loc is valid jump piece

                                    for j in range(i+1,N):        # iterate over final jump positions 
                                        if direction == 'forward':
                                            new_row = row + j
                                            new_col = col 
                                        elif direction == 'backward':
                                            new_row = row - j
                                            new_col = col 
                                        elif direction == 'left':
                                            new_row = row 
                                            new_col = col - j
                                        elif direction == 'right':
                                            new_row = row 
                                            new_col = col + j

                                        elif direction == 'diag_1':
                                            new_row = row - j
                                            new_col = col + j

                                        elif direction == 'diag_2':
                                            new_row = row + j
                                            new_col = col - j
                                        
                                        elif direction == 'diag_3':
                                            new_row = row - j
                                            new_col = col - j
                                        
                                        elif direction == 'diag_4':
                                            new_row = row + j
                                            new_col = col + j

                                        if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                                            if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                                new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move

                                                new_board[row][col] = '.'                            # jump operation
                                                new_board[new_jumped_row][new_jumped_col] = '.'

                                                #  just move it normally
                                                new_board[new_row][new_col] = '@' 

                                                new_boards.append(new_board) # append to list of successsor baord states
                                            else:
                                                break
                                        else:
                                            break
                                    
                                    break # done with this direction 
                                elif board_arr[new_jumped_row][new_jumped_col] == '.': # if empty continue checking
                                    continue
                                else: # if invalid piece is found then break to new direction
                                    break
                            else: # if invalid loc is found then break to new direction
                                break                



 
    else: # if player is black 'b'

        for row in range(N):      # iterate through all board indcies
            for col in range(N):
                
                if board_arr[row][col] == 'b':  # find black pichu

                    # Basic forward diag move black pichu
                    directions = ['forward_diag_l', 'forward_diag_r']
                    for direction in directions:
                      
                        if direction == 'forward_diag_l':
                            new_row = row - 1
                            new_col = col - 1
                        elif direction == 'forward_diag_r':
                            new_row = row - 1
                            new_col = col + 1
                       
                    
                        if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                            if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move
        
                                new_board[row][col] = '.'            # move operation

                                if new_row == 0: # pichu is eligible for raichu evolution
                                    new_board[new_row][new_col] = '$'
                                else: # else just move it normally
                                    new_board[new_row][new_col] = 'b' 

                                new_boards.append(new_board) # append to list of successsor baord states
                        

                    # Jump case black pichu
                    directions = ['forward_diag_l', 'forward_diag_r']
                    for direction in directions:
                        if direction == 'forward_diag_l':
                            new_row = row - 2
                            new_col = col - 2
                            new_jumped_piece_row = row - 1
                            new_jumped_piece_col = col - 1
                        elif direction == 'forward_diag_r':
                            new_row = row - 2
                            new_col = col + 2
                            new_jumped_piece_row = row - 1
                            new_jumped_piece_col = col + 1

                        if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                            if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                if board_arr[new_jumped_piece_row][new_jumped_piece_col] == 'w': # chk if new jumped piece is a white pichu

                                    new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move

                                    new_board[row][col] = '.'                                      # jump operation
                                    new_board[new_jumped_piece_row][new_jumped_piece_col] = '.'

                                    if new_row == 0: # pichu is eligible for raichu evolution
                                        new_board[new_row][new_col] = '$'
                                    else: # else just move it normally
                                        new_board[new_row][new_col] = 'b' 

                                    new_boards.append(new_board) # append to list of successsor baord states

                elif board_arr[row][col] == 'B':  # find black pikachu

                    # Basic move black pikachu
                    directions = ['forward', 'left', 'right']
                    for direction in directions:
                        for i in range(1,3):
                            if direction == 'forward':
                                new_row = row - i
                                new_col = col 
                            elif direction == 'left':
                                new_row = row 
                                new_col = col - i
                            elif direction == 'right':
                                new_row = row 
                                new_col = col + i

                            if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                                if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                    new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move
               
                                    new_board[row][col] = '.'            # move operation

                                    if new_row == 0: # pikachu is eligible for raichu evolution
                                        new_board[new_row][new_col] = '$'
                                    else: # else just move it normally
                                        new_board[new_row][new_col] = 'B' 

                                    new_boards.append(new_board) # append to list of successsor baord states
                                else:
                                    break
                            else:
                                break

                    # jump black pikachu
                    directions = ['forward', 'left', 'right']
                    for direction in directions:
                        for i in range(1,3):  # possible location of jumped piece
                            if direction == 'forward':
                                new_jumped_row = row - i
                                new_jumped_col = col 
                            elif direction == 'left':
                                new_jumped_row = row 
                                new_jumped_col = col - i
                            elif direction == 'right':
                                new_jumped_row = row 
                                new_jumped_col = col + i

                            # Sending out feeler until piece is found to jump
                            if (0 <= new_jumped_row <= N-1) and (0 <= new_jumped_col <= N-1):  # chk if valid move pos
                                if board_arr[new_jumped_row][new_jumped_col] in "wW":   # chk if new jump loc is valid jump piece

                                    for j in range(i+1,4):        # iterate over final jump positions 
                                        if direction == 'forward':
                                            new_row = row - j
                                            new_col = col 
                                        elif direction == 'left':
                                            new_row = row 
                                            new_col = col - j
                                        elif direction == 'right':
                                            new_row = row 
                                            new_col = col + j

                                        if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                                            if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                                new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move

                                                new_board[row][col] = '.'                                      # jump operation
                                                new_board[new_jumped_row][new_jumped_col] = '.'

                                                if new_row == 0: # pikachu is eligible for raichu evolution
                                                    new_board[new_row][new_col] = '$'
                                                else: # else just move it normally
                                                    new_board[new_row][new_col] = 'B' 
                                                new_boards.append(new_board) # append to list of successsor baord states
                                            else:
                                                break
                                        else:
                                            break
                                    
                                    break # done with this direction 
                                elif board_arr[new_jumped_row][new_jumped_col] == '.': # if empty continue checking
                                    continue
                                else: # if invalid piece is found then break to new direction
                                    break
                            else: # if invalid loc is found then break to new direction
                                break
                
                elif board_arr[row][col] == '$':  # find black raichu

                    # Basic move black raichu
                    directions = ['forward', 'backward', 'left', 'right', 'diag_1', 'diag_2', 'diag_3', 'diag_4']
                    for direction in directions:
                        for i in range(1,N):
                            if direction == 'forward':
                                new_row = row + i
                                new_col = col 
                            elif direction == 'backward':
                                new_row = row - i
                                new_col = col 
                            elif direction == 'left':
                                new_row = row 
                                new_col = col - i
                            elif direction == 'right':
                                new_row = row 
                                new_col = col + i

                            elif direction == 'diag_1':
                                new_row = row - i
                                new_col = col + i

                            elif direction == 'diag_2':
                                new_row = row + i
                                new_col = col - i
                            
                            elif direction == 'diag_3':
                                new_row = row - i
                                new_col = col - i
                            
                            elif direction == 'diag_4':
                                new_row = row + i
                                new_col = col + i

                            if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                                if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                    new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move
               
                                    new_board[row][col] = '.'            # move operation

                                    # just move it normally
                                    new_board[new_row][new_col] = '$' 

                                    new_boards.append(new_board) # append to list of successsor baord states
                                else:
                                    break
                            else:
                                break

                    # jump black raichu
                    directions = ['forward', 'backward', 'left', 'right', 'diag_1', 'diag_2', 'diag_3', 'diag_4']
                    for direction in directions:
                        for i in range(1,N-1): 
                            if direction == 'forward':
                                new_jumped_row = row + i
                                new_jumped_col = col 
                            elif direction == 'backward':
                                new_jumped_row = row - i
                                new_jumped_col = col 
                            elif direction == 'left':
                                new_jumped_row = row 
                                new_jumped_col = col - i
                            elif direction == 'right':
                                new_jumped_row = row 
                                new_jumped_col = col + i

                            elif direction == 'diag_1':
                                new_jumped_row = row - i
                                new_jumped_col = col + i

                            elif direction == 'diag_2':
                                new_jumped_row = row + i
                                new_jumped_col = col - i
                            
                            elif direction == 'diag_3':
                                new_jumped_row = row - i
                                new_jumped_col = col - i
                            
                            elif direction == 'diag_4':
                                new_jumped_row = row + i
                                new_jumped_col = col + i

                            # Sending out feeler until piece is found to jump
                            if (0 <= new_jumped_row <= N-1) and (0 <= new_jumped_col <= N-1):  # chk if valid move pos
                                if board_arr[new_jumped_row][new_jumped_col] in "wW@":   # chk if new jump loc is valid jump piece

                                    for j in range(i+1,N):        # iterate over final jump positions 
                                        if direction == 'forward':
                                            new_row = row + j
                                            new_col = col 
                                        elif direction == 'backward':
                                            new_row = row - j
                                            new_col = col 
                                        elif direction == 'left':
                                            new_row = row 
                                            new_col = col - j
                                        elif direction == 'right':
                                            new_row = row 
                                            new_col = col + j

                                        elif direction == 'diag_1':
                                            new_row = row - j
                                            new_col = col + j

                                        elif direction == 'diag_2':
                                            new_row = row + j
                                            new_col = col - j
                                        
                                        elif direction == 'diag_3':
                                            new_row = row - j
                                            new_col = col - j
                                        
                                        elif direction == 'diag_4':
                                            new_row = row + j
                                            new_col = col + j

                                        if (0 <= new_row <= N-1) and (0 <= new_col <= N-1):  # chk if valid move pos
                                            if board_arr[new_row][new_col] == '.':   # chk if new sqaure is empty
                                                new_board = copy.deepcopy(board_arr) # copying board_array to create modified version with move

                                                new_board[row][col] = '.'                            # jump operation
                                                new_board[new_jumped_row][new_jumped_col] = '.'

                                                #  just move it normally
                                                new_board[new_row][new_col] = '$' 

                                                new_boards.append(new_board) # append to list of successsor baord states
                                            else:
                                                break
                                        else:
                                            break
                                    
                                    break # done with this direction 
                                elif board_arr[new_jumped_row][new_jumped_col] == '.': # if empty continue checking
                                    continue
                                else: # if invalid piece is found then break to new direction
                                    break
                            else: # if invalid loc is found then break to new direction
                                break       

    return new_boards         
                




def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #


    def minimax(board, alpha, beta, depth, N, player):
        _, new_board = max_val(board, alpha, beta, depth, N, player)
        return new_board


    def min_val(board, alpha, beta, depth, N, player):
        # chk terminal state
        # if (chk_win(board)): # could add horizon and heuristic if depth is reached
        #     return -20+depth, None # depth allows the agent to chose the the fastest win possible
        # # elif chk_terminal(board):
        # #     return 0, None

        if (depth == depth_limit):
            return heuristic_func(board, player), board
            
        minEval = float('inf')
        min_board = None

        succ_board_list = successor_func(board, player, N)
        # for i in range(len(board)):
        #   for j in range(len(board[0])):
        #     if board[i][j] != 'x' :
        #       new_board = add_piece(board, i, j)
        for new_board in succ_board_list:
            eval, _ = max_val(new_board, alpha, beta, depth+1, N, player) 
            if eval < minEval:
                minEval = eval
                min_board = new_board
            if minEval < beta:
                beta = minEval
            if beta <= alpha:
                return minEval, min_board

        return minEval, min_board


    def max_val(board, alpha, beta, depth, N, player):
        # chk terminal state
        # if (check_win(board)):
        #     return 20-depth, None
        # elif chk_terminal(board):
        #     return 0, None

        if (depth == depth_limit):
            return heuristic_func(board, player), board


        maxEval = float('-inf')
        max_board = None

        succ_board_list = successor_func(board, player, N)
        # for i in range(len(board)):
        #   for j in range(len(board[0])):
        #     if board[i][j] != 'x' :
        #       new_board = add_piece(board, i, j)
        for new_board in succ_board_list:
            eval, _ = min_val(new_board, alpha, beta, depth+1, N, player) 
            if eval > maxEval:
                maxEval = eval
                max_board = new_board
            if maxEval > alpha:
                alpha = maxEval
            if beta <= alpha:
                return maxEval, max_board
        return maxEval, max_board


    
    depth_limit = 2 # basic move
    time_remaining = timelimit
    while True:
        start_time = time.time()
        new_board = minimax(board_to_array(board, N), float('-inf'),float('inf'), 0, N, player)
        
        current_time = time.time()
        time_elapsed = current_time - start_time
        time_remaining = time_remaining - time_elapsed
        print("Depth : {} took {} seconds".format(depth_limit, time_elapsed))
        print()
        print(board_to_string(array_to_board(new_board, N), N))
        print()
        yield array_to_board(new_board, N)
        depth_limit += 1
        if(time_remaining < time_elapsed):
            break
        else:
            continue

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
