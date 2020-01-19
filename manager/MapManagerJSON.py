import numpy
import json

class Map(object):
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
        self.matrix = None

    def createMap(self, name, author, desc, textures, sizeX, sizeY):
        self.name = name
        self.desc = desc
        self.textures = textures
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.matrix = numpy.array([[0 for _y in range(sizeY)] for _x in range(sizeX)],dtype=numpy.int8)
