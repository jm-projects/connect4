import numpy as np

class Position():
    def __init__(self, board = []) -> None:
        self.width = 7
        self.height = 6
        self.nbMoves = 0
        if board == []:
            self.board = np.tile(0, (self.width, self.height))
        else:
            self.board = board
            
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
        Input: column index from 0 to width
        Output: True is winning, False otherwise"""
        
            
def negamax(P: Position) -> int:
    """Recursivley solves connect4 via a min/max algorithm.
    Input: Position class
    Output: Integer score n. 
        n = 0 -> draw
        n = k > 0 -> player1 wins with nth to last stone.
        n = k < 0 -> player2 wins with nth to last stone.
    Note if player 1 has score n, player 2 has score -n"""
    
    b = P.height*P.width
    if P.nbMoves() == b:
        return 0
    
    for i in range(0,P.width):
        if P.canPlay(i) and P.isWinningMove(i):
            return (b + 1 - P.nbMoves())/2
    
    bestScore = -b

    for i in range(0, P.width):
        if P.canPlay(i):
            P2 = Position(board = P.board)
            P2.play(i)
            score = -negamax(P2)
            if score > bestScore:
                score = bestScore
    
    return bestScore
