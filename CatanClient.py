import Catan
import argparse


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--numplayers",
        help="Set this to the number of players playing.",
        type=int,
        default=3,
    )
    return parser


def main():
    parser = init_parser().parse_args()
    players = []
    for i in range(0, 3):
        players.append(Catan.Player("Player" + str(i)))
    MyCatan = Catan.CatanGame(parser.numplayers, players)
    MyCatan.playGame()


if __name__ == "__main__":
    main()
