# Nagging-Naagin: Deep Q-Learning Applied to Snake

Using adverserial search, reinforcement learning and eventually deep-q learning for model independent game play of snake. The game has been built uisng `pygame` and various agents have been provided that can be used to play the game.

## Preview

Properties|Reflex-Agent | MinMax-Agent|
|----------|-------------|-------------|
|Preview    |<img src="dlsnake/preview/01.gif" height="200" alt="A Simple Reflex-Agent playing Snake">|<img src="dlsnake/preview/02.gif" height="200" alt="A Simple MinMax-Agent playing Snake">|
|Grid Size| 20x20 | 20x20|
SnakeAgent| Reflex Agent| MinMax-Agent|
Food Agent| MaxManhattanFoodAgent|MaxManhattanFoodAgent|
Score| 2021||
Snake Length | 67|
Time-Real| 1m14.105s |
Time-User| 0m6.547s |
Time-System| 0m0.980s |
Misc| None|  Depth=6


## Installation
>The module uses `python3` and has `Keras` with `Theano` backend installed from their upstream git repository as the pip package was not up-to-date. If you face problems with Keras during the installation procedure, revert back to the version specified in the `requirements.txt`. 

Create a `virtualenv` with `python3` and install `Keras` with `Theano` backend. Then install the requirements specified in the `requirements.txt` using pip:

    pip install -r requirements.txt

There is no documentation yet within the code, but it should be easy to follow. For a GUI version of the game simulation, run the following from the project root:

    python -m dlsnake.snakeGame

Various agents have been included and can be enabled using the `--agent` flag.

## Usage
```
usage: snakeGame.py [-h] [-a {ReflexAgent}]
                    [-s {RandomFoodAgent,MaxManhattanFoodAgnet}] [-n] [-t]
                    [-f FRAMERATE]

Naagin-Nagging v0.1 - Applying Deep Q-Learning to Snake.

optional arguments:
  -h, --help            show this help message and exit
  -a {ReflexAgent}, --agent {ReflexAgent}
                        Specify the agent to use for playing snake.
  -s {RandomFoodAgent,MaxManhattanFoodAgnet}, --food-agent {RandomFoodAgent,MaxManhattanFoodAgnet}
                        Specify the food agent to use.
  -n, --no-graphics     Disable graphics and run silently.
  -t, --text-graphics   Enable text graphics.
  -f FRAMERATE, --frame-rate FRAMERATE
                        Frame rate for GUI graphics. Should be a non - zero
                        integer.
```