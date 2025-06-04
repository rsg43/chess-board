from ..chess import Chessboard, Piece, PieceType, Colour


class TestChessboard:

    @staticmethod
    def test_initialization():
        """
        Test the initialization of the chessboard.
        """
        board = Chessboard()
        assert board is not None
        assert len(board.board) == 8
        for row in board.board:
            assert len(row) == 8

    @staticmethod
    def test_setup_piece():
        """
        Test the setup of pieces on the chessboard.
        """
        board = Chessboard()
        board.setup_piece(PieceType.PAWN, Colour.WHITE, "e4")
        assert board.board[4][4] == Piece(
            colour=Colour.WHITE, piece_type=PieceType.PAWN
        )
        board.setup_piece(PieceType.KNIGHT, Colour.BLACK, "g6")
        assert board.board[2][6] == Piece(
            colour=Colour.BLACK, piece_type=PieceType.KNIGHT
        )

    @staticmethod
    def test_take_turn():
        """
        Test the taking of a turn on the chessboard.

        Note: ran out of time for this test, I would probably have restructured
        the code to make it easier to test, or used mocking to test the
        interaction with the player.
        """

    @staticmethod
    def test_get_coordinates_from_player():
        """
        Test the conversion of player coordinates to board coordinates.

        Note: ran out of time for this test, similarly to the take_turn test,
        I would probably used mocking to test the interaction with the player.
        """

    @staticmethod
    def test_validate_coordinates():
        """
        Test the validation of coordinates on the chessboard.
        """
        board = Chessboard()
        assert board.validate_coordinates("e4")
        assert board.validate_coordinates("h8")
        assert not board.validate_coordinates("i9")
        assert not board.validate_coordinates("a0")

    @staticmethod
    def test_validate_move():
        """
        Test the validation of moves on the chessboard. Covers cases where
        bishop takes a piece, is blocked, and is able to move, along with valid
        and invalid knight L moves.
        """
        board = Chessboard()
        board.setup_piece(PieceType.BISHOP, Colour.WHITE, "e2")
        board.setup_piece(PieceType.KNIGHT, Colour.BLACK, "d3")

        assert not board.validate_move(board.board[6][4], 4, 6, 2, 3)
        assert board.validate_move(board.board[6][4], 4, 6, 3, 5)
        assert not board.validate_move(board.board[6][4], 4, 6, 2, 4)
        assert board.validate_move(board.board[6][4], 4, 6, 5, 7)

        assert not board.validate_move(board.board[5][3], 3, 5, 3, 5)
        assert not board.validate_move(board.board[5][3], 3, 5, 3, 4)
        assert board.validate_move(board.board[5][3], 3, 5, 5, 6)
