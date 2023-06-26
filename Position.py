import numpy as np


class Position:
    def __init__(self, code, finished, turn, res):
        self.board = self.board_from_code(code)
        self.game_over = finished
        self.turn = turn  # the turn that is to be played from this position
        self.result = res  # None if game is not over, string if it is or if only one outcome is possible

    @staticmethod
    def board_from_code(code):
        board = np.empty(9, dtype=str)  # blank board, use code to figure out the moves
        for i in range(9):  # up to 9 possible moves to decode
            if code % 3 == 1:
                board[i] = "x"
            elif code % 3 == 2:
                board[i] = "o"
            code = int((code - (code % 3)) / 3)
        return board

    def game_is_over(self):
        return self.game_over

    def get_turn(self):
        return self.turn

    def get_result(self):
        return self.result

    def set_result(self, res):
        self.result = res

    def has_result(self):
        if self.result is None:
            return False
        return True

    def get_available_moves(self):
        open_squares = np.empty(10 - self.turn, dtype=int)  # we know that turn - 1 moves have been made, so...
        # ... 9 - (turn - 1) = 10 - turn squares are empty
        cnt = 0  # index of open square for insertion into open_squares
        for sq in range(len(self.board)):
            if self.board[sq] == "":
                open_squares[cnt] = sq + 1  # convert sq (index) to integer between 1-9 representing a square
                cnt += 1
        return open_squares
