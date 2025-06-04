from chess import Chessboard, PieceType, Colour


def main() -> None:
    board = Chessboard()
    board.setup_piece(PieceType.BISHOP, Colour.WHITE, "e2")
    board.setup_piece(PieceType.KNIGHT, Colour.BLACK, "d3")

    board.show()

    turns = 0
    while turns < 200:
        if turns % 2 == 0:
            colour = Colour.WHITE
        else:
            colour = Colour.BLACK

        if not board.take_turn(colour):
            continue

        board.show()
        turns += 1
    print("Maximum turns reached.")
    print("Game over!")


if __name__ == "__main__":
    main()
