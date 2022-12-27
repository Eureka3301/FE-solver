import numpy as np

def area(x, y):
    A = np.array([
        [x[0], y[0], 1.0],
        [x[1], y[1], 1.0],
        [x[2], y[2], 1.0]
    ])
    return 0.5*np.linalg.det(A)

# plate 5mx5m with 1m round hole in x=0 y=0; x=5m has 1e+3 Pa

file_nodes = 'nodes.txt'
file_elements = 'elements.txt'
u_x = 'u_x.txt'
u_y = 'u_y.txt'

file = open(file_nodes, 'r')
line = file.readline()
X = []
Y = []
ndnum = 0
while True:
    line = file.readline()
    if not line:
        break
    [x, y] = list(map(float, line.split()[1:3]))
    X.append(x)
    Y.append(y)
    ndnum += 1



file = open(file_elements, 'r')
line = file.readline()
ijk = []
N = []
enum = 0
while True:
    line = file.readline()
    if not line:
        break
    l = []
    for n in list(map(int, line.split()[2:])):
        l.append(n-1)
    A = np.array([
        [1, X[l[0]], Y[l[0]]],
        [1, X[l[1]], Y[l[1]]],
        [1, X[l[2]], Y[l[2]]]
    ])
    N.append(np.linalg.inv(A).transpose())
    ijk.append(l)
    enum += 1



E = 2e+6
nu = 0.3

invD = np.array([
        [1.0, -nu, 0.0],
        [-nu, 1.0, 0.0],
        [0.0, 0.0, 2*(1+nu)]
    ])
D = E * np.linalg.inv(invD)

K = np.zeros((2*ndnum, 2*ndnum))
b = np.zeros(2*ndnum)

for e in range(enum):
    Ne = N[e]

    i = ijk[e][0]
    j = ijk[e][1]
    k = ijk[e][2]

    Ni = Ne[0]
    Nj = Ne[1]
    Nk = Ne[2]
    
    N_i = lambda x,y: Ni[0] + Ni[1]*x + Ni[2]*y
    N_j = lambda x,y: Nj[0] + Nj[1]*x + Nj[2]*y
    N_k = lambda x,y: Nk[0] + Nk[1]*x + Nk[2]*y

    BN = np.array([
        [Ni[1], 0.0, Nj[1], 0.0, Nk[1], 0.0],
        [0.0, Ni[2], 0.0, Nj[2], 0.0, Nk[2]],
        [Ni[2], Ni[1], Nj[2], Nj[1], Nk[2], Nk[1]]
    ])

    S = area([X[i], X[j], X[k]], [Y[i], Y[j], Y[k]])
    Ke = S * np.matmul(np.matmul(BN.transpose(), D), BN)



    be = np.zeros(2*ndnum)

    x0 = 5
    sigm0 = 1e+3

    bnd = []
    for q in ijk[e]:
        if (abs(X[q] - x0) < 1e-7):
            bnd.append(q)

    be = np.zeros(6)

    if len(bnd) == 2:
        y1 = Y[bnd[0]]
        y2 = Y[bnd[1]]

        l = abs(y1 - y2)
        d = abs(y1*y1-y2*y2)/2

        be[0] += Ni[0] * l + Ni[1] * x0 * l + Ni[2] * d
        be[2] += Nj[0] * l + Nj[1] * x0 * l + Nj[2] * d
        be[4] += Nk[0] * l + Nk[1] * x0 * l + Nk[2] * d

    be = be*sigm0

    for q in range(3):
        for p in range(3):
            K[2*ijk[e][q]][2*ijk[e][p]] += Ke[2*q][2*p]
            K[2*ijk[e][q]+1][2*ijk[e][p]] += Ke[2*q+1][2*p]
            K[2*ijk[e][q]][2*ijk[e][p]+1] += Ke[2*q][2*p+1]
            K[2*ijk[e][q]+1][2*ijk[e][p]+1] += Ke[2*q+1][2*p+1]

        b[2*ijk[e][q]] += be[2*q]



rem = []
for p in range(ndnum):
    if X[p] < 1e-7:
        rem.append(2*p)
    if Y[p] < 1e-7:
        rem.append(2*p+1)


Krem = np.delete(K, rem, 0)
Krem = np.delete(Krem, rem, 1)

brem = np.delete(b, rem, 0)

urem = np.linalg.solve(Krem, brem)

urem = np.linalg.solve(Krem, brem)

nums = np.delete(range(2*ndnum), rem, 0)


u = [0.0]*(2*ndnum)

i = 0
for n in range(len(nums)):
    u[nums[n]] = urem[n]


for z in K.dot(u) - b:
    if z > 1e+7:
        print('big diff')



file = open(u_x, 'r')
line = file.readline()
ux = []
ndnum = 0
while True:
    line = file.readline()
    if not line:
        break
    ux.append(float(line.split()[-1]))
    ndnum += 1

file = open(u_y, 'r')
line = file.readline()
uy = []
ndnum = 0
while True:
    line = file.readline()
    if not line:
        break
    uy.append(float(line.split()[-1]))
    ndnum += 1

for i in range(ndnum):
    if (abs(u[2*i] - ux[i]) > 1e-3):
        print('big diff')
    if (abs(u[2*i+1] - uy[i]) > 1e-3):
        print('big diff')


import matplotlib.pyplot as plt

# !!! u is scaled 100 times to see the deformation
# !!! this plot represents qualitative information - direction of u
XX = [X[i] + 100*u[2*i] for i in range(ndnum)]
YY = [Y[i] + 100*u[2*i+1] for i in range(ndnum)]

fig, ax = plt.subplots(figsize=(6, 6))

plt.title(r'E = 2e+6, $\nu$ = 0.3, $\sigma_0$ = 1e+3 Pa')

plt.scatter(X, Y, s = 10, color='blue', label='initial nodes')
plt.scatter(XX, YY, s = 10, color='red', label='deformed nodes')

plt.xlim([-1, 6])
plt.xlabel('x, m')
plt.ylabel('y, m')
plt.ylim([-1, 6])
plt.show()

my = []
ms = []

yy = []
ss = []
nn = []
for e in range(enum):
    i = ijk[e][0]
    j = ijk[e][1]
    k = ijk[e][2]

    Ni = Ne[0]
    Nj = Ne[1]
    Nk = Ne[2]

    BN = np.array([
        [Ni[1], 0.0, Nj[1], 0.0, Nk[1], 0.0],
        [0.0, Ni[2], 0.0, Nj[2], 0.0, Nk[2]],
        [Ni[2], Ni[1], Nj[2], Nj[1], Nk[2], Nk[1]]
    ])

    a = np.array([
        u[2*i], u[2*i+1], u[2*j], u[2*j+1], u[2*k], u[2*k+1]
        ])

    eps = BN.dot(a)
    print(eps)
    s = D.dot(eps)

    bnd = []
    for q in ijk[e]:
        if (abs(X[q]) < 1e-7):
            bnd.append(q)

    if len(bnd) == 2:
        ss.append(s[0])
        ss.append(s[0])
        #yy.append((X[bnd[0]]+X[bnd[1]])/2)
        yy.append(Y[bnd[0]])
        yy.append(Y[bnd[1]])


fig, ax = plt.subplots(figsize=(6, 6))

plt.title(r'E = 2e+6, $\nu$ = 0.3, $\sigma_0$ = 1e+3 Pa')

ss = [x for _,x in sorted(zip(yy,ss))]
yy = sorted(yy)
plt.scatter(ss, yy, color='blue')

plt.ylim([-1, 6])
plt.ylabel('y, m')
plt.xlabel(r'$\sigma_x$, Pa')
#plt.xlim([0, 3e+3])
plt.show()