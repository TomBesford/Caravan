import pygame
from variables import *

class CardSprite(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
    
class SelectedSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.green = pygame.image.load('../img/cardOverlay_green.png')
        self.red = pygame.image.load('../img/cardOverlay_red.png')
        self.image = self.green
        self.rect = self.image.get_rect()

class BidSprite(pygame.sprite.Sprite):
    def __init__(self, origin, track_in_focus):
        pygame.sprite.Sprite.__init__(self)
        self.origin = origin
        self.track_in_focus = track_in_focus
        self.font = pygame.font.SysFont('Helvetica', 32)
        self.colour = BLACK
        self.update()
    
    def update(self):
        self.number = self.track_in_focus.total
        
        if self.number >= 21 and self.number <= 26:
            self.colour = GREEN
        elif self.number > 26:
            self.colour = RED
        else:
            self.colour = BLACK
        
        self.image = self.font.render(str(self.number), False, self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = self.origin[0] - self.rect[2]/2
        self.rect.y = self.origin[1] - self.rect[3]/2
        
class CardsRemainingSprite(pygame.sprite.Sprite):
    def __init__(self, origin, deck):
        pygame.sprite.Sprite.__init__(self)
        self.origin = origin
        self.font = pygame.font.SysFont('Helvetica', 32)
        self.colour = BLACK
        self.deck = deck
        self.update()
    
    def update(self):
        self.number = len(self.deck.cards)
        self.image = self.font.render(str(self.number), False, self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = self.origin[0] - self.rect[2]/2
        self.rect.y = self.origin[1] - self.rect[3]/2 - self.number
        
class MessageSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, message, colour):
        pygame.sprite.Sprite.__init__(self)
        font = pygame.font.SysFont('Helvetica', 64)
        text = font.render(message, False, colour)
        self.rect = text.get_rect()
        self.rect.x = x - self.rect[2]/2
        self.rect.y = y - self.rect[3]/2
        self.image = pygame.Surface((self.rect[2], self.rect[3]))
        self.image.fill(BLACK)
        self.image.blit(text, (0, 0))
        