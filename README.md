# FE-solver
This is educational program that i will make while learning how FE solver works.

## Day 1. 22.09.22
We have solved one dimensional staticaly and kinematicaly defined reological problems.
We can make a matrix of system stiffness and write equations for unknown nodal shift vector.
If boundary conditions are provided we can solve the system and find shifts.

### stiffness_matrix(M)
M - list of 3x4 matrix for each element.
Each matrix is extended and apparantely contains nodes numbers and force column.
---------------
0 |  i  |  j  | 0
---------------
i | a11 | a12 | f1
---------------
j | a21 | a22 | f2
---------------
