# Code-in-Place-rubik-script-capstone
Educational Python/Pygame app to learn the Rubik’s Cube and practice Python concepts such as lists, dictionaries, conditionals, loops, and algorithms through interactive Rubik Script challenges.

# Rubik Script: Learn Python with the Rubik’s Cube

Rubik Script is an educational Python/Pygame application created as a final project for Code in Place. The project uses the Rubik’s Cube as a visual and interactive way to help users learn both cube logic and basic programming concepts in Python.

The application combines guided Rubik’s Cube learning, special cube patterns, solving support, and programming challenges based on variables, lists, dictionaries, conditionals, loops, and algorithms.

## Project Purpose

The purpose of this project is to make programming more visual, interactive, and beginner-friendly. Instead of learning Python only through abstract examples, users interact with a Rubik’s Cube and connect cube movements with programming logic.

The cube is used as a learning model because it naturally connects with important Python concepts:

* Lists and matrices: each cube face can be represented as a 3x3 structure.
* Dictionaries: each face of the cube can be stored using keys such as `U`, `D`, `F`, `B`, `R`, and `L`.
* Conditionals: the program can decide which move to apply depending on the cube state.
* Loops: repeated cube algorithms can be automated using `for` and `while`.
* Functions: cube movements and learning modules are organized into reusable actions.

## Main Features

### 1. Beginner Rubik’s Cube Guide

This mode is designed for users who do not know how to solve the Rubik’s Cube. It provides simple instructions using beginner-friendly language and visual support.

The user can color the cube according to their real cube and generate a guided solution.

### 2. Experienced User Mode

This mode is designed for users who already know how to solve the cube. It includes a challenge system with a timer, machine solving time, and personal record tracking.

### 3. Visual Manual

The manual explains the basic structure of the Rubik’s Cube:

* Centers
* Edges
* Corners
* Cube orientation
* Face names
* Basic cube notation

### 4. Special Patterns

This module includes special Rubik’s Cube patterns such as:

* Checkerboard
* Six spots
* Four spots
* Cube in cube
* Superflip
* Snake
* Anaconda
* Cross
* Stripes
* Staircase
* Frame
* Zigzag

Each pattern includes the algorithm to create it and the route to return the cube to its original state.

### 5. Rubik Script: Python Learning Challenges

Rubik Script is a game-like learning module inspired by Karel-style logic. The user learns Python by selecting the correct code block to control the cube.

The module includes three levels:

#### Level 1: Cube Variables

This level teaches how to represent the cube using variables, lists, dictionaries, and indexes.

Example concept:

```python
cubo["F"][1][1]
```

This expression accesses the center of the front face.

#### Level 2: Turn Conditionals

This level teaches `if`, `elif`, and `else` statements by deciding which cube movement should be executed.

Example concept:

```python
if centro_derecho == "Rojo":
    giro_R()
else:
    giro_U()
```

#### Level 3: Algorithmic Loops

This level teaches `for` and `while` loops by repeating Rubik’s Cube algorithms.

Example concept:

```python
algoritmo_base = ["R", "U", "R_prima", "U_prima"]

for _ in range(6):
    ejecutar(algoritmo_base)
```

## Cube Notation

The project uses standard Rubik’s Cube notation:

| Notation | Meaning                |
| -------- | ---------------------- |
| `U`      | Upper face             |
| `D`      | Down face              |
| `F`      | Front face             |
| `B`      | Back face              |
| `R`      | Right face             |
| `L`      | Left face              |
| `'`      | Inverse turn           |
| `2`      | Half turn, 180 degrees |

## Python Concepts Used

This project uses several core Python concepts:

* Variables
* Strings
* Lists
* Dictionaries
* Conditional statements
* Loops
* Functions
* Classes
* Event handling
* File persistence
* Pygame graphics
* User interaction

## Requirements

Install the required libraries with:

```bash
pip install -r requirements.txt
```

The project uses:

```text
pygame
kociemba
```

## How to Run

Run the project with:

```bash
python rubik_capstone.py
```

## Project Structure

```text
rubik_capstone.py      Main Python/Pygame application
README.md             Project documentation
requirements.txt      Required Python libraries
.gitignore            Files and folders ignored by Git
```

## Author

Created by **Alejandra Lafuente**.

## Final Project Statement

Rubik Script is an educational project that connects the Rubik’s Cube with Python programming. It helps users learn how algorithms work through visual cube movements and interactive programming challenges. The project aims to make programming more engaging, practical, and accessible for beginners.
