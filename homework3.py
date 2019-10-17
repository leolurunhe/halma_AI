import sys
import math
import time

class moveAction:
    def __init__(self, start, end):
        self.startX = start[0]
        self.startY = start[1]
        self.endX = end[0]
        self.endY = end[1]

class game:
    def __init__(self, size, color, board, time):
        self.size = size
        self.board = board
        self.color = color
        self.cur_player = 1
        self.color1 = color
        self.time = time
        if color == "BLACK":
            self.color2 = "WHITE"
            self.cur_player = 1 #black
        else:
            self.color2 = "BLACK"
            self.cur_player = -1 #white
        self.camps = []
        for i in range(0, self.size):
            self.camps.append([])
            for j in range(0, self.size):
                self.camps[i].append(0)
        for i in range(0, 5):
            for j in range(0,2):
                self.camps[i][j] = 1 #black
        for i in range(0,4):
            self.camps[i][2] = 1
        for i in range(0,3):
            self.camps[i][3] = 1
        for i in range(0,2):
            self.camps[i][4] = 1
        for i in range(11,16):
            for j in range(14, 16):
                self.camps[i][j] = -1 #white
        for i in range(12, 16):
            self.camps[i][13] = -1
        for i in range(13, 16):
            self.camps[i][12] = -1
        for i in range(14, 16):
            self.camps[i][11] = -1
        
    def isValid(self, startx, starty, endx, endy):
        '''
        Check if (endx, endy) is valid to go
        '''
        if endx < 0 or endy < 0 or endx>=self.size or endy>=self.size:
            return False
        if self.camps[startx][starty] != self.cur_player and self.camps[endx][endy] == self.cur_player: #jump back to camp
            return False
        return True
    
    def isOneInsideCamp(self):
        '''
        Check if there is one chess in camp
        '''
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == self.cur_player and self.camps[i][j] == self.cur_player:
                    return True
        return False

    def dfs(self, moves, x, y, depth):
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i==0 and j==0:
                    continue
                if self.isValid(x, y, x+i, y+j):
                    if self.board[x+i][y+j] != 0:
                        if self.isValid(x, y, x+i*2, y+j*2) and self.board[x+i*2][y+j*2] == 0:
                            if (x+2*i, y+2*j) in moves:
                                continue
                            moves.add((x+2*i, y+2*j))
                            self.dfs(moves, x+2*i, y+2*j, depth+1)
                else:
                    continue

    def find_moves(self, x, y):
        '''
        Find possible moves for chess at (x, y)
        '''
        moves = set()
        if self.camps[x][y] != 0 and self.camps[x][y] != self.cur_player: #in op camp
            return moves
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i==0 and j==0:
                    continue
                if self.isValid(x, y, x+i, y+j):
                    
                    if self.board[x+i][y+j] == 0:
                        moves.add((x+i, y+j))
                    else:
                        if x== 9 and y == 9:
                            print(self.isValid(x, y, x+i*2, y+j*2))
                        if self.isValid(x, y, x+i*2, y+j*2) and self.board[x+i*2][y+j*2] == 0:
                            moves.add((x+i*2, y+j*2))
                            self.dfs(moves, x+i*2, y+j*2, 1)
        
        return moves

    def find_all_moves(self, player, state):
        '''
        Find all legal moves
        '''
        res = []
        
        if not self.isOneInsideCamp():
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == player:
                        if self.camps[i][j] != 0 and self.camps[i][j] != player:
                            #in op camp
                            continue
                        moves = self.find_moves(i, j)
                        
                        for move in moves:
                            action = moveAction((i, j), move)
                            res.append((action, self.getNextBoard(action, state)))
            return res
        else:
            for i in range(self.size):
                for j in range(self.size):
                    if self.camps[i][j] == player and self.board[i][j] == player:
                        moves = self.find_moves(i, j)
                        for move in moves:
                            if self.camps[move[0]][move[1]] != player:
                                action = moveAction((i, j), move)
                                res.append((action, self.getNextBoard(action, state)))
            if len(res) != 0:
                return res
            else:
                cornor = (0,0)
                if self.cur_player == 1:
                    cornor = (15,15)
                for i in range(self.size):
                    for j in range(self.size):
                        if self.camps[i][j] == player and self.board[i][j] == player:
                            moves = self.find_moves(i, j)
                            for move in moves:
                                endX = move[0]
                                endY = move[1]
                                cornorX = cornor[0]
                                cornorY = cornor[1]
                                originalDis = math.fabs(i-cornorX) + math.fabs(j-cornorY)
                                newDis = math.fabs(endX-cornorX) + math.fabs(endY-cornorY)
                                if newDis <= originalDis:
                                    continue
                                action = moveAction((i, j), move)
                                res.append((action, self.getNextBoard(action, state)))
                return res
        return res

    
    
    def ifWin(self, state=None):
        # black win
        winCheck = 0
        if not state:
            state = self.board
        realWin = False
        for i in range(self.size):
            for j in range(self.size):
                if self.camps[i][j] == -1 and state[i][j] != 0:
                    winCheck += 1
                    if state[i][j] == 1:
                        realWin = True
        if winCheck == 19 and realWin:
            return True
        # white win:
        winCheck = 0
        realWin = False
        for i in range(self.size):
            for j in range(self.size):
                if self.camps[i][j] == 1 and state[i][j] != 0:
                    winCheck += 1
                    if state[i][j] == -1:
                        realWin = True
        return winCheck == 19 and realWin

    def getNextBoard(self, move, state):
        nextBoard = [[0 for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                nextBoard[i][j] = state[i][j]
        nextBoard[move.startX][move.startY] = 0
        nextBoard[move.endX][move.endY] = state[move.startX][move.startY]
        return nextBoard

    def eval_fn(self, board, player):
            goal_x = 0
            goal_y = 0
            if player == 1: #black
                goal_x = 15
                goal_y = 15
            score = 0
            for i in range(16):
                for j in range(16):
                    if board[i][j] == player:
                        score += abs(goal_x-i) + abs(goal_y-j)
            return -score

def abSearch(game, depth):
    test = lambda state, d: game.time > 20 or d > depth or game.ifWin(state)
    eval_fn = game.eval_fn
    def maxVal(state, a, b, depth):
        if test(state, depth):
            return eval_fn(state, game.cur_player)
        v = -float("inf")
        futureMoves = game.find_all_moves(game.cur_player, state)
        for (action, futureBoard) in futureMoves:
            v = max(v, minVal(futureBoard, a, b, depth+1))
            if v >= b:
                return v
            a = max(a, v)
        return v
    def minVal(state, a, b, depth):
        opponent = 1
        if game.cur_player == 1:
            opponent = -1
        if test(state, depth):
            return eval_fn(state, game.cur_player)
        v = float("inf")
        futureMoves = game.find_all_moves(opponent, state)
        for (action, futureBoard) in futureMoves:
            v = min(v, maxVal(futureBoard, a, b, depth+1))
            if v <= a:
                return v
            b = min(b, v)
        return v
    next = game.find_all_moves(game.cur_player, game.board)
    bestMove = next[0]
    bestScore = minVal(bestMove[1], -float("inf"), float("inf"), 0)
    for temp in next[1:]:
        tempScore = minVal(temp[1], -float("inf"), float("inf"), 0)
        
        if tempScore >= bestScore:
            bestMove, bestScore = temp, tempScore
            #print(bestMove[0].endX, bestMove[0].endY, bestScore)
    return bestMove[0]

    

def main():
    inputFile = "input.txt"
    gameType = ""
    color = ""
    totalTime = 0
    board = []
    with open(inputFile, "r") as f:
        lineNum = 1
        for line in f.readlines():
            line = line.strip()
            if lineNum == 1:
                gameType = line
            elif lineNum == 2:
                color = line
            elif lineNum == 3:
                totalTime = float(line)
            elif lineNum >= 4 and lineNum <= 19:
                board.append(line)
            lineNum += 1
    f.close()

    realBoard = [[0 for i in range(16)] for j in range(16)]
    #print(len(board), len(board[0]))
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[j][i] == "B"):
                realBoard[i][j] = 1
            elif(board[j][i] == "W"):
                realBoard[i][j] = -1
    #print(realBoard[10][0])
    newGame = game(16, color, realBoard, totalTime)

    if gameType == "SINGLE":
        if not newGame.isOneInsideCamp():
            moves = set()
            for i in range(16):
                for j in range(16):
                    if realBoard[i][j] == newGame.cur_player:
                        if newGame.camps[i][j] != 0 and newGame.camps[i][j] != newGame.cur_player:
                            #in op camp
                            continue
                        moves = newGame.find_moves(i, j)
                        moveToX = 0
                        moveToY = 0
                        for key in moves:
                            moveToX = key[0]
                            moveToY = key[1]
                            break
                        temp = "J "
                        for m in range(-1, 2):
                            for n in range(-1, 2):
                                if i+m == moveToX and j+n == moveToY:
                                    temp = "E "
                                    break
                        #if temp == "E ": continue
                        with open("output.txt", "w") as f:
                            f.write(temp + str(i) + "," + str(j) + " " + str(moveToX) + "," + str(moveToY))
                        f.close()
                        pass             
        else:
            for i in range(16):
                for j in range(16):
                    if newGame.camps[i][j] == newGame.cur_player and realBoard[i][j] == newGame.cur_player:
                        moves = newGame.find_moves(i, j)
                        for move in moves:
                            moveToX = move[0]
                            moveToY = move[1]
                            if newGame.camps[move[0]][move[1]] != newGame.cur_player:
                                temp = "J "
                                for m in range(-1, 2):
                                    for n in range(-1, 2):
                                        if i+m == moveToX and j+n == moveToY:
                                            temp = "E "
                                            break
                                with open("output.txt", "w") as f:
                                    f.write(temp + str(i) + "," + str(j) + " " + str(moveToX) + "," + str(moveToY))
                                f.close()
                                pass 
            cornor = (15,15)
            if newGame.cur_player == 1:
                cornor = (0,0)
            for i in range(16):
                for j in range(16):
                    if newGame.camps[i][j] == newGame.cur_player and realBoard[i][j] == newGame.cur_player:
                        moves = newGame.find_moves(i, j)
                        for move in moves:
                            endX = move[0]
                            endY = move[1]
                            cornorX = cornor[0]
                            cornorY = cornor[1]
                            originalDis = math.fabs(i-cornorX) + math.fabs(j-cornorY)
                            newDis = math.fabs(endX-cornorX) + math.fabs(endY-cornorY)
                            if newDis <= originalDis:
                                continue
                            else:
                                temp = "J "
                                for m in range(-1, 2):
                                    for n in range(-1, 2):
                                        if i+m == moveToX and j+n == moveToY:
                                            temp = "E "
                                            break
                                with open("output.txt", "w") as f:
                                    f.write(temp + str(i) + "," + str(j) + " " + str(endX) + "," + str(endY))
                                f.close()
                                pass
    else:
        nextMove = abSearch(newGame, 5)
        print(nextMove.startX, nextMove.startY, nextMove.endX, nextMove.endY)


if __name__ == "__main__":
    main()

        


                


