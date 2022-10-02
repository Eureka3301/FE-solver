# creating input file object
file = open('input.in', 'r')

# number of nodes
nodenum = int(file.readline())

file.readline()
# create vector of forces
forces = []

# adding nodal forces
for i in range(nodenum):
    line = file.readline()
    forces += list(map(float, line.split(', ')))

file.readline()
# creates list of elements
elements = []

while True:
    # takes a line
    line = file.readline()
    # ends when line is empty
    if not line or line == '\n':
        break
    # adding element
    elements.append(list(map(float, line.split(', '))))
    elements[-1][0] = int(elements[-1][0])
    elements[-1][1] = int(elements[-1][1])

file.readline()
# boundary
bound = list(map(int, file.readline().split(', ')))

# closing file
file.close()

import numpy as np

# матрица жестокости
Kee = np.zeros((2*nodenum, 2*nodenum))

for el in elements:
    # матрица-универсал
    K0 = np.array([
        [1, 0, -1, 0],
        [0, 0, 0, 0],
        [-1, 0, 1, 0],
        [0, 0, 0, 0]
    ])
    # преобразование для элемента
    Lt = np.array([
        [el[3], -el[4], 0, 0],
        [el[4], el[3], 0, 0],
        [0, 0, el[3], -el[4]],
        [0, 0, el[4], el[3]]
    ])
    add = np.matmul(Lt, K0)
    add = np.matmul(add, Lt.transpose())
    add = el[5]*el[6]/el[2] * add
    
    # закинуть насчитанное в большого босса
    nodes = [2*el[0], 2*el[0]+1, 2*el[1], 2*el[1]+1]
    for i in range(4):
        for j in range(4):
            Kee[nodes[i]][nodes[i]] += add[i][i]
            Kee[nodes[i]][nodes[j]] += add[i][j]
            Kee[nodes[j]][nodes[i]] += add[j][i]
            Kee[nodes[j]][nodes[j]] += add[j][j]
    
# boundary conditions
A = np.delete(np.delete(Kee, bound, 0), bound, 1)
b = np.delete(forces, bound)

X = np.linalg.solve(A, b)

# закинуть все в большой вектор
U = []
i = 0
j = 0
for n in bound:
    while i < n:
        U.append(X[j])
        i += 1
        j += 1
    U.append(0)
    i += 1
while (i < 2*nodenum):
    U.append(X[j])
    i += 1
    j += 1

l = np.sqrt(U[2]*U[2] + U[3]*U[3])



print(elements[0][6]*U[3])