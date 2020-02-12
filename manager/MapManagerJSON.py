import numpy
import json

class MapJSON(object):
    def __init__(self, src):
        self.Header = "PrimoAttack"
        if src[-5:] == ".json":
            self.src = src[:-5]
        else:
            self.src = src
        self.MAP_FOLDER = "resources/levels/"
        self.name = None
        self.desc = None
        self.textures = None
        self.sizeX = None
        self.sizeY = None
        self.matrix = {}

    def createMap(self, name, author, desc, textures, sizeX, sizeY):
        self.name = name
        self.desc = desc
        self.textures = textures
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.matrix = numpy.array([[0 for _y in range(sizeY)] for _x in range(sizeX)],dtype=numpy.int8)

    def loadMap(self):
        with open('resources/levels/' + self.src  + '.json') as map:
            map = json.load(map)

        self.name = map['name']
        self.sizeX = map['sizex']
        self.sizeY = map['sizey']
        self.textures = []
        for t in map['textures']:
            self.textures.append(t)
        for i in range(len(map['matrixlayers'])):
            self.matrix[i] = map['matrixlayers'][i]['matrix']
        print(self.matrix[0][0][0])

    def editMatrix(self, layer, x, y, value):
        self.matirx[layer][x][y] = value


        

        

