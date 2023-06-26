import numpy as np
from Trainer import Trainer
from Position import Position


class Game:
    def __init__(self, game_mode, train):
        self.finished = False
        self.moves = np.zeros(9, dtype=int)  # up to 9 moves possible in tic tac toe
        self.game_board = np.empty(9, dtype=str)  # will be filled with x and o
        self.move_cnt = 0
        self.res = None  # will be changed to x, d or o
        self.ai_is_X = True  # will be changed when game starts if AI is o
        self.ai_turn = True  # will be changed when game starts if AI is o
        self.mode = game_mode
        self.trainer = Trainer(game_mode)
        self.training_mode = train  # True if ai plays itself, false if it plays user

    def display_board(self):
        print(self.game_board[0:3])
        print(self.game_board[3:6])
        print(self.game_board[6:9])

    def assign_players(self):
        if not self.training_mode:
            user_role = input("Would you like to play as x or o? ")
            if user_role == "x":
                self.ai_is_X = False
                self.ai_turn = False

    def update_game_params(self, new_move):
        # add the new move to the board and list of moves
        # new_move is an integer from 1-9 representing a square
        if self.ai_turn == self.ai_is_X:  # ai is x played or ai is o and didn't play
            self.game_board[new_move - 1] = "x"  # convert new_move to index
        else:
            self.game_board[new_move - 1] = "o"  # convert new_move to index

        # update moves, move_cnt and ai_turn
        self.moves[self.move_cnt] = new_move
        self.move_cnt += 1
        self.ai_turn = not self.ai_turn

    def fix_user_input(self):
        try:
            user_move = int(input("What square would you like to play next?: "))
            if user_move < 1 or user_move > 9:  # will cause index out of bounds error later
                print("Input must be an integer between 1 and 9. ")
                self.fix_user_input()
            elif user_move in self.moves:  # move has already been played
                print("That move has already been played. ")
                self.fix_user_input()
            else:
                self.update_game_params(user_move)
        except TypeError:
            print("Input must be an integer between 1 and 9. ")
            self.fix_user_input()

    def code_from_board(self):
        c = 0
        for i in range(len(self.game_board)):
            if self.game_board[i] == "x":
                c += 3**i
            elif self.game_board[i] == "o":
                c += 2 * (3**i)
        return c

    def play_turn(self, data):
        pos_code = self.code_from_board()  # retrieve code for position shown on the game board
        # we don't want to create a new position object for the game_board because it would not have the data loaded
        # by self.trainer, which is the outcome associated with the position
        try:
            pos = data[pos_code]
        except KeyError:
            # now we can create a new position object since this is a new position and there is no data on it yet
            pos = Position(pos_code, False, self.move_cnt + 1, None)
            # we can assume this is not a final position because the check_game_status method would have flipped
            # self.finished to true and ended the while loop, so this code would not have been reached
        if not self.training_mode and not self.ai_turn:  # user makes a new move
            self.display_board()  # allow the user to see the new game board
            self.fix_user_input()
        else:  # ai makes a new move
            new_move = self.trainer.choose_move(pos_code, pos, self.ai_is_X)
            self.update_game_params(new_move)
            if self.training_mode:
                self.ai_turn = True  # always ai_turn
                # ai starts as x, but has to change to o on the next turn and alternate
                self.ai_is_X = not self.ai_is_X

    def check_for_win(self, plyr):
        # plyr is true or false, true means check if x won, false means check if o won
        if self.game_board[0] == plyr:  # played in square 1
            if self.game_board[1] == plyr:  # played in square 2
                if self.game_board[2] == plyr:  # X played in square 3
                    return True
            if self.game_board[3] == plyr:  # played in square 4
                if self.game_board[6] == plyr:  # played in square 7
                    return True
            if self.game_board[4] == plyr:  # played in square 5
                if self.game_board[8] == plyr:  # played in square 9
                    return True
        if self.game_board[1] == plyr:  # played in square 2
            if self.game_board[4] == plyr:  # played in square 5
                if self.game_board[7] == plyr:  # played in square 8
                    return True
        if self.game_board[2] == plyr:  # played in square 3
            if self.game_board[5] == plyr:  # played in square 6
                if self.game_board[8] == plyr:  # played in square 9
                    return True
            if self.game_board[4] == plyr:  # played in square 5
                if self.game_board[6] == plyr:  # played in square 7
                    return True
        if self.game_board[3] == plyr:  # played in square 4
            if self.game_board[4] == plyr:  # played in square 5
                if self.game_board[5] == plyr:  # X played in square 6
                    return True
        if self.game_board[6] == plyr:  # played in square 7
            if self.game_board[7] == plyr:  # played in square 8
                if self.game_board[8] == plyr:  # X played in square 9
                    return True
        return False

    def check_game_status(self):
        self.finished = self.check_for_win("x")  # check if x won
        if self.finished:
            self.res = "x"
        else:
            self.finished = self.check_for_win("o")  # check if o won
            if self.finished:
                self.res = "o"
            elif self.move_cnt == 9:  # check if thew drew
                self.finished = True
                self.res = "d"

    def announce_winner(self):
        if self.res == "d":
            print("Draw.")
        elif (self.ai_is_X and self.res == "x") or ((not self.ai_is_X) and self.res == "o"):
            print("AI wins!")
        else:
            print("User wins!")

    def play_game(self):
        self.assign_players()  # determine who is x and o
        data = self.trainer.code_to_pos

        while not self.finished:
            # play a turn
            self.play_turn(data)

            # check if game is over
            self.check_game_status()  # will adjust finished value to True if game is over, breaks while loop

        if not self.training_mode:
            self.announce_winner()

    def catalog_game(self):
        final_code = self.code_from_board()
        final_pos = Position(final_code, True, self.move_cnt + 1, self.res)
        self.trainer.learn_from_game(final_pos, final_code, True)
