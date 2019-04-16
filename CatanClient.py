import Catan
import argparse


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--numplayers",
        help="Set this to the number of players playing.",
        type=int,
        default=3)
    return parser


def main():
    parser = init_parser().parse_args()
    MyCatan = Catan.CatanGame(parser.numplayers)
    MyCatan.playGame()


if __name__ == "__main__":
    main()
