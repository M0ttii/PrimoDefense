
from OpenGL.GL import *
from OpenGL.GLUT import *

from Texture import Text
from ui.Button import Button


class Menu(object):
    def __init__(self, main, screenManager):
        self.main = main
        self.screenManager = screenManager
        self.display_surf = screenManager.display_surf
        self.colors = screenManager.colors
        self.middle = screenManager.size[0]/2
        self.logo = Text("Primo Defense - Level Creator", 30, self.colors["White"], self.middle-130,
                         self.screenManager.size[1]/10)

        self.createButtons()
        self.screenManager.setBackgrounColor(self.colors["Black"])

    def draw(self):
        self.logo.draw()
        self.CreateButton.draw()
        self.OpenButton.draw()
        self.image.draw()

    def createButtons(self):
        self.CreateButton = Button(self.main,
                                        self.display_surf,
                                        self.colors["Gray"],
                                        self.colors["Blue"],
                                        self.colors["Yellow"],
                                        self.colors["White"],
                                        self.middle-200,
                                        (self.screenManager.size[1]/10)*2+140,
                                        400, 80,
                                        "Create Level", 60,
                                        self.LevelEditor)

        self.OpenButton = Button(self.main,
                                        self.display_surf,
                                        self.colors["Gray"],
                                        self.colors["Blue"],
                                        self.colors["Yellow"],
                                        self.colors["White"],
                                        self.middle-200,
                                        (self.screenManager.size[1]/10)*2+240,
                                        400, 80,
                                        "Open Level", 60,
                                        self.LevelEditor)


    def LevelEditor(self):
        print("LevelEditor")


    def stop(self):
        try:
            self.LevelEditorButton.stop()
            del(self.LevelEditorButton)
        except:
            pass

    def __del__(self):
        self.stop()