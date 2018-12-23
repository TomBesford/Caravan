import sprites, pygame
from random import shuffle

class Deck():
    def __init__(self, jokers=True):
        self.cards = []
        for suit in ['Spades', 'Hearts', 'Clubs', 'Diamonds']:
            for value, value_string in enumerate(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']):
                self.cards.append(Card(value+1, value_string, suit))
        if jokers:
            for i in range(2):
                self.cards.append(Card(14, 'Joker'))
    
    def shuffle(self):
        shuffle(self.cards)

class Card():
    def __init__(self, value, value_string, suit=''):
        self.suit = suit
        self.value = value
        self.sprite = sprites.CardSprite('../img/card' + suit + value_string + '.png')

class Hand():
    def __init__(self, parent):
        self.cards = []
        self.sprite_group = pygame.sprite.OrderedUpdates()
        self.parent = parent
        self.draw(8)
    
    def draw(self, amount):#Draw cards from the top of a deck
        for i in range(amount):
            self.cards.append(self.parent.cards[0])
            self.sprite_group.add(self.parent.cards[0].sprite)
            self.parent.cards.pop(0)
    
    def remove(self, card, destination=None, index=-1, draw=0):
        if destination is not None and index == -1:#Add card to end of caravan
            destination.cards.append([card])
            destination.sprite_groups.append(pygame.sprite.OrderedUpdates())
            destination.sprite_groups[-1].add(card.sprite)
            destination.update()
        elif destination is not None and index != -1:#Add card to card in caravan
            destination.cards[index].append(card)
            destination.sprite_groups[index].add(card.sprite)
            destination.update()
        self.cards.remove(card)
        self.sprite_group.remove(card.sprite)
        
        self.draw(draw)

class Track():
    def __init__(self):
        self.cards = []
        self.sprite_groups = []
        self.total = 0
        self.direction = 0
    
    def remove(self, index=None):
        if index is not None:
            self.cards.pop(index)
            self.sprite_groups.pop(index)
        else:
            self.cards = []
            self.sprite_groups = []
        self.update()
    def update(self):
        #Total
        self.total = 0
        for i in range(len(self.cards)):
            value = self.cards[i][0].value
            for ii in range(1, len(self.cards[i])):
                if self.cards[i][ii].value == 13:
                    value = value * 2
            self.total += value
        
        #Direction
        if len(self.cards) > 1:
            if self.cards[-1][0].value > self.cards[-2][0].value:
                self.direction = 1
            elif self.cards[-1][0].value < self.cards[-2][0].value:
                self.direction = -1
            else:
                self.direction = 0
            
            for card in self.cards[-1]:
                if card.value == 12:
                    self.direction = self.direction * -1
        else:
            self.direction = 0