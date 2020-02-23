import pygame
from pygame.locals import *
from pygame.image import *

from utils.Isometric import IsoMathHelper
from manager.MapManager import Map
from manager.MapManagerJSON import MapJSON
from Texture import Texture
from ui.Button import Button


class Game(object):
    def __init__(self, main, ScreenManager, tileSizeX, tileSizeY, map="base"):
        self.main = main
        self.screenManager = ScreenManager
        self.display_surf = ScreenManager.display_surf
        self.middle = ScreenManager.size[0]/2
        self.tileSizeX = tileSizeX  # H
        self.tileSizeY = tileSizeY  # W

        self.IsoMathHelper = None
        self._IsoMathHelperInit()

        self.MapPos = self.MapPosX, self.MapPosY = 0, 0
        self.MapMovConst = 10
        self.RegisterMapMovement()

        self.RecalculateDisplayTiles = True 
        self.RDT_X_S = None
        self.RDT_X_E = None
        self.RDT_Y_S = None
        self.RDT_Y_E = None

        self.Map = Map(map)
        self.Map.loadMap()
        print(self.Map.sizeX)
        self.MapJSON = MapJSON(map)
        self.MapJSON.loadMap()
        print(self.MapJSON.sizeX)
        self.tiles = []
        self.loadTextures()
        self.screenManager.setBackgrounColor(self.screenManager.colors["Black"], 1.0)
        self.MouseSelectedTexture = Texture("resources/graphics/map/select_tile.png")
        self.test = Texture("resources/graphics/map/holzblock.png")
        self.MouseActive = True 
        self.InGameMenuActive = False
        self.button = Button(self.main,
                                        self.display_surf,
                                        self.screenManager.colors["Gray"],
                                        self.screenManager.colors["Blue"],
                                        self.screenManager.colors["Yellow"],
                                        self.screenManager.colors["White"],
                                        self.middle-200,
                                        (self.screenManager.size[1]/10)*2+140,
                                        400, 80,
                                        "Create Level", 60,
                                        self.place)

        self.main.EventHandler.registerKEYDOWNevent(K_ESCAPE, self.KEYDOWNesc)
        self.main.EventHandler.registerMOUSEBUTTONDOWNevent(1, self.place)
        self.button.draw()

    def _IsoMathHelperInit(self):
        self.IsoMathHelper = IsoMathHelper(self.tileSizeY/2, self.tileSizeX/2,
                                           self.screenManager.width/2)

    def draw(self):
        if self.RecalculateDisplayTiles:
            self.RDT()
        for x in range(self.RDT_X_S, self.RDT_X_E):
            for y in range(self.RDT_Y_S, self.RDT_Y_E):
                tile = self.MapJSON.matrix[0][y][x]
                #layer1 = self.MapJSON.matrix[1][y][x]
                tile_x, tile_y = self.IsoMathHelper.Map2ScreenFIN((x, y),
                                                                  self.MapPos)
                self.tiles[tile].draw(tile_x, tile_y)
                #if layer1 = 1:
                #    self.tiles[3].draw(tile_x, tile_y)
        for i in range(len(self.MapJSON.matrix[1])):
            for j in range(len(self.MapJSON.matrix[1][i])):
                layer1 = self.MapJSON.matrix[1][i][j]

                tile_i, tile_j = self.IsoMathHelper.Map2ScreenFIN((j, i),self.MapPos)
                if layer1 == 1:
                    print(tile_i)
                    self.tiles[1].draw(tile_i, tile_j - 50) 

        mouseCoord = self.IsoMathHelper.Screen2MapFIN(pygame.mouse.get_pos(),self.MapPos)

        if -1 < mouseCoord[0] <= self.MapJSON.sizeX and -1 < mouseCoord[1] <= self.MapJSON.sizeY and self.MouseActive:
            select_x, select_y = self.IsoMathHelper.Map2ScreenFIN((int(mouseCoord[0]),int(mouseCoord[1])),self.MapPos)
            self.MouseSelectedTexture.draw(select_x, select_y)
            self.test.draw(select_x, select_y - 50)

    def place(self):
        mouseCoord = self.IsoMathHelper.Screen2MapFIN(pygame.mouse.get_pos(),self.MapPos)
        if -1 < mouseCoord[0] <= self.MapJSON.sizeX and -1 < mouseCoord[1] <= self.MapJSON.sizeY and self.MouseActive:
            select_x, select_y = self.IsoMathHelper.Map2ScreenFIN((int(mouseCoord[0]),int(mouseCoord[1])),self.MapPos)
            self.MapJSON.matrix[1][int(mouseCoord[1]/1)][int(mouseCoord[0]/1)] = 1



    def moveMap(self, dir1, dir2):
        if dir1:
            self.MapPosY += self.MapMovConst
        elif not dir1:
            self.MapPosY -= self.MapMovConst
        if dir2:
            self.MapPosX += self.MapMovConst
        elif not dir2:
            self.MapPosX -= self.MapMovConst

    def moveMapUp(self):
        self.MapPosY += self.MapMovConst
        self.MapPos = self.MapPosX, self.MapPosY
        self.RecalculateDisplayTiles = True

    def moveMapDown(self):
        self.MapPosY -= self.MapMovConst
        self.MapPos = self.MapPosX, self.MapPosY
        self.RecalculateDisplayTiles = True

    def moveMapRight(self):
        self.MapPosX -= self.MapMovConst
        self.MapPos = self.MapPosX, self.MapPosY
        self.RecalculateDisplayTiles = True

    def moveMapLeft(self):
        self.MapPosX += self.MapMovConst
        self.MapPos = self.MapPosX, self.MapPosY
        self.RecalculateDisplayTiles = True

    def RegisterMapMovement(self):
        self.main.EventHandler.registerKEYPRESSEDevent(K_UP, self.moveMapUp)
        self.main.EventHandler.registerKEYPRESSEDevent(K_DOWN, self.moveMapDown)
        self.main.EventHandler.registerKEYPRESSEDevent(K_LEFT, self.moveMapLeft)
        self.main.EventHandler.registerKEYPRESSEDevent(K_RIGHT, self.moveMapRight)

    def loadTextures(self):
        for TextureSrc in self.MapJSON.textures:
            self.tiles.append(Texture("resources/graphics/map/" + TextureSrc + ".png"))

    def checkEdges(self):
        if self.MapPosY < -self.IsoMathHelper.Map2Screen((self.MapJSON.sizeX, self.MapJSON.sizeY-(self.screenManager.width*1.5)/self.tileSizeY))[1]:
            self.MapPosY = -self.IsoMathHelper.Map2Screen((self.MapJSON.sizeX, self.MapJSON.sizeY-(self.screenManager.width*1.5)/self.tileSizeY))[1]
        elif self.MapPosY > self.screenManager.width/4:
            self.MapPosY = int(self.screenManager.width/4)

        if self.MapPosX > self.IsoMathHelper.Map2Screen((int(self.MapJSON.sizeX+(self.screenManager.height*0.25)/self.tileSizeX), self.MapJSON.sizeY))[1]:
            self.MapPosX = self.IsoMathHelper.Map2Screen((int(self.MapJSON.sizeX+(self.screenManager.height*0.25)/self.tileSizeX), self.MapJSON.sizeY))[1]
        elif self.MapPosX < -self.IsoMathHelper.Map2Screen((int(self.MapJSON.sizeX+(self.screenManager.height*0.25)/self.tileSizeX), self.MapJSON.sizeY))[1]:
            self.MapPosX = -self.IsoMathHelper.Map2Screen((int(self.MapJSON.sizeX+(self.screenManager.height*0.25)/self.tileSizeX), self.MapJSON.sizeY))[1]

    def RDT(self):
        self.checkEdges()
        TopLeft = self.IsoMathHelper.Screen2MapFIN((0, 0), self.MapPos)
        TopRight = self.IsoMathHelper.Screen2MapFIN((self.screenManager.width, 0),
                                                    self.MapPos)
        BottomRight = self.IsoMathHelper.Screen2MapFIN((self.screenManager.height,
                                                        self.screenManager.width),
                                                       self.MapPos)
        BottomLeft = self.IsoMathHelper.Screen2MapFIN((0, self.screenManager.height),
                                                      self.MapPos)

        self.RDT_X_S = int(TopLeft[0]) - 2
        self.RDT_X_E = int(BottomRight[0]) + 2

        self.RDT_Y_S = int(TopRight[1]) - 2
        self.RDT_Y_E = int(BottomLeft[1]) + 2

        if self.RDT_X_S < 0:
            self.RDT_X_S = 0
        elif self.RDT_X_S > self.MapJSON.sizeX:
            self.RDT_X_S = self.MapJSON.sizeX

        if self.RDT_X_E < 0:
            self.RDT_X_E = 0
        elif self.RDT_X_E > self.MapJSON.sizeX:
            self.RDT_X_E = self.MapJSON.sizeX

        if self.RDT_Y_S < 0:
            self.RDT_Y_S = 0
        elif self.RDT_Y_S > self.MapJSON.sizeY:
            self.RDT_Y_S = self.MapJSON.sizeY

        if self.RDT_Y_E < 0:
            self.RDT_Y_E = 0
        elif self.RDT_Y_E > self.MapJSON.sizeY:
            self.RDT_Y_E = self.MapJSON.sizeY

        self.RecalculateDisplayTiles = False

    def KEYDOWNesc(self):
        print("Hi")

    def openInGameMenu(self):
        self.MouseActive = False
        self.InGameMenuActive = True

    def closeInGameMenu(self):
        self.MouseActive = True
        self.InGameMenuActive = False

    def stop(self):
        pass
