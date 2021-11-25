from copy import deepcopy
from utils import Position

def negamax(P: Position) -> int:
    """Recursivley solves connect4 via a min/max algorithm.
    Input: Position class
    Output: Integer score n. 
        n = 0 -> draw
        n = k > 0 -> player1 wins with nth to last stone.
        n = k < 0 -> player2 wins with nth to last stone.
    Note if player 1 has score n, player 2 has score -n"""
    
    b: int = P.height*P.width

    # Returning 0 for a draw
    if P.nbMoves == b: 
        return 0
    
    # Returning score when there is a winning next move
    for i in range(0,P.width):
        if P.canPlay(i) and P.isWinningMove(i):
            winning_score: int = (b+1-P.nbMoves)//2
            return winning_score

    bestScore: int = -b

    # Make moves and recursively calculate the board positions score for that move
    for i in range(0, P.width):
        if P.canPlay(i):
            P2 = deepcopy(Position(board=P.board))
            P2.play(i)
            score: int = -negamax(P2)
            if score > bestScore:
                bestScore = score

    return bestScore


def negamaxpruning(P: Position, alpha: int, beta: int) -> int:
    """Negamax method but with alpha-beta pruning to discard certain 
    branches for the sake of a faster runtime"""
    col_order = [3,2,4,1,5,0,6]
    b: int = P.height*P.width

    # Returning 0 for a draw
    if P.nbMoves == b: 
        return 0
    
    # Returning score when there is a winning next move
    for i in range(P.width):
        if P.canPlay(i) and P.isWinningMove(i):
            winning_score: int = (b+1-P.nbMoves)//2
            return winning_score
        
    max: int = (b-1-P.nbMoves)//2;	# Upper bound to the score as we cannot win next move
    if beta > max:
        beta = max
        if alpha >= beta:
            return beta  # Prune if the alpha-beta interval is empty

    for i in range(P.width):
        if P.canPlay(col_order[i]):
            P2 = deepcopy(Position(board=P.board))
            P2.play(col_order[i])
            score: int = -negamaxpruning(P2, -beta, -alpha)

            if score >= beta:
                return score

            elif score > alpha:
                alpha = score

    return alpha
