import pygame

from Texture import Texture


class Button(object):
    def __init__(self, main, surface, in_color, bord_color,
                 hover_color, text_color, x, y, sizeX, sizeY,
                 text, textSize, onClick, border=5, onClickIdent=None):
        self.main = main
        self.surface = surface
        self.in_color = in_color
        self.bord_color = bord_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.pos = self.x, self.y = x, y
        self.size = self.sizeX, self.sizeY = sizeX, sizeY
        self.border = border
        self.text = text
        self.textSize = textSize
        self.onClick = onClick
        self.onClickIdent = onClickIdent

        self.Rect = None
        self.InRect = None
        self.HoverSurf = None
        self.BordSurf = None
        self.HoverTexture = None
        self.BordTexture = None

        self.textFont = None
        self.textSurf = None
        self.textRect = None

        self._initRect()
        self._initText()
        self._genTextures()
        self._registerClick()

    def _initRect(self):
        self.Rect = pygame.Rect(0, 0, self.sizeX, self.sizeY)
        self.InRect = pygame.Rect(self.border, self.border, 
                                  self.sizeX-self.border*2,
                                  self.sizeY-self.border*2)

    def _genTextures(self):
        self.BordSurf = pygame.Surface(self.size)
        self.HoverSurf = pygame.Surface(self.size)

        pygame.draw.rect(self.BordSurf, self.bord_color, self.Rect, self.border)
        pygame.draw.rect(self.BordSurf, self.in_color, self.InRect, 0)
        self.BordSurf.blit(self.textSurf, self.textRect)

        pygame.draw.rect(self.HoverSurf, self.hover_color, self.Rect, self.border)
        pygame.draw.rect(self.HoverSurf, self.in_color, self.InRect, 0)
        self.HoverSurf.blit(self.textSurf, self.textRect)

        self.HoverTexture = Texture(None, self.HoverSurf, self.Rect)
        self.BoardTexture = Texture(None, self.BordSurf, self.Rect)

    def _initText(self):
        self.font = pygame.font.Font(None, self.textSize)
        self.textSurf = self.font.render(self.text, True, self.text_color)
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = self.InRect.center

    def draw(self):
        if self.isHover():
            self.HoverTexture.draw(self.x, self.y)
        else:
            self.BoardTexture.draw(self.x, self.y)

    def isHover(self):
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.sizeX + self.x and self.y < pos[1] < self.sizeY + self.y:
            return True
        return False

    def _onClick(self):
        if self.isHover():
            if self.onClickIdent is None:
                self.onClick()
            else:
                self.onClick(self.onClickIdent)

    def _registerClick(self):
        self.main.EventHandler.registerMOUSEBUTTONDOWNevent(1, self._onClick)

    def stop(self):
        try:
            del(self.HoverTexture)
        except:
            pass
        try:
            del(self.BoardTexture)
        except:
            pass
        self.main.EventHandler.unregisterMOUSEBUTTONDOWNevent(1, self._onClick)

    def __del__(self):
        self.stop()