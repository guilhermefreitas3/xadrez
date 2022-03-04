import chess
from random import sample

class Player():
  PIECE_WEIGHTS = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
  }

  WHITE_COLOR = True
  BLACK_COLOR = False

  RANDOM_STRATEGY = 0
  MINIMAX_STRATEGY = 1

  MINIMAX_DEPTH = 4

  def __init__(self, color, is_bot, strategy=None) -> None:
    self.color = color
    self.is_bot = is_bot
    self.strategy = strategy
    self.move_stack = []

  def move(self, board) -> chess.Move:
    if not self.is_bot:
      try:
        position = input("\nMake a move\n")
        movement = chess.Move.from_uci(position)
      except ValueError:
        print("Invalid move. Try again.")
    elif self.strategy == Player.RANDOM_STRATEGY:
      movement = self.random_move(board)
    elif self.strategy == Player.MINIMAX_STRATEGY:
      movement = self.minimax_root(board, Player.MINIMAX_DEPTH, True)
    self.move_stack.append(movement.uci())
    return movement

  def random_move(self, board) -> chess.Move:
    return sample(list(board.legal_moves), 1).pop()

  def minimax_root(self, board, depth, maximizing_player) -> chess.Move:
    best_move = None
    best_value = alpha = -float('inf')
    beta = float('inf')

    for movement in board.legal_moves:
      board.push(movement)
      value = max(best_value, self.minimax(board, alpha, beta, depth - 1, not maximizing_player))
      board.pop()
      if value > best_value:
        best_move = movement
        best_value = value

    if self.move_stack.count(best_move.uci()) >= 3:
      self.move_stack = []
      return self.random_move(board)
    return best_move

  def minimax(self, board, alpha, beta, depth, maximizing_player) -> int:
    if depth == 0 or board.is_game_over():
      return self.evaluate(board)
    if maximizing_player:
      value = alpha
      for movement in board.legal_moves:
        board.push(movement)
        value = max(value, self.minimax(board, alpha, beta, depth - 1, False))
        board.pop()
        alpha = max(alpha, value)
        if beta <= alpha:
          return value
      return value
    else:
      value = beta
      for movement in board.legal_moves:
        board.push(movement)
        value = min(value, self.minimax(board, alpha, beta, depth - 1, True))
        board.pop()
        beta = min(beta, value)
        if beta <= alpha:
          return value
      return value

  def evaluate(self, board) -> int:
    points = 0
    for square in chess.SQUARES:
      piece = board.piece_at(square)
      if not piece:
        continue
      if piece.color == self.color:
        points += Player.PIECE_WEIGHTS[piece.piece_type]
      else:
        points -= Player.PIECE_WEIGHTS[piece.piece_type]
    return points
