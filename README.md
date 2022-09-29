# FE-solver
This is educational program that i will make while learning how FE solver works.

## Day 1. 22.09.22
One-dimensional linear elastic elements were considered.

Extended element stiffness matrix were introduced.

A single system for all nodes were written.

### function Kee(elems)
input: elems - list of threes: nodes of element and element stiffness.
Nodes are enumerated from 0.

output: Kee - extended elastic matrix of stiffness.
