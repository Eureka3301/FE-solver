# FE-solver
This is educational program that i will make while learning how FE solver works.

## Day 1. 22.09.22
One-dimensional linear elastic elements were considered.
In nodes forces were applied.
Our goal was to find nodes shifts.

We made extended stiffness matrix for series of 2 elements.

The same idea is for general system. Its implemented here in following function.
All the info about connections contains node pairs (i,j) of elements.

### Kee(nodes) \\ function
*nodes* - list of threes: pair of nodes and elastic modulus.
Prog goes through nodes list and calculates Kee matrix.
