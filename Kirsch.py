class Element:
    def __init__(self, nodenums, invA) -> None:
        self.nodes = nodenums
        # костыль для извлечения столбца из invA
        # если можно сделать это элегантно, то лучше поменять
        # например, транспонировать и взять строки
        import numpy as np
        invA = np.array(invA)
        #
        self.N = [invA[:,0], invA[:,1], invA[:,2]]

class Node:
    def __init__(self, X, Y) -> None:
        self.X = X
        self.Y = Y

class Mesh():
    def __init__(self, nodes_input, elements_input) -> None:
        self.get_nodes(nodes_input)
        self.get_elements(elements_input)

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

    def get_elements(self, filename):
        from numpy.linalg import inv
        file = open(filename, 'r')
        line = file.readline()
        self.elements = []
        while True:
            line = file.readline()
            if not line:
                break
            nums = list(map(int, line.split()[2:]))
            A = [[1, self.nodes[nums[0]-1].X, self.nodes[nums[0]-1].Y],
                 [1, self.nodes[nums[1]-1].X, self.nodes[nums[1]-1].Y],
                 [1, self.nodes[nums[2]-1].X, self.nodes[nums[2]-1].Y]]
            self.elements.append(Element(nums, inv(A)))

# *********************************************************************


mesh = Mesh('nodes.txt', 'elements.txt')

