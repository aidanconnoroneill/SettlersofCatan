# import catan.board
# import catan.game
# import catan.trading

from Catan import CatanGame
from Catan import Player
from Catan import Road
from Catan import Tile
import CatanVertex
import BoardState

def main():

    players = [
        Player("Ross"),
        Player("Josh"),
        Player("Yuri"),
        Player("Zach")]

    Catan1 = CatanGame(4)

    Catan1.insertPlayers(players)

    Catan1.playGame()


    # Actions on a turn:

    # Always must roll for resource production (applies to all players)
        # Each person with a settlement/city on an intersection that borders
        # a terrain hex with the rolled number gets resources
        # each settlement gets 1 card, each city gets 2 cards
    # Build a road
        # requires brick and lumber
    # Build a settlement
        # requires brick, lumber, wool, and grain
    # Build a city
        # requires 3 ore, 2 grain
    # Buy development card
        # requires ore, wool, grain
    # Use development card

if __name__ == "__main__":
    main()

# board = catan.board.Board()
# game = catan.game.Game(board=board)
# game.start(players=players)
# print(game.get_cur_player())  # -> ross (red)
# game.buy_settlement(0x37)
# game.buy_road(0x37)
# game.end_turn()
# game.roll(6)
# game.end()
