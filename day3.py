import numpy as np

n = 10
a = 0
b = 1

x = np.arange(a,b+(b-a)/(n),(b-a)/(n))
print(x)

class N:
    def __init__(self, i) -> None:
        self.i = i
    def val(self, t):
        if (self.i==1):
            if (t >= x[1]):
                return 0
            elif (t <= x[1]):
                return (x[1]-t)/(x[1]-x[0])
        elif (self.i==n):
            if (t <= x[n-1]):
                return 0
            elif (t >= x[n-1]):
                return (t-x[n-1])/(x[n]-x[n-1])
        else:
            if (t <= x[self.i-1]):
                return 0
            elif (t <= x[self.i]):
                return (t-x[self.i-1])/(x[self.i]-x[self.i-1])
            elif (t <= x[self.i+1]):
                return (x[self.i+1]-t)/(x[self.i+1]-x[self.i])
            else:
                return 0
    def diffval(self, t):
        if (self.i==1):
            if (t >= x[1]):
                return 0
            elif (t <= x[1]):
                return -1/(x[1]-x[0])
        elif (self.i==n):
            if (t <= x[n-1]):
                return 0
            elif (t >= x[n-1]):
                return 1/(x[n]-x[n-1])
        else:
            if (t <= x[self.i-1]):
                return 0
            elif (t <= x[self.i]):
                return 1/(x[self.i]-x[self.i-1])
            elif (t <= x[self.i+1]):
                return -1/(x[self.i+1]-x[self.i])
            elif (t >= x[self.i+1]):
                return 0

NN = [N(1)]

for i in range(1, n+1):
    NN.append(N(i))

print(NN[2].val(0.25))

xdiv = np.arange(a,b+(b-a)/(4*n),(b-a)/(4*n))

def integral(l):
    y = []
    i = 0
    while (xdiv[i] < b):
        y.append(NN[l].val(xdiv[i]))
        i += 1
    return np.trapz(y, xdiv)

def find(l, m):
    y = []
    i = 0
    while (xdiv[i] < b):
       y.append(NN[l].diffval(xdiv[i])*NN[m].diffval(xdiv[i])-NN[l].val(xdiv[i])*NN[m].val(xdiv[i]))
       i += 1


Kee = [[0 for _ in range(n)] for _ in range(n)]
f = [0 for _ in range(n)]

for l in range(n):
    for m in range(n):
        f[l] = -integral(l+1)
        #Kee[l][m] = find(l+1, m+1)