from player import Player
from game import Game
import os

def clear_stdout() -> None:
  os.system('cls' if os.name == 'nt' else 'clear')

def set_player(color) -> Player:
  clear_stdout()
  output_color = "white" if color == Player.WHITE_COLOR else "black"
  player_kind = input("Choose " + output_color + " player:\n1. Bot\n2. Player\n")

  is_bot = True if player_kind == "1" else False
  strategy = None

  if is_bot:
    strategy_kind = input("Choose bot strategy:\n1. Random\n2. Minimax\n")
    strategy = Player.RANDOM_STRATEGY if strategy_kind == "1" else Player.MINIMAX_STRATEGY

  return Player(color, is_bot, strategy)

def main():
  match = Game()
  match.white_player = set_player(Player.WHITE_COLOR)
  match.black_player = set_player(Player.BLACK_COLOR)

  while True:
    clear_stdout()
    print(match)

    if match.board.is_game_over():
      break

    player = match.current_player()
    position = player.move(match.board)
    match.push(position)

if __name__ == "__main__":
    main()
