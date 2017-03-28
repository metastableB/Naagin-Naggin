# DeepLearning Snake

Create a `virtualenv` and install `Keras` with `Theano` backend. Then install the requirements specified in the `requirements.txt` using pip:

    pip install -r requirements.txt

There is no documentation yet within the code, but it should be easy to follow. For a GUI version of the game simulation, run the following:

    python -m dlsnake.snakeGame

Use python3 for all operations, and work from the project root directory.

## TODO
- [ ] Document configuration options
- [ ] ArgParser
- [X] Snake with increasing length
- [X] Head differently colored
- [X] Prevent reverse moves
- [ ] Fix toggling between GUI and non GUI versions
- [X] Move score, foodScore and livingScore to gameState
- [X] Check if food is valid
- [X] Check if update causes death
- [ ] Special power food
- [X] Add border to cells
- [X] Add gameover message
- [ ] Add walls
- [ ] Add something which actually looks like head/tail

SIDE NOTE: BOXY THEME WITH NUMIX SKIN IS AWESOME
