# Dev GPTeam CLI

Dev GPTeam CLI is a command-line application designed to streamline the software development process by leveraging the power of GPT models. This application allows users to input initial software requirements and uses GPT-powered interactions to refine requirements, generate source code, and validate the code.

## Features

- Requirement refinement through simulated PM GPT interaction.
- Source code generation with simulated Dev GPT model.
- Code validation and quality checks with simulated QA GPT model.
- Simple command-line interface for ease of use.

## Getting Started

### Prerequisites

Before running Dev GPTeam CLI, make sure you have Python 3.9 or higher installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation and Run

Clone the repository to your local machine:

```
cd DevGPTeam
pip install -r requirements.txt
python src/main.py
```

### Generate source code from a checkpoint file

usage:
`usage: main.py [-h] [--skipPM] [--skipDev] [--noQA] [--snapshot-directory SNAPSHOT_DIRECTORY]`

example:

```
python src\main.py --skipPM --snapshot brick_breaker_game
```
