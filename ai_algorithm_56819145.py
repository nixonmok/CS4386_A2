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
    #changed char detection to integer detection to avoid bug
    sheep_num = 0
    wolf_neighbour = []
    wolf_win = True
    sheep_win = True
    winner = 0
    line_range = [0, 1, 2, 3, 4]
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 1:
                sheep_num += 1
            elif board[r][c] == 2:
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
        if board[item[0]][item[1]] == 0:
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
    
    #COPY FROM ORIGINAL next_move_wolf/sheep PROVIDED BY YOU
    candidates=[]
    role = 0
    if turn == 'Wolf':
        role = 2
    else:
        role = 1
    
    if role == 2:
        for i in range(5):
            for j in range(5):
                if matrix[i,j]==2:
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
    else:
        for i in range(5):
            for j in range(5):
                if matrix[i,j]==1:
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
    return candidates

# core of minimax algorithm, if yourRole != turn -> score should be inverted by *-1 
def evaluationFunction(matrix, turn, yourRole):
        
    wolfPos = []
    sheepPos = []
    for i in range(5):
        for j in range(5):
            if matrix[i][j]==2:
                wolfPos.append([i,j])
            if matrix[i][j]==1:
                sheepPos.append([i,j])   
        # idea:
        # have a counter check different sheep position to wolf
        # if countSheepNearby == 4 -> -score
        # if wolf can eat a sheep -> +score (premise that sheep 'can' eat that sheep, not blocked by the sheep near)
        # if sheep count == 3 and wolf can eat sheep -> score+++ -> no neccessary the best(so not inf) cuz maybe the alternative decision while chossing the decision is bad
        # for horizontal or vertical:
        # 3 block from wolf -> +score if that sheep has no ally nearby, -score for 1 sheep nearby
        # 4 block from wolf -> no need to care
        # for diagonal:
        # 1 block from wolf -> - score according to how dangerous it is
 
                
    NumberOfSheep = len(sheepPos) #get the number of sheep on the board
    score = 0 #score to be returned
    
    for wolf in wolfPos:
        countSheepNearby = 0 #various counter, check out report for detailed description
        countCanEat = 0 
        countThreeBlockAway = 0
        futureRisk = 0
        atMostThreeRisk = 0
        atMostFourRisk = 0
        for sheep in sheepPos:            
            if sheep[0] == wolf[0]: #horizontal
                if sheep[1]-wolf[1] == -1 or sheep[1]-wolf[1] == 1:#nearby
                    countSheepNearby += 1
                
                elif sheep[1]-wolf[1] == -2 or sheep[1]-wolf[1] == 2:#2 block away
                    if wolf[1] == 0:
                        if matrix[wolf[0]][1] == 0:
                            countCanEat += 1
                    if wolf[1] == 4:
                        if matrix[wolf[0]][3] == 0:
                            countCanEat += 1
                    else:
                        if matrix[wolf[0]][(sheep[1]+wolf[1])//2] == 0:
                            countCanEat += 1
                elif sheep[1]-wolf[1] == -3 or sheep[1]-wolf[1] == 3: #3 block away
                    countThreeBlockAway += 1
                    #print("3 blocks away")
                    ifSheepMove = None
                    if sheep[1] > wolf[1]:
                        ifSheepMove = sheep[1] - 1
                    else:
                        ifSheepMove = sheep[1] + 1
                    if sheep[0] - 1 < 0: #sheep[0][?]
                        #print("sheep[0][?]")
                        if matrix[sheep[0]+1][ifSheepMove] == 1:
                            futureRisk += 1
                    elif sheep[0] + 1 > 4: #sheep[4][?]
                        #print("sheep[4][?]")
                        if matrix[sheep[0]-1][ifSheepMove] == 1:
                            futureRisk += 1
                    else:
                        if matrix[sheep[0]+1][ifSheepMove] == 1:
                            futureRisk += 1
                        if matrix[sheep[0]-1][ifSheepMove] == 1:
                            futureRisk += 1
                        
                    #print("3 blocks away")
            elif sheep[1] == wolf[1]: #vertical 
                if sheep[0]-wolf[0] == -1 or sheep[0]-wolf[0] == 1:
                    countSheepNearby += 1                
                elif sheep[0]-wolf[0] == -2 or sheep[0]-wolf[0] == 2:
                    if wolf[0] == 0:
                        if matrix[1][wolf[1]] == 0:
                            countCanEat += 1
                    if wolf[0] == 4:
                        if matrix[3][wolf[1]] == 0:
                            countCanEat += 1
                    else:
                        if matrix[(sheep[0]+wolf[0])//2][wolf[1]] == 0:
                            countCanEat += 1
                elif sheep[0]-wolf[0] == -3 or sheep[0]-wolf[0] == 3: 
                    #print("3 blocks away")
                    ifSheepMove = None
                    if sheep[0] > wolf[0]:
                        ifSheepMove = sheep[0] - 1
                    else:
                        ifSheepMove = sheep[0] + 1
                    if sheep[1] - 1 < 0: #sheep[0][?]
                        #print("sheep[0][?]")
                        if matrix[ifSheepMove][sheep[1]+1] == 1:
                            futureRisk += 1
                    elif sheep[1] + 1 > 4: #sheep[4][?]
#                       print("sheep[4][?]")
                        if matrix[ifSheepMove][sheep[1]-1] == 1:
                            futureRisk += 1
                    else:
                        if matrix[ifSheepMove][sheep[1]+1] == 1:
                            futureRisk += 1
                        if matrix[ifSheepMove][sheep[1]-1] == 1:
                            futureRisk += 1
                                     
#                    print("3 blocks away")
            else: #diagonal
                if wolf[0] == 0 and wolf[1] == 0:
                    if sheep[0] == 1 and sheep[1] == 1: 
                        if matrix[0][1] == 1 and matrix[1][0] == 1:
                            score -= 70 #no escape
                        elif matrix[0][1] == 1 or matrix[1][0] == 1:
                            score -= 50 #no escape
                        else:
                            score -= 20 #bad idea
                    #print("left up")
                elif wolf[0] == 4 and wolf[1] == 0:
                    if sheep[0] == 3 and sheep[1] == 1:
                        if matrix[3][0] == 1 and matrix[4][1] == 1:
                            score -= 70 #no escape
                        elif matrix[3][0] == 1 or matrix[4][1] == 1:
                            score -= 50 #no escape
                        else:
                            score -= 20 #bad idea
                    #print("left down")
                elif wolf[0] == 0 and wolf[1] == 4:
                    if sheep[0] == 1 and sheep[1] == 3:
                        if matrix[0][3] == 1 and matrix[1][4] == 1:
                            score -= 70 #no escape
                        elif matrix[0][3] == 1 or matrix[1][4] == 1:
                            score -= 50 #no escape
                        else:
                            score -= 20 #bad idea
                    #print("right up")
                elif wolf[0] == 4 and wolf[1] == 4:
                    if sheep[0] == 3 and sheep[1] == 3:
                        if matrix[3][4] == 1 and matrix[4][3] == 1:
                            score -= 70
                        elif matrix[3][4] == 1 or matrix[4][3] == 1:
                            score -= 50 #no escape
                        else:
                            score -= 20 #bad idea
                    #print("right down")
                elif wolf[0] == 0:
                    if sheep[0] == 1 and (sheep[1] == wolf[1] - 1 or sheep[1] == wolf[1] + 1):
                        if matrix[wolf[0]][wolf[1]+1] == 1:
                            atMostThreeRisk += 1
                        if matrix[wolf[0]][wolf[1]-1] == 1:
                            atMostThreeRisk += 1
                        if matrix[wolf[0]+1][wolf[1]] == 1:
                            atMostThreeRisk += 1
                    #print("up")
                elif wolf[0] == 4:
                    if sheep[0] == 3 and (sheep[1] == wolf[1] - 1 or sheep[1] == wolf[1] + 1):
                        if matrix[wolf[0]][wolf[1]+1] == 1:
                            atMostThreeRisk += 1
                        if matrix[wolf[0]][wolf[1]-1] == 1:
                            atMostThreeRisk += 1
                        if matrix[wolf[0]-1][wolf[1]] == 1:
                            atMostThreeRisk += 1
                    #print("down")
                elif wolf[1] == 0:
                    if sheep[1] == 1 and (sheep[0] == wolf[0] - 1 or sheep[0] == wolf[0] + 1):
                        if matrix[wolf[0]-1][wolf[1]] == 1:
                            atMostThreeRisk += 1
                        if matrix[wolf[0]+1][wolf[1]] == 1:
                            atMostThreeRisk += 1
                        if matrix[wolf[0]][wolf[1]+1] == 1:
                            atMostThreeRisk += 1
                    #print("left")
                elif wolf[1] == 4:
                    if sheep[1] == 3 and (sheep[0] == wolf[0] - 1 or sheep[0] == wolf[0] + 1):
                        if matrix[wolf[0]-1][wolf[1]] == 1:
                            atMostThreeRisk += 1
                        if matrix[wolf[0]+1][wolf[1]] == 1:
                            atMostThreeRisk += 1
                        if matrix[wolf[0]][wolf[1]-1] == 1:
                            atMostThreeRisk += 1
                    #print("right")
                else:
                    if (sheep[0] == wolf[0] - 1 or sheep[0] == wolf[0] + 1) and (sheep[1] == wolf[1] - 1 or sheep[1] == wolf[1] + 1):
                        if matrix[wolf[0]-1][wolf[1]] == 1:
                            atMostFourRisk += 1
                        if matrix[wolf[0]+1][wolf[1]] == 1:
                            atMostFourRisk += 1
                        if matrix[wolf[0]][wolf[1]+1] == 1:
                            atMostFourRisk += 1
                        if matrix[wolf[0]][wolf[1]-1] == 1:
                            atMostFourRisk += 1 
                    #print("center")
        #score calculation session
        score -= countSheepNearby * 20
        if countCanEat > 1:
            if NumberOfSheep == 3:
                score += 280
            else:
                score += countCanEat * 15 * (16/NumberOfSheep+1) # set to 11 to avoid 10/0
        if countThreeBlockAway > 0:
            score += 15 - futureRisk * 7.5
        if atMostThreeRisk == 3:
            score -= 70
        else:
            score -= atMostThreeRisk * 10
        if atMostFourRisk == 4:
            score -= 70
        else:
            score -= atMostFourRisk * 7.5
        #score calculation ends
        
    #score convertion
    if turn == 'Sheep': #maximize sheep score
        score *= -1
    if yourRole != turn: #maximize score
        score *= -1
    #score convertion ends
    
    return score
        

def minimax(state, score, depth, alpha, beta, yourRole, turn):
    if depth == 0 or checkWinning(state) != 0:  #game over
        if depth == 0:
            return score + evaluationFunction(state,turn,yourRole)
        return score
    
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
        
        evaluatedScoreUntilThisBoard = score + evaluationFunction(simulationState, turn, yourRole)
        nextTurn = 'Who is next turn'
        if role == 2:
            nextTurn = 'Sheep'
        else:
            nextTurn = 'Wolf'
        currentScore = minimax(simulationState, evaluatedScoreUntilThisBoard, depth-1,alpha, beta, yourRole, nextTurn)
        
        
        if yourRole == turn: #player = current turn -> max
            bestScore = max(bestScore, currentScore)           
            alpha = max(alpha,bestScore)
            if alpha >= beta: #pruning
                break
        else: #player != current turn -> min
            bestScore = min(bestScore, currentScore)           
            beta = min(bestScore,currentScore)
            if alpha >= beta:
                break
    return bestScore

            
    
#THE WAY OF WRITING THE MINIMAX ALGO IS SIMILAR TO ASM 1 OF MINE, IT IS JUST A MINIMAX, JUST THE EVALUATION FUNCTION IS DIFFERENT
def next_move_wolf(matrix): # move for wolf
    availableMove = getAvailableMove(matrix, 'Wolf')

    bestMove = None
    bestScore = -math.inf
    
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
        EvaluatedScoreForThisBoard = evaluationFunction(simulationState, 'Wolf', 'Wolf')
        currentScore = minimax(simulationState, EvaluatedScoreForThisBoard, 10, alpha, beta, 'Wolf', 'Sheep')
        if currentScore >= bestScore:
            bestScore = currentScore
            bestMove = move 
        alpha = max(alpha, bestScore)

    return bestMove    
    
    

def next_move_sheep(matrix): # move for sheep
    availableMove = getAvailableMove(matrix, 'Sheep')
    bestMove = None
    bestScore = -math.inf #initializing bestScore
    
    alpha = -math.inf #initializing alpha and beta
    beta = math.inf
    
    for move in availableMove:
        simulationState = copy.deepcopy(matrix) #copy the board
        beforeMoveX = move[0]
        beforeMoveY = move[1] 
        afterMoveX = move[2]
        afterMovey = move[3] #available move
        simulationState[beforeMoveX,beforeMoveY] = 0
        simulationState[afterMoveX,afterMovey] = 1 #make the move
        EvaluatedScoreForThisBoard = evaluationFunction(simulationState, 'Sheep', 'Sheep') #evaluate the board
        currentScore = minimax(simulationState, EvaluatedScoreForThisBoard,0, alpha, beta,'Sheep', 'Wolf') #minimax
        if currentScore > bestScore: #update the score if it is better
            bestScore = currentScore
            bestMove = move #better move
        alpha = max(alpha, bestScore) #update alpha
    return bestMove 


#!!!DISCLAIMER!!!
################################################################
#I DID ALL THE THING BY MYSELF
#THE WAY OF WRITING THE MINIMAX ALGO IS SIMILAR TO ASM 1 OF MINE (NOT COPYING)
################################################################
#!!!DISCLAIMER!!!

def AIAlgorithm(filename, movemade): # a showcase for random walk
    iter_num=filename.split('/')[-1]
    iter_num=iter_num.split('.')[0]
    iter_num=int(iter_num.split('_')[1])
    matrix=load_matrix(filename)
    
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
