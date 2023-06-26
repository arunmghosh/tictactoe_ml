# Tic-tac-toe Machine Learning Algorithm

## Summary
Python program that allows user to play tic tac toe against a machine learning algorithm that reads data from previous games from a spreadsheet. Each game is recorded by assigning an integer code to the final position and writing the outcome to a spreadsheet. The algorithm can also classify non-final positions as winning for x or o after all the possibilities stemming from those positions have been tested. 

## Background
This project addresses the problem of coding a machine learning algorithm to play a game without using any AI packages such as scikitlearn (create an ML algorithm from scratch). It is used to simulate how a human learns the optimal moves for tic tac toe, and can also play reverse tic tac toe (where you lose if you get three in a row) based off the same training data. 

## How is it used?
This project can be used by anyone who wants to play tic tac toe or the reverse version, as well as other students of AI who want to avoid the black-box problem as much as possible (it is possible to avoid it for a simple game like this). 

## Data sources and AI methods
The code and spreadsheet that records the data can be found in the other files.

## Challenges
There were many challenges during the development process:
1. Deciding how to store game data in the spreadsheet (ultimately settled on encoding the final positions and pairing the numeric code with the result (x, o, draw)
2. Getting the algorithm to improve (learn from the past games)
3. Implementing a "training" mode where the algorithm plays itself

There are also many things it cannot do:
1. Inefficient with games such as Go or Chess which have many more possible positions
2. Observe symmetry in the game board like a human would
3. Play a game that requires more than two players

## What's next?
In the future, I hope to create AI algorithms for purposes other than game simulation, perhaps in the field of politics. I want to test AI-run social media accounts (but not on real socials, just in the program) or voting simulations. 
