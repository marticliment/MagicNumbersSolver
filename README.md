# MagicNumbersSolver
Python solver for MagicNumbers.

MagicNumber is a game where your opponent thinks a four-digit number, without repeating any digits, and you need to guess it with the least amount of rounds possible.
At each round, you guess a combination, and you opponent lets you know the amount of digits in the correct position, and the amount of digits that are in wrong positions, but that appear in the number to guess.

For example: The number I have to guess is `5018`, and I guess `3089`. I am given one correct digit and one misplaced digit (being the `0` and the `8`, respectively. However, which digits are correct and which are not is not told to me)

This python script tries to guess that number in the least amount possible of attempts, averaging around `~5.460324` (avg after 1,000,000 reps) guesses per game

1. Download the .py file
2. Adjust the `NUM_OF_DIGITS` variable. This changes the possible digits an input can take. Default is 10
3. Adjust the `REPS` to change how many tests will be run. 500 reps should finish in a reasonable amount of time (<10secs for python, <5 secs for pypy)
3. Adjust the `PRINT_EACH_RESULT` to enable/disable reporting each solved game
4. Run the script (with pypy preferably) and watch your CPU melt itself.
