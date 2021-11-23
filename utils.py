import time
from copy import deepcopy
import numpy as np
from numpy.core.numeric import count_nonzero

from wincons import return_winners


class Position():
    def __init__(self, board = None) -> None:
        self.width: int = 7
        self.height: int = 6
        if board is not None:
            self.board = board
        else:
            self.board = np.tile(0, (self.width, self.height))
        self.nbMoves = int(count_nonzero(board))
            
    def changeOver(self) -> None:
        """Changes the player who is in control. 
        This is effectively a visual change for the board"""
        self.board = -self.board
        
    def canPlay(self, col: int) -> bool:
        """Checks whether a column is playable.
        Input: column index from 0 to width
        Output: True if playable, False otherwise"""
        if self.board[col].dot(self.board[col]) >= self.height:
            return False
        else:
            return True
        
    def play(self, col: int) -> None:
        """Plays a specific column. Should only be called on a playable column.
        Input: column index from 0 to width"""
        i=0
        while self.board[col][i] != 0:
            i += 1
        self.board[col][i] = 1
        self.nbMoves += 1
        self.changeOver()
    
    def isWinningMove(self, col: int) -> bool:
        """Checks whether playing in a column in a winning move.
        Does this via a lookup in the wincons file and the set function.
        Input: column index from 0 to width
        Output: True is winning, False otherwise"""
        matches = return_winners(col)
        i=0
        b2 = self.board
        while self.board[col][i] != 0:
            i += 1
        self.board[col][i] = 1
        for m in matches:
            if set([self.board[m[i][0]][m[i][1]] for i in range(0,4)]) == {1}:
                self.board[col][i] = 0
                return True
        self.board[col][i] = 0
        return False
    
    def isWinningMove2(self, col: int) -> bool:
        """Checks whether playing in a column in a winning move.
        Does this by looking at any potential fours on the tile a piece is placed.
        Seems to be faster when there are a large number of tests to do.
        Input: column index from 0 to width
        Output: True is winning, False otherwise"""
        
        i=0
        while self.board[col][i] != 0:
            i += 1
        self.board[col][i] = 1
        b2 = np.pad(self.board, 3, mode='constant')
        self.board[col][i] = 0
        row = i + 3
        col += 3
        # Horizontally sloped cols
        for i in range(-3,1):
                if b2[col+i][row] + b2[col+i+1][row] + b2[col+i+2][row] + b2[col+i+3][row] == 4:
                    return True
    
        # Check vertical locations for win
        for i in range(-3,1):
                if b2[col][row+i] + b2[col][row+i+1] + b2[col][row+i+2] + b2[col][row+i+3] == 4:
                    return True
    
        # Check positively sloped diaganols
        for i in range(-3,1):
                if b2[col+i][row+i] + b2[col+i+1][row+i+1] + b2[col+i+2][row+i+2] + b2[col+i+3][row+i+3] == 4:
                    return True
    
        # Check negatively sloped diaganols
        for i in range(-3,1):
                if b2[col-i][row+i] + b2[col-i-1][row+i+1] + b2[col-i-2][row+i+2] + b2[col-i-3][row+i+3] == 4:
                    return True

        return False
