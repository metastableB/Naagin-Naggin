# Nagging-Naagin: Deep Q-Learning Applied to Snake

Using adverserial search, reinforcement learning and eventually deep-q learning for model independent game play of snake. The game has been built uisng `pygame` and various agents have been provided that can be used to play the game.

## Preview

Reflex-Agent:
![A Simple Reflex-Agent playing Snake][previewReflexAgent]


## Installation
>The module uses `python3` and has `Keras` with `Theano` backend installed from their upstream git repository as the pip package was not up-to-date. If you face problems with Keras during the installation procedure, revert back to the version specified in the `requirements.txt`. 

Create a `virtualenv` with `python3` and install `Keras` with `Theano` backend. Then install the requirements specified in the `requirements.txt` using pip:

    pip install -r requirements.txt

There is no documentation yet within the code, but it should be easy to follow. For a GUI version of the game simulation, run the following from the project root:

    python -m dlsnake.snakeGame

Various agents have been included and can be enabled using the `--agent` flag.

## TODO

### Pertaining to Code and Functionality
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
- [ ] Add some graphics which actually looks like head/tail

### Pertaining to Project
- [X] Implement manual play
- [X] Implement Reflex Agent
- [ ] Implement adversary controlling food capsules so as to trap snake.
- [ ] Implement adverserial search (minMax)
- [ ] Implement expectimax search
- [ ] Implement MDP based Q-Learning
- [ ] Implement grids + MDP based Q-learning
- [ ] Train an image based Q-learning agent


[previewReflexAgent]: https://github.com/metastableB/Naagin-Naggin/preview/01_reflexAgent.gif "Logo Title Text 2"
