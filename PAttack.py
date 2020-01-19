import pygame, sys
from manager.ScreenManager import ScreenManager
from manager.EventHandler import EventHandler


class main(object):
    def __init__(self):
        #self.logger = Logger(True)

        self.EventHandler = EventHandler(self)
        self.ScreenManager = ScreenManager(self, 1024, 600, 30)
        self.loop = True
        self.run()

    def run(self):
        while self.loop:
            self.ScreenManager.clearScreen()
            self.EventHandler.tick()
            if not self.loop:
                break
            self.ScreenManager.draw()
            self.ScreenManager.UpdateDisplay()

    def quit(self):
        self.loop = False
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = main()