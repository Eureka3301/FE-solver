# FE-solver
This is educational program that i will make while learning how FE solver works.

## Day 1. 22.09.22
We have solved one dimensional staticaly and kinematicaly defined reological problems.
We can make a matrix of system stiffness and write equations for unknown nodal shift vector.
If boundary conditions are provided we can solve the system and find shifts.

### nodes \\ variable
list of pairs
pair number *i* shows corresponding pair of nodes for element number *i*

### Kee_F(order) \\ function
gives extended stiffness matrix and force vector
*order* is a list of threes (el1 num, el2 num, type of circuit).
type can be 'p' - paralell or 's' - series.
el1 num < el2 num
threes must be sorted so that each step has needed precalculations.
all changes occur in Kee
