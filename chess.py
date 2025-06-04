"""
Module for a simple chess game implementation. Provides classes and functions
to represent a chessboard, pieces, and their movements. The chessboard is an
8x8 grid where each square can either be empty or occupied by a piece.

The chessboard supports setting up pieces, displaying the board, and taking
turns for players to move their pieces. The pieces are represented by their
initials (e.g. "WB" for white bishop, "BN" for black knight).

The chess pieces are defined by the Piece class, which includes the colour and
type of the piece. The PieceType and Colour enumerations define the types of
pieces (e.g. pawn, rook, knight) and the colours of the pieces (white or
black). Each piece type has its own movement rules, which are validated when a
player attempts to move a piece.

Currently, only the knight and bishop movement rules are implemented. The
knight moves in an "L" shape, while the bishop moves diagonally any number of
squares, so long as there are no obstacles in the way.

The chessboard also includes a method to validate the coordinates of a piece on
the board, ensuring that they are within the valid range (a1 to h8). The
coordinates are represented in standard chess notation (e.g. "e4"), where the
first character represents the x-coordinate and the second character represents
the y-coordinate (https://en.wikipedia.org/wiki/Algebraic_notation_(chess)).
"""

from enum import Enum
from typing import Optional
from dataclasses import dataclass

X_NOTATION_TO_INT = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}
INT_TO_X_NOTATION = {v: k for k, v in X_NOTATION_TO_INT.items()}

Y_NOTATION_TO_INT = {
    "1": 7,
    "2": 6,
    "3": 5,
    "4": 4,
    "5": 3,
    "6": 2,
    "7": 1,
    "8": 0,
}
INT_TO_Y_NOTATION = {v: k for k, v in Y_NOTATION_TO_INT.items()}


class Colour(Enum):
    """
    An enumeration representing the colours of chess pieces.
    """

    WHITE = "White"
    BLACK = "Black"


class PieceType(Enum):
    """
    An enumeration representing the types of chess pieces.
    """

    PAWN = "Pawn"
    ROOK = "Rook"
    KNIGHT = "Knight"
    BISHOP = "Bishop"
    QUEEN = "Queen"
    KING = "King"


DISPLAYED_PIECE_TYPES = {
    PieceType.PAWN: "P",
    PieceType.ROOK: "R",
    PieceType.KNIGHT: "N",
    PieceType.BISHOP: "B",
    PieceType.QUEEN: "Q",
    PieceType.KING: "K",
}


@dataclass(frozen=True, kw_only=True)
class Piece:
    """
    A class representing a chess piece.

    :param colour: The colour of the piece (white or black).
    :type colour: Colour
    :param piece_type: The type of the piece (e.g. pawn, rook, knight).
    :type piece_type: PieceType
    """

    colour: Colour
    piece_type: PieceType


class Chessboard:
    """
    A class representing a chessboard. The chessboard is an 8x8 grid
    where each square can either be empty or occupied by a piece.
    The chessboard supports setting up pieces, displaying the board,
    and taking turns for players to move their pieces.
    """

    def __init__(self) -> None:
        self.board: list[list[Optional[Piece]]] = [
            [None] * 8 for _ in range(8)
        ]

    def setup_piece(
        self, piece_type: PieceType, colour: Colour, coord: str
    ) -> None:
        """
        Set up a piece on the chessboard at the given coordinates.

        :param piece_type: The type of the piece to set up.
        :type piece_type: PieceType
        :param colour: The colour of the piece to set up.
        :type colour: Colour
        :param coord: The coordinates to set up the piece at, using standard
            chess notation (e.g. "e4").
        :type coord: str
        :raises ValueError: If the piece type, colour, or coordinates are
            invalid, or spot already occupied.
        """
        if not isinstance(piece_type, PieceType):
            raise ValueError("Invalid piece type")
        if not isinstance(colour, Colour):
            raise ValueError("Invalid colour")
        if not self.validate_coordinates(coord):
            raise ValueError("Invalid coordinates")

        x = X_NOTATION_TO_INT[coord[0]]
        y = Y_NOTATION_TO_INT[coord[1]]
        if self.board[y][x] is not None:
            raise ValueError("Position already occupied")

        self.board[y][x] = Piece(colour=colour, piece_type=piece_type)

    def show(self) -> None:
        """
        Show the chessboard in a human-readable format in the console.
        The board is displayed with the pieces represented by their
        initials (e.g. "WB" for white bishop, "BN" for black knight).
        """
        print("  " + "-" * 41)
        for i, row in enumerate(self.board):
            print(
                f"{INT_TO_Y_NOTATION[i]} | "
                + " | ".join(
                    (
                        piece.colour.value[0]
                        + DISPLAYED_PIECE_TYPES[piece.piece_type]
                        if piece
                        else "  "
                    )
                    for piece in row
                )
                + " |"
            )
            print("  " + "-" * 41)
        print("    " + "    ".join(INT_TO_X_NOTATION.values()))
        print("\n")

    def take_turn(self, colour: Colour) -> bool:
        """
        Take a turn for the given colour. The player is prompted to enter
        the coordinates of the piece to move and the coordinates of the
        destination. The move is validated and executed if valid.

        :param colour: The colour of the player taking the turn.
        :type colour: Colour
        :return: True if the turn was successful, False otherwise.
        :rtype: bool
        """
        print(f"{colour.value}'s turn")
        print("Enter the coordinates of the piece to move (e.g. a4):")
        x, y = self.get_coordinates_from_player()

        piece = self.board[y][x]
        if piece is None:
            print("No piece at that position")
            return False
        if piece.colour != colour:
            print("You cannot move your opponent's piece")
            return False

        print("Where do you want to move it? (e.g. a5)")
        new_x, new_y = self.get_coordinates_from_player()

        new_position = self.board[new_y][new_x]
        if new_position is not None and colour == new_position.colour:
            print("You cannot move to a position occupied by your own piece")
            return False
        if (new_x, new_y) == (x, y):
            print("You must move the piece to a different position")
            return False
        if not self.validate_move(piece, x, y, new_x, new_y):
            print("Invalid move for this piece")
            return False

        self.board[new_y][new_x] = piece
        self.board[y][x] = None

        print(
            f"Moved {piece.colour.value} {piece.piece_type.value} "
            + f"from ({x}, {y}) to ({new_x}, {new_y})"
        )
        return True

    def get_coordinates_from_player(self) -> tuple[int, int]:
        """
        Get the coordinates from the player in standard chess notation.

        :raises ValueError: If the coordinates are invalid.
        :return: The coordinates as a tuple of (x, y) indexes.
        :rtype: tuple[int, int]
        """
        notation = input("Coordinates: ").strip().lower()
        if not self.validate_coordinates(notation):
            raise ValueError("Invalid coordinates")

        x = X_NOTATION_TO_INT[notation[0]]
        y = Y_NOTATION_TO_INT[notation[1]]
        return x, y

    def validate_coordinates(self, coords: str) -> bool:
        """
        Validate the coordinates of a piece on the chessboard.

        :param coords: The coordinates to validate, using standard chess
            notation (e.g. "e4").
        :type coords: str
        :return: True if the coordinates are valid, False otherwise.
        :rtype: bool
        """
        if len(coords) != 2:
            return False
        if coords[0] not in X_NOTATION_TO_INT:
            return False
        if coords[1] not in Y_NOTATION_TO_INT:
            return False
        return True

    def validate_move(
        self, piece: Piece, x: int, y: int, new_x: int, new_y: int
    ) -> bool:
        """
        Validate the move of a piece based on its type. Note, coordinates here
        are indexes of the board, not chess notation.

        :param piece: The piece to move.
        :type piece: Piece
        :param x: The current x-coordinate of the piece.
        :type x: int
        :param y: The current y-coordinate of the piece.
        :type y: int
        :param new_x: The new x-coordinate of the piece.
        :type new_x: int
        :param new_y: The new y-coordinate of the piece.
        :type new_y: int
        :raises NotImplementedError: If the piece type is not implemented.
        :return: True if the move is valid, False otherwise.
        :rtype: bool
        """
        if piece.piece_type == PieceType.KNIGHT:
            return (abs(x - new_x) == 2 and abs(y - new_y) == 1) or (
                abs(x - new_x) == 1 and abs(y - new_y) == 2
            )
        elif piece.piece_type == PieceType.BISHOP:
            if not abs(x - new_x) == abs(y - new_y):
                return False

            if x < new_x and y < new_y:
                xs = list(range(x + 1, new_x))
                ys = list(range(y + 1, new_y))
            else:
                xs = list(range(new_x + 1, x))
                ys = list(range(new_y + 1, y))

            for x, y in zip(xs, ys):
                if self.board[y][x] is not None:
                    return False

            return True
        else:
            raise NotImplementedError(
                f"Validation for {piece.piece_type.value} not implemented"
            )
