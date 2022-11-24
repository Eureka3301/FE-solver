class nodes:
    def __init__(self, filename):
        file = open(filename, "r")

        line = file.readline()
        self.X = []
        self.Y = []
        self.stress = []
        while True:
            line = file.readline()
            if not line:
                break
            lst = list(map(float, line.split()))
            self.stress.append(lst.pop())
            lst.pop()
            self.Y.append(lst.pop())
            self.X.append(lst.pop())

        file.close

    def plot_mesh(self):
        import matplotlib.pyplot as plt

        plt.title("mesh")
        plt.scatter(self.X, self.Y)
        plt.show()

class elements:
    def __init__(self, filename, nodes):
        self.nodes = nodes

        file = open(filename, "r")

        line = file.readline()
        self.elNodes = []
        while True:
            line = file.readline()
            if not line:
                break
            self.elNodes.append(list(map(int, line.split()[2:])))

        file.close

        import numpy as np
        self.Ne = []
        for elnum in range(len(self.elNodes)):
            A = np.matrix([[1, nds.X[self.elNodes[elnum][0]-1], nds.Y[self.elNodes[elnum][0]-1]],
                           [1, nds.X[self.elNodes[elnum][1]-1], nds.Y[self.elNodes[elnum][1]-1]],
                           [1, nds.X[self.elNodes[elnum][2]-1], nds.Y[self.elNodes[elnum][2]-1]]])
            invA = np.linalg.inv(A)
            invAtr = np.transpose(invA)
            self.Ne.append([invAtr[0], invAtr[1], invAtr[2]])


################################ main part of the program #############################################

nds = nodes("ndsXstress.txt")
elms = elements("elms.txt", nds)

print(elms.Ne[0])
print(elms.elNodes[0])
