# FE-solver
This is educational program that i will make while learning how FE solver works.

## Day 1. 22.09.22
One-dimensional linear elastic elements were considered.

Extended element stiffness matrix were introduced.

A single system for all nodes shifts were written.

### function Kee(elems)
input: elems - list of threes: nodes of element and element stiffness.
Nodes are enumerated from 0.

output: Kee - extended elastic matrix of stiffness.

## Day 2. 29.09.22
Truss analysis.

Matrix of extended elements stiffness were made for the truss.

A single system for all nodes shifts were written.

### input.in - additional file for the day2.py program.
Consists of data about elements, nodal forces and boundary conditions.

It works? Actually, no tests provided.

## Day 3. 20.10.22
Weak and strong formulations. General scheme of FE method.

Form functions introduced.
Solution approximation with form functions was written.
Matrix of stiffness and forсe vector can be calculated.

y''+y=1, 0<x<1, y(0)=1, y(1)=0 is solved.
