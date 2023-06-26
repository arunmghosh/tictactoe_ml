import pandas as pd
import numpy as np
import math
import random
from Position import Position


class Trainer:
    def __init__(self, game_mode):
        self.source = "TicTacToeAI.xlsx"  # spreadsheet
        self.mode = game_mode  # 0 for traditional, 1 for reverse
        self.data = pd.read_excel(self.source, sheet_name=0)
        self.code_to_pos = dict()  # retrieve the position object using the integer code
        # directory of positions encoded by integer values
        # a position in which the game is over will have a string value of the result
        # directory organized numerically (least to greatest value)
        self.format_data()

    @staticmethod
    def encode_new_move(sq, turn):
        new_move = 3**(sq - 1) * (2 - (turn % 2))
        return new_move

    def catalog_pos(self, code, pos):
        self.code_to_pos[code] = pos

    def process_entry(self, code, outcome, finished):
        board = Position.board_from_code(code)
        turn = 10
        for sqr in board:
            if sqr == "":
                turn -= 1
        pos_read = Position(code, finished, turn, outcome)
        self.catalog_pos(code, pos_read)

    def format_data(self):
        # populate code_to_pos
        num_rows = len(self.data.get("Result"))
        print(num_rows)
        for row in range(num_rows):
            r = self.data.iloc[row]

            # convert r into a numpy array so indexing works
            # r may have 4columns instead of 3 because of a glitch
            r_factor = int(len(r) - 3)
            code = r[0 + r_factor]
            res = r[1 + r_factor]
            finished = r[2 + r_factor]
            self.process_entry(code, res, finished)

        # catalog the blank board
        blank = Position(0, False, 1, None)
        self.catalog_pos(0, blank)

    @staticmethod
    def min_max(array, maxi):
        # array is a 1D numpy array
        # if maxi is true, return max value, and vice versa
        minim = 1  # highest possible val
        maxim = -1  # lowest possible val
        for i in range(len(array)):
            if array[i] > maxim:
                maxim = array[i]
            if array[i] < minim:
                minim = array[i]
        if maxi:
            return maxim
        else:
            return minim

    def process_outcome(self, outcome, ai):
        # ai is True if ai is x, false if ai is o
        if outcome == "d":  # doesn't matter who AI is or what the game mode is
            return 0
        game_mode_factor = -2 * self.mode + 1  # result is 1 for traditional, -1 for reverse
        # if the game mode is reverse, opposite outcome needs to be returned
        if ai:  # ai is x
            if outcome == "x":
                return game_mode_factor
        else:  # ai is o
            if outcome == "o":
                return game_mode_factor
        return -1 * game_mode_factor

    def learn_from_game(self, final_pos, code, game_over):
        # write the new game moves and result into the spreadsheet
        # final_pos is the position object representing the game_board

        # create a row with new data
        new_row = list()
        new_row.append(code)
        new_row.append(final_pos.get_result())
        if game_over:
            new_row.append(True)
        else:
            new_row.append(False)
        # append it to dataframe and write to the relevant sheet
        if len(self.data) > 0 and not len(new_row) == len(self.data.iloc[0]):
            self.data = self.data.drop("Code", axis=1)  # avoid glitch where cell row number is placed in column 1
        #  extra column is created (not sure why)
        self.data.loc[len(self.data)] = new_row
        with pd.ExcelWriter(self.source, mode='a', if_sheet_exists="overlay") as writer:
            self.data.to_excel(writer, sheet_name="OriginalData")

    def learn_from_pos(self, unknown, pos, code, node_val):
        # if unknown is 0, the node can be assigned a permanent value that should be written to the spreadsheet
        # that way the AI won't have to process it in future games so runtime is quicker (and saves memory)

        pos.set_result(node_val)
        if unknown == 0:
            self.learn_from_game(pos, code, False)

    def process_node(self, old_code, old_pos, ai):
        # old_pos is a position object representing the position being evaluated (without new move added)
        # old_code is the integer code for old_pos
        # ai is True if ai is x, false if ai is o

        # base case (old_pos is a final position, game is over)
        if old_pos.game_is_over():
            return self.process_outcome(old_pos.get_result(), ai)

        # secondary base case (old_pos is not final but has only one possible outcome with optimal play)
        if type(old_pos.get_result()) == str:
            return self.process_outcome(old_pos.get_result(), ai)

        # recursive case
        turn = old_pos.get_turn()
        options = old_pos.get_available_moves()
        positions_unknown = 0  # if all positions stemming from a node have a result, the value of the node can be
        # written to the spreadsheet so the AI does not need to evaluate it in future games
        # saves memory and runtime
        if (ai and (turn % 2 == 1)) or (not ai and (turn % 2 == 0)):  # it is the ai's turn
            analysis = np.zeros(len(options), dtype=int)  # evaluate all possible moves
            for m in range(len(options)):
                your_m = options[m]
                new_code = old_code + self.encode_new_move(your_m, turn + 1)
                try:
                    new_pos = self.code_to_pos[new_code]
                    if not new_pos.has_result():
                        positions_unknown += 1
                    analysis[m] = self.process_node(new_code, new_pos, ai)
                except KeyError:  # move has not been made before, outcome unknown
                    positions_unknown += 1
                    analysis[m] = 0  # better than known loss (-1), worse than known win (1)
            node_value = self.min_max(analysis, True)
            self.learn_from_pos(positions_unknown, old_pos, old_code, node_value)
            return node_value  # max val is returned (best outcome for AI)
        else:  # it is the opponent's turn
            moves_seen = list()  # will only store evaluations of moves previous opponents have made
            for m in range(len(options)):
                opp_m = options[m]
                new_code = old_code + self.encode_new_move(opp_m, turn + 1)
                try:
                    new_pos = self.code_to_pos[new_code]
                    if not new_pos.has_result():
                        positions_unknown += 1
                    moves_seen.append(self.process_node(new_code, new_pos, ai))
                except KeyError:  # no opponent has made this move, AI will not consider it
                    positions_unknown += 1
                    pass
            # copy moves_seen into a numpy array so we can use min_max
            analysis = np.zeros(len(moves_seen), dtype=int)
            for i in range(len(moves_seen)):
                analysis[i] = moves_seen[i]
            # return worst outcome in analysis (assume opponent plays optimally and knows the analysis too)
            node_value = self.min_max(analysis, False)
            self.learn_from_pos(positions_unknown, old_pos, old_code, node_value)
            return node_value

    def choose_move(self, old_code, old_pos, ai):
        # old_pos is a position object representing the position being evaluated (without new move added)
        # old_code is the integer code for old_pos
        # ai is True if ai is x, false if ai is o
        turn = old_pos.get_turn()
        options = old_pos.get_available_moves()
        evals = np.zeros(len(options), dtype=int)  # analyze each option to determine which is least likely to lose
        positions_unknown = 0
        # -1 represents loss, 0 represents draw, 1 represents win
        for i in range(len(evals)):
            your_m = options[i]
            new_code = old_code + self.encode_new_move(your_m, turn + 1)
            try:
                new_pos = self.code_to_pos[new_code]
                if not new_pos.has_result():
                    positions_unknown += 1
                evals[i] = self.process_node(new_code, new_pos, ai)
            except KeyError:  # position has not been reached before, outcome unknown
                positions_unknown += 1
                evals[i] = 0  # better than known loss (-1), worse than known win (1)
        best_res = self.min_max(evals, True)

        # choose randomly between all the moves that have the best_res
        best_moves = list()
        for m in range(len(evals)):
            if evals[m] == best_res:
                best_moves.append(options[m])
        choice = math.floor(random.random() * len(best_moves))
        return best_moves[choice]
