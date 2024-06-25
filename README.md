# CuriosityAgents
In the following, I mentione the execution environment and important files.

## Environments
- ACT-R (7.21) 
- SBCL (2.0) 
- Ptyhon (3.8.12) 
- NumPy (1.21.5) 
- Pandas (1.4.2) 
- Matplotlib (3.5.1) 
- Pytourch (1.9.0) 
- jupyter_core (4.7.1) 
- jupyter-notebook (6.3.0) 
- seaborn (0.12.2) 

## act-r directory
This directory contains the source code for the ACT-R models.

- 7_7
- 9_9
- 11_11

The files in these directories are maze maps. Each map file includes exterior walls, so the actual map sizes are 5x5, 7x7, and 9x9.

- random.lisp

randome model

- backtrack.lisp

DFS model

- instance-base.lisp

DFS+IBL model

- main.py

This file describes the main process for executing the ACT-R model. Please place this file and the maze map directories in the same location mentioned above under the ACT-R environment. Additionally, please set the path to each of the aforementioned models on line 310 of this file after launching ACT-R, you can execute the following command.

- execution example: python main.py

Please install Python version 3 or higher. Additionally, make sure to install NumPy and Pandas.

## data directory
This directory contains the simulation results of the models (ACT-R and ICM) and a script that outputs them to graphs.

- data.ipynb

This script draws the graphs of simulation.

- trajectory.ipynb

This script draws the trajectory of movements.

## icm directory
This directory contains the source code for the ICM model.

- 7_7
- 9_9
- 11_11

These files in these directories are the same maze maps above (act-r directory).

- main.py

This file describes the main process for executing the ICM model. Please place this file and the maze map directories in the same location.

- execution example: python main.py

## rule_example directory
This folder contains pseudo code for the rules of model movement. You can see the difference in the complexity of the rules and the number of variables used for pattern-matching.

- random_model.txt

This file is the Random model.

- dfs_and_dfsibl_model.txt

This file is the DFS and DFS+IBL models. 
