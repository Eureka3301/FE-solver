import numpy as np
from numpy.linalg import inv

def triag_square(x, y):
    a = np.array([
        [1, x[0], y[0]],
        [1, x[1], y[1]],
        [1, x[2], y[2]]
    ])
    return 0.5*np.linalg.det(a)

def dist(x, y):
    return np.square((x[1]-x[0])**2+(y[1]-y[0])**2)

class Element:
    def __init__(self, nodenums, invA) -> None:
        self.nd_nums = nodenums
        invA = np.array(invA)
        self.N = [invA[:,0], invA[:,1], invA[:,2]]

class Node:
    def __init__(self, X, Y) -> None:
        self.X = X
        self.Y = Y

class Mesh():
    def __init__(self, nodes_input, elements_input) -> None:
        self.get_nodes(nodes_input)
        self.get_elements(elements_input)

    def nodes_in_loc(self, x, y):
        res = []
        if x == 'any' and y != 'any':
            for nd_num in range(1, self.nodes_num+1):
                if self.nodes[nd_num-1].Y == y:
                    res.append(nd_num)
        elif x != 'any' and y == 'any':
            for nd_num in range(self.nodes_num):
                if self.nodes[nd_num-1].X == x:
                    res.append(nd_num)
        elif x != 'any' and y != 'any':
            for nd_num in range(self.nodes_num):
                if self.nodes[nd_num-1].X == x and self.nodes[nd_num-1].Y == y:
                    res.append(nd_num)
        return res

    def get_nodes(self, filename):
        file = open(filename, 'r')
        line = file.readline()
        self.nodes = []
        while True:
            line = file.readline()
            if not line:
                break
            [X, Y] = list(map(float, line.split()[1:3]))
            self.nodes.append(Node(X, Y))
        self.nodes_num = len(self.nodes)

    def get_elements(self, filename):
        file = open(filename, 'r')
        line = file.readline()
        self.elements = []
        while True:
            line = file.readline()
            if not line:
                break
            nums = list(map(int, line.split()[2:]))
            A = [
                [1, self.nodes[nums[0]-1].X, self.nodes[nums[0]-1].Y],
                [1, self.nodes[nums[1]-1].X, self.nodes[nums[1]-1].Y],
                [1, self.nodes[nums[2]-1].X, self.nodes[nums[2]-1].Y]
            ]
            self.elements.append(Element(nums, inv(A)))
        self.elements_num = len(self.elements)
        
def fe_solve(mesh, E, nu, sigm0):
    b = np.array([0.0]*(2*mesh.nodes_num))
    K = np.array([[0.0]*(2*mesh.nodes_num) for _ in range(2*mesh.nodes_num)])

    def integrate(Ke, be, nums):
        for i in range(3):
            for j in range(3):
                K[nums[i]-1][nums[j]-1] += Ke[2*i][2*j]
                K[nums[i]][nums[j]] += Ke[2*i+1][2*j+1]
            b[nums[i]-1] += be[i]
            b[nums[i]] += be[2*i+1]

    def task(mesh, elem, bond, E, nu):
        Ke = [[0.0]*6 for _ in range(6)]
        be = [0.0]*6

        Ni = elem.N[0]
        Nj = elem.N[1]
        Nk = elem.N[2]

        BN = np.array([
            [Ni[1], 0, Nj[1], 0, Nk[1], 0],
            [0, Ni[2], 0, Nj[2], 0, Nk[2]],
            [Ni[2], Ni[1], Nj[2], Nj[1], Nk[2], Nk[1]]
        ])

        invD = np.array([
            [1, -nu, 0],
            [-nu, 1, 0],
            [0, 0, 2*(1+nu)]
        ])

        D = np.linalg.inv(invD)
        D = E * D

        xx = [mesh.nodes[elem.nd_nums[0]-1].X, mesh.nodes[elem.nd_nums[1]-1].X, mesh.nodes[elem.nd_nums[2]-1].X]
        yy = [mesh.nodes[elem.nd_nums[0]-1].Y, mesh.nodes[elem.nd_nums[1]-1].Y, mesh.nodes[elem.nd_nums[2]-1].Y]

        S = triag_square(xx, yy)

        Ke = S * np.matmul(np.matmul(BN.transpose(), D), BN)
        be = [0]*6

        bnd = []
        for nd_num in elem.nd_nums:
            if nd_num in bond:
                bnd.append(nd_num)

        if len(bnd) == 2:
            xx = [mesh.nodes[bnd[0]-1].X, mesh.nodes[bnd[1]-1].X]
            yy = [mesh.nodes[bnd[0]-1].Y, mesh.nodes[bnd[1]-1].Y]

            l = dist(xx, yy)

            x0 = 10.0

            for i in range(3):
                be[2*i] += elem.N[i][0]*l
                be[2*i] += elem.N[0][1]*x0*l
                be[2*i] += elem.N[0][2]*abs(mesh.nodes[bnd[0]-1].Y**2 - mesh.nodes[bnd[1]-1].Y**2)/2
        
        return [Ke, be]

    for elem in mesh.elements:
        [Ke, be] = task(mesh, elem, mesh.nodes_in_loc(10, 'any'), E, nu)
        integrate(Ke, be, elem.nd_nums)

    rem = np.array([])

    rem = np.append(rem, mesh.nodes_in_loc(0, 'any'))
    rem = np.append(rem, mesh.nodes_in_loc('any', 0))
    rem = np.append(rem, rem-1)

    rem = list(map(int, rem))

    K = np.delete(K, rem, 0)
    b = np.delete(b, rem, 0)
    K = np.delete(K, rem, 1)

    return [K, b]

# *****************************************************************************************************


mesh = Mesh('nodes.txt', 'elements.txt')

E = 2e+11
nu = 0.3
sigm0 = 1e+7

[K, b] = fe_solve(mesh, E, nu, sigm0)


u = np.linalg.solve(K, b)
