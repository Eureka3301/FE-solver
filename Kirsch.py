import numpy as np

# plate 5mx5m with 1m round hole in x=0 y=0; x=5m has 1e+3 Pa

file_nodes = 'nodes_test.txt'
file_elements = 'elements_test.txt'
u_x = 'u_x.txt'
u_y = 'u_y.txt'



file = open(file_nodes, 'r')
line = file.readline()
Xnode = []
Ynode = []
node_num = 0
while True:
    line = file.readline()
    if not line:
        break
    [x, y] = list(map(float, line.split()[1:3]))
    Xnode.append(x)
    Ynode.append(y)
    node_num += 1



file = open(file_elements, 'r')
line = file.readline()
ijk = []
N = []
elem_num = 0
while True:
    line = file.readline()
    if not line:
        break
    l = []
    for n in list(map(int, line.split()[2:])):
        l.append(n-1)
    A = np.array([
        [1, Xnode[l[0]], Ynode[l[0]]],
        [1, Xnode[l[1]], Ynode[l[1]]],
        [1, Xnode[l[2]], Ynode[l[2]]]
    ])
    N.append(np.linalg.inv(A))
    ijk.append(l)
    elem_num += 1

# Ne = N[e], Ne[p][q] q - 0 -- i, 1 -- j, 2 -- k; p - coefficient within 0 -- 1, 1 -- x, 2 -- y



def area(x, y):
    A = np.array([
        [x[0], y[0], 1.0],
        [x[1], y[1], 1.0],
        [x[2], y[2], 1.0]
    ])
    return 0.5*np.linalg.det(A)

def dist(x, y):
    return np.square((x[0]-x[1])**2 + (y[0]-y[1])**2)

E = 2e+6 #Pa
nu = 0.3

K = np.array([[0.0]*(2*node_num) for _ in range(2*node_num)])
b = np.array([0.0]*(2*node_num))

invD = np.array([
        [1.0, -nu, 0.0],
        [-nu, 1.0, 0.0],
        [0.0, 0.0, 2*(1+nu)]
    ])
D = E * np.linalg.inv(invD)

for e in range(elem_num):
    Ne = N[e]
    BN = np.array([
        [Ne[1][0], 0.0, Ne[1][1], 0.0, Ne[1][2], 0.0],
        [0.0, Ne[2][0], 0.0, Ne[2][1], 0.0, Ne[2][2]],
        [Ne[2][0], Ne[1][0], Ne[2][1], Ne[1][1], Ne[2][2], Ne[1][2]]
    ])
    i = ijk[e][0]
    j = ijk[e][1]
    k = ijk[e][2]
    S = area([Xnode[i], Xnode[j], Xnode[k]], [Ynode[i], Ynode[j], Ynode[k]])
    Ke = S * np.matmul(np.matmul(BN.transpose(), D), BN)



    x0 = 5.
    sigm0 = 1e+3

    bond = []
    for q in ijk[e]:
        if (Xnode[q] == x0):
            bond.append(q)
    be = np.array([0.0]*6)
    if len(bond) == 2:
        l = abs(dist([Xnode[bond[0]], Xnode[bond[1]]], [Ynode[bond[0]], Ynode[bond[1]]]))
        for q in range(3):
            be[2*q] += Ne[0][q]*l
            be[2*q] += Ne[1][q]*x0*l
            be[2*q] += Ne[2][q] * 0.5 * abs(Ynode[bond[0]]**2 - Ynode[bond[1]]**2)
    sigm0 = 1e+3
    be = be * sigm0

    for q in range(3):
        for p in range(3):
            K[2*ijk[e][q]][2*ijk[e][p]] += Ke[2*q][2*p]
            K[2*ijk[e][q]+1][2*ijk[e][p]] += Ke[2*q+1][2*p]
            K[2*ijk[e][q]][2*ijk[e][p]+1] += Ke[2*q][2*p+1]
            K[2*ijk[e][q]+1][2*ijk[e][p]+1] += Ke[2*q+1][2*p+1]

        b[2*ijk[e][q]] += be[2*q]
        b[2*ijk[e][q]+1] += be[2*q+1]




nums = range(2*node_num)

rem = []
for p in range(node_num):
    if Xnode[p] < 1e-7:
        rem.append(2*p)
    if Ynode[p] < 1e-7:
        rem.append(2*p+1)


Krem = np.delete(K, rem, 0)
Krem = np.delete(Krem, rem, 1)

brem = np.delete(b, rem, 0)

nums = np.delete(nums, rem, 0)

urem = np.linalg.solve(Krem, brem)

#**********************************************************************************************

u = [0.0]*(2*node_num)

i = 0
for n in range(len(nums)):
    u[nums[n]] = urem[n]

print(rem)
print(nums)

#fileX = open(u_x, 'r')
#fileY = open(u_y, 'r')
#lineX = fileX.readline()
#ineY = fileY.readline()
#u_test = []
#while True:
#    lineX = fileX.readline()
#   lineY = fileY.readline()
#    if not lineX:
#        break
#    u_test.append(float(lineX.split()[-1]))
#   u_test.append(float(lineY.split()[-1]))

for i in range(node_num):
    print('%1.2E' % u[2*i])
    print('%1.2E' % u[2*i+1])

#u = np.linalg.solve(K,b)

print(K.dot(u)-b)
print(Krem.dot(urem)-brem)

#print(Ke)