import math
import sys
import numpy as np
import os 
import copy

#my direction of the algorithm: alpha-beta pruning minimax algorithm


def load_matrix(matrix_file_name): # read and load the current state
    with open(matrix_file_name, 'r') as f:
        data = f.read()
        data2=data.replace('\n',',').split(',')
    matrix = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            matrix[i,j]=int(data2[5*i+j])
    return matrix

def write_matrix(matrix, matrix_file_name_output): # wirte the new state into new txt file
    with open(matrix_file_name_output, 'w') as f:
        for i in range(5):
            for j in range(5):
                f.write(str(int(matrix[i,j])))
                if j<4:
                    f.write(',')
                if j==4:
                    f.write('\n')

# COPY FROM WES_Engine.py line 97
def checkWinning(board):
    # 1: wolf wins, 2: sheep wins, 0: continually gaming
    # check wolves winning
    sheep_num = 0
    wolf_neighbour = []
    wolf_win = True
    sheep_win = True
    winner = 0
    line_range = [0, 1, 2, 3, 4]
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == '1':
                sheep_num += 1
            elif board[r][c] == '2':
                if r - 1 in line_range:
                    wolf_neighbour.append((r-1, c))
                if r + 1 in line_range:
                    wolf_neighbour.append((r + 1, c))
                if c - 1 in line_range:
                    wolf_neighbour.append((r, c - 1))
                if c + 1 in line_range:
                    wolf_neighbour.append((r, c + 1))
            else:
                pass
    for item in wolf_neighbour:
        if board[item[0]][item[1]] == '0':
            sheep_win = not sheep_win
            break
    if sheep_num > 2:
        wolf_win = not wolf_win

    if wolf_win:
        winner = 1
    if sheep_win:
        winner = 2

    return winner

def getAvailableMove(matrix,turn):
    print("available Move is...")
    
    #COPY FROM ORIGINAL next_move_wolf PROVIDED BY YOU
    candidates=[]
    role = 0
    if turn == 'Wolf':
        role = 2
    else:
        role = 1
    
    for i in range(5):
        for j in range(5):
            if matrix[i,j]==role:
                if i+1<5:
                    if matrix[i+1,j]==0:
                        candidates.append([i,j,i+1,j])
                if i-1>=0:
                    if matrix[i-1,j]==0:
                        candidates.append([i,j,i-1,j])
                if j+1<5:
                    if matrix[i,j+1]==0:
                        candidates.append([i,j,i,j+1])
                if j-1>=0:
                    if matrix[i,j-1]==0:
                        candidates.append([i,j,i,j-1])
                if i+2<5:
                    if matrix[i+2,j]==1 and matrix[i+1,j]==0:
                        candidates.append([i,j,i+2,j])
                if i-2>=0:
                    if matrix[i-2,j]==1 and matrix[i-1,j]==0:
                        candidates.append([i,j,i-2,j])
                if j+2<5:
                    if matrix[i,j+2]==1 and matrix[i,j+1]==0:
                        candidates.append([i,j,i,j+2])
                if j-2>=0:
                    if matrix[i,j-2]==1 and matrix[i,j-1]==0:
                        candidates.append([i,j,i,j-2])
    
    return candidates

# core of minimax algorithm    
def evaluationFunction(matrix, turn, yourRole):
    role = 0
    if turn == 'Wolf':
        role = 2
    else:
        role = 1
    

def minimax(state, depth, score, alpha, beta, yourRole, turn):
    print("minimax algorithm")
    if depth == 0 or checkWinning(state) != 0:
        return evaluationFunction(state, turn, yourRole)
    
    role = 0
    if turn == 'Wolf':
        role = 2
    else:
        role = 1
        
    bestScore = -math.inf
    avaliableMove = getAvailableMove(state, turn)
    for move in avaliableMove:
        simulationState = copy.deepcopy(state)
        beforeMoveX = move[0]
        beforeMoveY = move[1]
        afterMoveX = move[2]
        afterMovey = move[3]
        simulationState[beforeMoveX,beforeMoveY] = 0
        simulationState[afterMoveX,afterMovey] = role
        
        evaluatedScoreForThisBoard = evaluationFunction(simulationState, turn, yourRole)
        nextTurn = 'Who is next turn'
        if role == 2:
            nextTurn = 'Sheep'
        else:
            nextTurn = 'Wolf'
        currentScore = minimax(simulationState, depth-1, evaluatedScoreForThisBoard, alpha, beta, yourRole, nextTurn)
        
        bestScore = max(bestScore, currentScore)
        
        if yourRole == turn:           
            alpha = max(alpha,bestScore)
            if alpha >= beta:
                break
        else:
            beta = min(bestScore,currentScore)
            if alpha >= beta:
                break
    return bestScore

            
    
#THE WAY OF WRITING THE MINIMAX ALGO IS SIMILAR TO ASM 1 OF MINE, IT IS JUST A MINIMAX, WHAT CAN I CHANGE? JUST THE EVALUATION FUNCTION IS DIFFERENT
def next_move_wolf(matrix): # minimax for wolf
    availableMove = []
    
    bestMove = None
    bestScore = math.inf
    
    alpha = -math.inf
    beta = math.inf
    
    for move in availableMove:
        simulationState = copy.deepcopy(matrix)
        beforeMoveX = move[0]
        beforeMoveY = move[1]
        afterMoveX = move[2]
        afterMovey = move[3]
        simulationState[beforeMoveX,beforeMoveY] = 0
        simulationState[afterMoveX,afterMovey] = 2
        EvaluatedScoreForThisBoard = evaluationFunction(simulationState, True)
        currentScore = minimax(simulationState, 7, False, EvaluatedScoreForThisBoard, alpha, beta, 'Wolf', 'Sheep')
        bestScore = max(bestScore, currentScore)
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = move 
        alpha = max(alpha, bestScore)
    return bestMove    
    
    # candidates=[]
    # for i in range(5):
    #     for j in range(5):
    #         if matrix[i,j]==2:
    #             if i+1<5:
    #                 if matrix[i+1,j]==0:
    #                     candidates.append([i,j,i+1,j])
    #             if i-1>=0:
    #                 if matrix[i-1,j]==0:
    #                     candidates.append([i,j,i-1,j])
    #             if j+1<5:
    #                 if matrix[i,j+1]==0:
    #                     candidates.append([i,j,i,j+1])
    #             if j-1>=0:
    #                 if matrix[i,j-1]==0:
    #                     candidates.append([i,j,i,j-1])
    #             if i+2<5:
    #                 if matrix[i+2,j]==1 and matrix[i+1,j]==0:
    #                     candidates.append([i,j,i+2,j])
    #             if i-2>=0:
    #                 if matrix[i-2,j]==1 and matrix[i-1,j]==0:
    #                     candidates.append([i,j,i-2,j])
    #             if j+2<5:
    #                 if matrix[i,j+2]==1 and matrix[i,j+1]==0:
    #                     candidates.append([i,j,i,j+2])
    #             if j-2>=0:
    #                 if matrix[i,j-2]==1 and matrix[i,j-1]==0:
    #                     candidates.append([i,j,i,j-2])
    # move_idx=np.random.randint(0, len(candidates))
    # return candidates[move_idx]
    
    

def next_move_sheep(matrix): # minimax for sheep
    availableMove = []
    
    bestMove = None
    bestScore = math.inf
    
    alpha = -math.inf
    beta = math.inf
    
    for move in availableMove:
        simulationState = copy.deepcopy(matrix)
        beforeMoveX = move[0]
        beforeMoveY = move[1]
        afterMoveX = move[2]
        afterMovey = move[3]
        simulationState[beforeMoveX,beforeMoveY] = 0
        simulationState[afterMoveX,afterMovey] = 1
        EvaluatedScoreForThisBoard = evaluationFunction(simulationState, True)
        currentScore = minimax(simulationState, 7, False, EvaluatedScoreForThisBoard, alpha, beta,'Sheep', 'Wolf')
        bestScore = max(bestScore, currentScore)
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = move 
        alpha = max(alpha, bestScore)
    return bestMove  
    
    # candidates=[]
    # for i in range(5):
    #     for j in range(5):
    #         if matrix[i,j]==1:
    #             if i+1<5:
    #                 if matrix[i+1,j]==0:
    #                     candidates.append([i,j,i+1,j])
    #             if i-1>=0:
    #                 if matrix[i-1,j]==0:
    #                     candidates.append([i,j,i-1,j])
    #             if j+1<5:
    #                 if matrix[i,j+1]==0:
    #                     candidates.append([i,j,i,j+1])
    #             if j-1>=0:
    #                 if matrix[i,j-1]==0:
    #                     candidates.append([i,j,i,j-1])
    # move_idx=np.random.randint(0, len(candidates))
    # return candidates[move_idx]

#!!!DISCLAIMER!!!
################################################################
#I DID ALL THE THING BY MYSELF
#THE WAY OF WRITING THE MINIMAX ALGO IS SIMILAR TO ASM 1 OF MINE
#PLEASE DO NOT ACCUSE ME OF PLAGARISM CUZ OF COPYING WORK BY MYSELF
#IT IS CALL REUSE ENGINEERING(WORK SMART NOT HARD) AND NOT FULLY COPYING(JUST LIKE REFERRING TO PSEUDO CODE)
#IF THIS CALL PLAGARISM, THEN EVERYTIME I WRITE HELLO WORLD PROGRAM I PLAGARISE ONCE CUZ I MOST LIKELY A LOT OF HELLO WORLD CODE IN THE INTERNET 
################################################################
#!!!DISCLAIMER!!!

def AIAlgorithm(filename, movemade): # a showcase for random walk
    iter_num=filename.split('/')[-1]
    iter_num=iter_num.split('.')[0]
    iter_num=int(iter_num.split('_')[1])
    matrix=load_matrix(filename)
    role = ""
    if movemade is True:
        role = "wolf"
    else:
        role = "sheep"
    print(role,"'s turn, current board: \n",matrix)
    if movemade==True:
        [start_row, start_col, end_row, end_col]=next_move_wolf(matrix)
        matrix2=copy.deepcopy(matrix)
        matrix2[end_row, end_col]=2
        matrix2[start_row, start_col]=0
            
    if movemade==False:
        [start_row, start_col, end_row, end_col]=next_move_sheep(matrix)
        matrix2=copy.deepcopy(matrix)
        matrix2[end_row, end_col]=1
        matrix2[start_row, start_col]=0
        
    matrix_file_name_output=filename.replace('state_'+str(iter_num), 'state_'+str(iter_num+1)) 
    write_matrix(matrix2, matrix_file_name_output)

    return start_row, start_col, end_row, end_col

# import numpy as np
# import os 
# import copy

# def load_matrix(matrix_file_name): # read and load the current state
#     with open(matrix_file_name, 'r') as f:
#         data = f.read()
#         data2=data.replace('\n',',').split(',')
#     matrix = np.zeros((5, 5))
#     for i in range(5):
#         for j in range(5):
#             matrix[i,j]=int(data2[5*i+j])
#     return matrix

# def write_matrix(matrix, matrix_file_name_output): # wirte the new state into new txt file
#     with open(matrix_file_name_output, 'w') as f:
#         for i in range(5):
#             for j in range(5):
#                 f.write(str(int(matrix[i,j])))
#                 if j<4:
#                     f.write(',')
#                 if j==4:
#                     f.write('\n')

# def next_move_wolf(matrix): # random walk for wolf
#     candidates=[]
#     for i in range(5):
#         for j in range(5):
#             if matrix[i,j]==2:
#                 if i+1<5:
#                     if matrix[i+1,j]==0:
#                         candidates.append([i,j,i+1,j])
#                 if i-1>=0:
#                     if matrix[i-1,j]==0:
#                         candidates.append([i,j,i-1,j])
#                 if j+1<5:
#                     if matrix[i,j+1]==0:
#                         candidates.append([i,j,i,j+1])
#                 if j-1>=0:
#                     if matrix[i,j-1]==0:
#                         candidates.append([i,j,i,j-1])
#                 if i+2<5:
#                     if matrix[i+2,j]==1 and matrix[i+1,j]==0:
#                         candidates.append([i,j,i+2,j])
#                 if i-2>=0:
#                     if matrix[i-2,j]==1 and matrix[i-1,j]==0:
#                         candidates.append([i,j,i-2,j])
#                 if j+2<5:
#                     if matrix[i,j+2]==1 and matrix[i,j+1]==0:
#                         candidates.append([i,j,i,j+2])
#                 if j-2>=0:
#                     if matrix[i,j-2]==1 and matrix[i,j-1]==0:
#                         candidates.append([i,j,i,j-2])
#     move_idx=np.random.randint(0, len(candidates))
#     return candidates[move_idx]

# def next_move_sheep(matrix): # random walk for sheep
#     candidates=[]
#     for i in range(5):
#         for j in range(5):
#             if matrix[i,j]==1:
#                 if i+1<5:
#                     if matrix[i+1,j]==0:
#                         candidates.append([i,j,i+1,j])
#                 if i-1>=0:
#                     if matrix[i-1,j]==0:
#                         candidates.append([i,j,i-1,j])
#                 if j+1<5:
#                     if matrix[i,j+1]==0:
#                         candidates.append([i,j,i,j+1])
#                 if j-1>=0:
#                     if matrix[i,j-1]==0:
#                         candidates.append([i,j,i,j-1])
#     move_idx=np.random.randint(0, len(candidates))
#     return candidates[move_idx]

# def ai_algorithm(filename, movemade): # a showcase for random walk
#     iter_num=filename.split('/')[-1]
#     iter_num=iter_num.split('.')[0]
#     iter_num=int(iter_num.split('_')[1])
#     matrix=load_matrix(filename)
#     if movemade==True:
#         [start_row, start_col, end_row, end_col]=next_move_wolf(matrix)
#         matrix2=copy.deepcopy(matrix)
#         matrix2[end_row, end_col]=2
#         matrix2[start_row, start_col]=0
            
#     if movemade==False:
#         [start_row, start_col, end_row, end_col]=next_move_sheep(matrix)
#         matrix2=copy.deepcopy(matrix)
#         matrix2[end_row, end_col]=1
#         matrix2[start_row, start_col]=0
        
#     matrix_file_name_output=filename.replace('state_'+str(iter_num), 'state_'+str(iter_num+1)) 
#     write_matrix(matrix2, matrix_file_name_output)

#     return start_row, start_col, end_row, end_col

