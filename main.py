# el from HW task
elnum = 5
nodnum = 5
el = [
    [0, 1, 1],
    [1, 2, 1],
    [2, 3, 1],
    [1, 3, 1],
    [3, 4, 1]
]

def Kee(el):
    Kee = [[0 for _ in range(nodnum)] for _ in range(nodnum)]
    for i in range(elnum):
        Kee[el[i][0]][el[i][0]] += - el[i][2]
        Kee[el[i][0]][el[i][1]] += + el[i][2]
        Kee[el[i][1]][el[i][0]] += + el[i][2]
        Kee[el[i][1]][el[i][1]] += - el[i][2]
    return Kee

print(Kee(el))