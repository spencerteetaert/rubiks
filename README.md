# rubiks
Project for APS360. A software package that facilitates all aspects of a Rubik's cube search and solves functions. This project is designed to be used by training a machine learning model on a self-generated dataset to act as a cube state heuristic. An expected prediction is a number representing how many moves the cube is away from being solved. Using this heuristic, A* search is implemented to find a path from any state to a solved state. Our best implementation solves ~25% of all possible cube states in near-optimal guarantee paths (< 20 moves). This algorithm sacrifices solve rate for solve optimality i.e. it does not guarantee a solve, but the cubes it does solve is near-optimal, something that most machine learning implementations cannot achieve. 


## __tests__
* contains tests for functions. Ensure before uploading that you have both written your test function, 
and your code successfully runs all other tests. 
---

## src
### src/model
* data_handler.py - functions for generating, loading, and parsing datasets 
* model.py - a class that contains our ML model for training the Rubiks heuristic
* search.py - contains search and node classes, both used when performing search. Can be easily edited to perform baseline searches without an ML model. 
* train.py - functions for training, evaluating, and documenting an ML model
### src/Rubiks 
* cube.py - class for a Rubiks Cube object. Stores state, performs rotations, scrambles, and checks for solve 
### src/UI
* display_tools.py - functions for displaying the Cube states in a user-friendly form

<img src="https://user-images.githubusercontent.com/45899408/114197049-f9dd5500-991f-11eb-9f08-7cce96249eae.PNG" height="200" /><img src="https://user-images.githubusercontent.com/45899408/114197052-fa75eb80-991f-11eb-9c37-34bf4353a708.PNG" height="200" />
---

## tools 
* example.py - 
* profiler.py - runs a timing analysis on the full search pipeline 
* test_search.py - tests a model's search against a given test/validation set
* training0.txt - dataset by Anton Bobrov 

THE BEER-WARE LICENSE (Revision 42):
antbob@users.noreply.github.com created this. As long as you retain
this notice you can do whatever you want with this stuff. If we meet
someday, and you think this stuff is worth it, you can buy me a beer in
return Anton Bobrov

* training_code.ipynb - notebook for running hyperparameter search, result representation, and general training
---

* close_nodes - pickled dictionary of cube states that are within 4 moves of optimal solve 
* requirements.txt - project requirements 
* run_tests.py - runs all unit tests
* test_set - pickled 2d list containing 20 sets of 5 cuubescubes scrambled 1 - 20 times (sorted)
