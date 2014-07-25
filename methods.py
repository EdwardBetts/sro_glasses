import os

def fileLength(file):
    return sum(1 for line in file)


def reformatFile(file):
    try:
        os.remove("tmp")
    except:
        pass
    for i in range(fileLength(file)):
        if i > 1 and file[i].split()[0] == "0":
            open("tmp", "a").write("{} {}\n".format(10000 + i - 1, ' '.join(file[i].split()[1:4])))
        elif file[i].split()[0] == "1":
            open("tmp", "a").write("{} {}\n".format(10000 - i, ' '.join(file[i].split()[1:4])))

def density(file):
    return  (99.63232692/(float(file[1].split()[1])**3))*1000


def distance(a, b, L):
    dummy = 0
    for i in range(3):
        u = a[i] - b[i]
        if u > L/2:
            u -= L
        elif u < -L/2:
            u += L
        dummy += u*u
    return dummy ** 0.5


def getCoordinates(file):
    at_coords = {}
    reformatFile(file)
    for line in open("tmp", "r").readlines():
        at_coords[int(line.split()[0])] = map(float, line.split()[1:4])
    return at_coords


def getNeighbors(file):
    at_neighbors = {}
    L = float(file[1].split()[1])
    coords = getCoordinates(file)
    os.system("voro++ -p -c \"%i %n \" -{0} {0} -{0} {0} -{0} {0} tmp".format(L / 2))
    fp = open("tmp.vol", 'r').readlines()
    for line in fp:
        central = line.split()[0]
        at_neighbors[int(central)] = []
        for atom in line.split()[1:]:
            if distance(coords.get(int(central)), coords.get(int(atom)), L) < 2.0:
                at_neighbors[int(central)].append(int(atom))
    return at_neighbors


def coordNumber_Si(file):
    try:
        os.system("rm -f coord_*.dat")
    except:
        pass
    coord_num = {}
    count = 0
    neighbors = getNeighbors(file)
    for key in neighbors.keys():
        if key > 10000:
            coord_num[len(neighbors[key])] = coord_num.get(len(neighbors[key]), 0) + 1
            count += 1
    for key in coord_num.keys():
        open("coord_{}.dat".format(key), "a").write("{:.3f}\t{}".format(density(file), 100 * float(coord_num[key]) / count))
    return coord_num


