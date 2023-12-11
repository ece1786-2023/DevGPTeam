# Dev GPTeam

Dev GPTeam CLI is a command-line application designed to streamline the software development process by leveraging the power of GPT models. This application allows users to input initial software requirements and uses GPT-powered interactions to refine requirements, generate source code.

## Features

- Requirement refinement through simulated PM GPT interaction.
- Source code generation with simulated Dev GPT model.
- Code validation and quality checks with simulated QA GPT model.
- Simple command-line interface for ease of use.
- Provide a checkpoint/snapshot feature so that users can restart from any stage. For example, they can regenerate source code from the latest requirements without going through PM GPT again.

## Game generation demo

<img src="assets/brick-breaker.gif" width="200" />
<img src="assets/snake.gif" width="200" />
<img src="assets/2048.gif" width="200" />
<img src="assets/flappy-bird-and-astreoid-dodger.gif" width="200" />
<img src="assets/flappy-bird.gif" width="200" />
<img src="assets/tetris.gif" width="200" />

## Getting Started

### Prerequisites

Before running Dev GPTeam CLI, make sure you have Python 3.9 or higher installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

You can also run the software inside [Anaconda](https://www.anaconda.com/download).

### Installation and Run

Clone the repository to your local machine:

```
cd DevGPTeam

pip install -r requirements.txt

python src/main.py
```

### Generate source code from a checkpoint file

usage:
`usage: main.py [-h] [--skipPM] [--skipDev] [--skipQA] [--snapshot-directory SNAPSHOT_DIRECTORY]`

example:

```
python src\main.py --skipPM --snapshot brick_breaker_game
```
