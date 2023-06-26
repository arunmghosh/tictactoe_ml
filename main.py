from Game import Game


def run_game(prompt, game_m, training_m):
    num_games = int(input(prompt))
    for g in range(num_games):
        new_game = Game(game_m, training_m)
        new_game.play_game()
        new_game.catalog_game()


def main():
    game_mode = int(input("Enter 0 for standard tic tac toe, and 1 for reverse tic tac toe. "))
    training_mode = input("Enter true to train the ai or false to play the ai. ")
    if training_mode == "true":  # input is a string, not boolean, must convert
        training_mode = True
    else:
        training_mode = False
    if training_mode:
        training_prompt = "How many games do you want the AI to play against itself? "
        run_game(training_prompt, game_mode, training_mode)
    else:  # user will play only one game per run of the program
        playing_prompt = "How many games do you want to play? "
        run_game(playing_prompt, game_mode, training_mode)


if __name__ == '__main__':
    main()
