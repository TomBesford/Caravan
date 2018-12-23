import pygame
from variables import *
from cards import *
from sprites import BidSprite, CardsRemainingSprite, MessageSprite
from ai import AI

class Main():
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOWSIZE, pygame.RESIZABLE)
        pygame.display.set_caption('Caravan')
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.font.init()
        self.state = PREGAME
        self.p1_card_back = pygame.image.load('../img/cardBack_blue.png')
        self.p2_card_back = pygame.image.load('../img/cardBack_red.png')
        self.numbers = pygame.sprite.Group()
        self.selected_card_overlay = sprites.SelectedSprite()
        self.newGame()
    
    def mainLoop(self):
        self.isRunning = True
        
        while(self.isRunning):
            self.clock.tick(60)
            self.event()
            
        pygame.quit()
    
    def draw(self):
        surface = pygame.Surface(SCREENSIZE)
        surface.fill(BGCOLOUR)
        
        if self.state != PREGAME:
            #Players hands
            self.p1_hand.sprite_group.draw(surface)
            for i in range(len(self.p2_hand.cards)):
                surface.blit(self.p2_card_back, (P2HAND[0] - CARDOFFSETX * (len(self.p2_hand.cards)-i), P2HAND[1]))
            
            #Players decks
            for i in range(len(self.p1_deck.cards)):
                surface.blit(self.p1_card_back, (P1DECK[0], P1DECK[1]-i))
            for i in range(len(self.p2_deck.cards)):
                surface.blit(self.p2_card_back, (P2DECK[0], P2DECK[1]-i))
            
            #Bids and remaining cards
            self.numbers.draw(surface)
            
            #Tracks
            for i in range(6):
                for ii in range(len(self.tracks[i].sprite_groups)):
                    self.tracks[i].sprite_groups[ii].draw(surface)
            
            #Selected card sprite
            if self.state == P1PLAY:
                surface.blit(self.selected_card.sprite.image, (self.selected_card_overlay.rect.x, self.selected_card_overlay.rect.y))
                surface.blit(self.selected_card_overlay.image, (self.selected_card_overlay.rect.x, self.selected_card_overlay.rect.y))
        
        window_width, window_height = self.screen.get_size()
        if window_width/16 <= window_height/9:
            width = window_width
            height = round((window_width/16)*9)
        elif window_width/16 > window_height/9:
            width = round((window_height/9)*16)
            height = window_height
            
        if self.state == GAMEOVER:
            winner = self.getWinner()
            if winner == 1:
                message = 'You Win!'
                colour = GREEN
            elif winner == 2:
                message = 'You lose.'
                colour = RED
            sprite = MessageSprite(SCREENSIZE[0]/2, SCREENSIZE[1]/2, message, colour)
            surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        
        transformed_surface = pygame.Surface((width, height))
        pygame.transform.scale(surface, (width, height), transformed_surface)
        self.screen.fill(BGCOLOUR)
        self.screen.blit(transformed_surface, (round((window_width-width)/2), round((window_height-height)/2)))
        
        pygame.display.flip()
    
    def update(self):
        self.numbers.update()
        
        for i, card in enumerate(self.p1_hand.cards):
            card.sprite.rect.x = P1HAND[0] - CARDOFFSETX * (len(self.p1_hand.cards)-1-i)
            if self.state == P1SELECT and i <= self.card_in_focus:
                card.sprite.rect.x -= CARDOFFSETX * 3
            card.sprite.rect.y = P1HAND[1]
        
        for i, card in enumerate(self.p2_hand.cards):
            card.sprite.rect.x = P2HAND[0] - CARDOFFSETX * (len(self.p2_hand.cards)-1-i)
            card.sprite.rect.y = P2HAND[1]
        
        for i in range(6):
            for ii in range(len(self.tracks[i].cards)):
                for iii, card in enumerate(self.tracks[i].cards[ii]):
                    if i < 3:
                        card.sprite.rect.x = TRACKS[i][0] + CARDOFFSETX * iii
                        card.sprite.rect.y = TRACKS[i][1] + CARDOFFSETY * ii
                    else:
                        card.sprite.rect.x = TRACKS[i][0] - CARDOFFSETX * iii
                        card.sprite.rect.y = TRACKS[i][1] - CARDOFFSETY * ii
        
        if self.state == P1PLAY:
            if self.selected_card.value > 10:
                if len(self.tracks[self.track_in_focus].cards):
                    x_offset = CARDOFFSETX * len(self.tracks[self.track_in_focus].cards[self.card_in_focus])
                else:
                    x_offset = 0
                
                if self.track_in_focus < 3:
                    self.selected_card_overlay.rect.x = TRACKS[self.track_in_focus][0] + x_offset
                    self.selected_card_overlay.rect.y = TRACKS[self.track_in_focus][1] + CARDOFFSETY * self.card_in_focus
                else:
                    self.selected_card_overlay.rect.x = TRACKS[self.track_in_focus][0] - x_offset
                    self.selected_card_overlay.rect.y = TRACKS[self.track_in_focus][1] - CARDOFFSETY * self.card_in_focus
            else:
                if self.state is P1PLAY:
                    self.selected_card_overlay.rect.x = TRACKS[self.track_in_focus][0]
                    self.selected_card_overlay.rect.y = TRACKS[self.track_in_focus][1] + CARDOFFSETY * len(self.tracks[self.track_in_focus].cards)
                elif self.state is P2PLAY:
                    self.selected_card_overlay.rect.x = TRACKS[self.track_in_focus][0]
                    self.selected_card_overlay.rect.y = TRACKS[self.track_in_focus][1] - CARDOFFSETY * len(self.tracks[self.track_in_focus].cards)
        
            if self.isLegal():
                self.selected_card_overlay.image = self.selected_card_overlay.green
            else:
                self.selected_card_overlay.image = self.selected_card_overlay.red
        
        if self.getWinner():
            self.changeState(GAMEOVER)
    
    def event(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.isRunning = False
                
            if event.type == pygame.KEYDOWN:
                if self.state != PREGAME and self.state != GAMEOVER:
                    if event.key == pygame.K_LEFT:
                        self.changeFocus(h_change=-1)
                        
                    if event.key == pygame.K_RIGHT:
                        self.changeFocus(h_change=1)
                        
                    if event.key == pygame.K_UP:
                        if self.track_in_focus < 3: change = -1
                        else: change = 1
                        
                        self.changeFocus(v_change=change)
                        
                    if event.key == pygame.K_DOWN:
                        if self.track_in_focus < 3: change = 1
                        else: change = -1
                        
                        self.changeFocus(v_change=change)
                        
                    if event.key == pygame.K_w:
                        if self.state == P1SELECT:
                            self.selectCard()
                        elif self.state == P1PLAY:
                            self.playCard()
                        
                    if event.key == pygame.K_q:
                        if self.state == P1SELECT or self.state == P1PLAY:
                            self.discardCard()
                        
                    if event.key == pygame.K_e:
                        if self.state == P1PLAY:
                            self.discardTrack()
                        
                    if event.key == pygame.K_r:
                        if self.state == P1PLAY:
                            self.cancelSelection()
                
                if event.key == pygame.K_RETURN:
                    self.newGame()
                    
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
        if len(events):
            if self.state != PREGAME and self.state != GAMEOVER:
                self.update()
            self.draw()
    
    def newGame(self):
        self.numbers.empty()
        
        self.p1_deck = Deck()
        self.p1_deck.shuffle()
        self.p1_hand = Hand(self.p1_deck)
        self.p1_cards_remaining = CardsRemainingSprite(P1CARDSREMAINING, self.p1_deck)
        self.numbers.add(self.p1_cards_remaining)
        
        self.p2_deck = Deck()
        self.p2_deck.shuffle()
        self.p2_hand = Hand(self.p2_deck)
        self.p2_cards_remaining = CardsRemainingSprite(P2CARDSREMAINING, self.p2_deck)
        self.numbers.add(self.p2_cards_remaining)
        self.ai = AI(self)
        
        self.tracks = [Track() for i in range(6)]
        self.bid_totals = []
        for i in range(6):
            self.bid_totals.append(BidSprite(BIDTOTALS[i], self.tracks[i]))
            self.numbers.add(self.bid_totals[i])
            
        self.isOpeningBids = True
        self.changeState(P1SELECT)
        self.update()
        self.draw()
    
    def changeFocus(self, h_change=0, v_change=0):
        if self.state == P1SELECT:
            self.card_in_focus = wrap(0, len(self.current_hand.cards), self.card_in_focus + h_change)
        elif self.state == P1PLAY:
            if self.track_in_focus < 3:
                start = 0
                stop = 3
            else:
                start = 3
                stop = 6
                
            self.track_in_focus = wrap(start, stop, self.track_in_focus + h_change)
            
            if self.selected_card.value > 10:
                if self.card_in_focus == 0 and v_change < 0:
                    self.track_in_focus = wrap(0, 6, self.track_in_focus + 3)
                else:
                    self.card_in_focus = wrap(0, max(1, len(self.tracks[self.track_in_focus].cards)), self.card_in_focus + v_change)
    
    def selectCard(self):
        if self.state == P1SELECT:
            self.selected_card = self.current_hand.cards[self.card_in_focus]
            self.changeState()
    
    def cancelSelection(self):
        if self.state == P1PLAY:
            self.changeState(PREVIOUS)
    
    def playCard(self):
        if self.state == P1PLAY or self.state == P2PLAY:
            if not self.isOpeningBids and len(self.current_hand.parent.cards):
                draw = 1
            else:
                draw = 0
            
            if self.selected_card.value <= 10 and self.isLegal():#Number card
                self.current_hand.remove(self.selected_card, self.tracks[self.track_in_focus], draw=draw)
                self.changeState()
                
            elif self.selected_card.value == 11 and self.isLegal():#Jack
                self.current_hand.remove(self.selected_card, draw=draw)
                self.tracks[self.track_in_focus].remove(self.card_in_focus)
                self.changeState()
                
            elif (self.selected_card.value == 12 or self.selected_card.value == 13) and self.isLegal():#King or Queen
                self.current_hand.remove(self.selected_card, self.tracks[self.track_in_focus], self.card_in_focus, draw=draw)
                self.changeState()
                
            elif self.selected_card.value == 14 and self.isLegal():#Joker
                self.current_hand.remove(self.selected_card, self.tracks[self.track_in_focus], self.card_in_focus, draw=draw)
                value = self.tracks[self.track_in_focus].cards[self.card_in_focus][0].value
                suit = self.tracks[self.track_in_focus].cards[self.card_in_focus][0].suit
                for i in range(6):
                    kill_list = []
                    for ii in range(len(self.tracks[i].cards)):
                        if self.tracks[i].cards[ii][0].value == value or self.tracks[i].cards[ii][0].suit == suit:
                            if i == self.track_in_focus and ii == self.card_in_focus:
                                continue
                            kill_list.append(ii)
                    
                    kill_list.reverse()
                    for iii in range(len(kill_list)):
                        self.tracks[i].remove(kill_list[iii])
                
                self.changeState()
            
            if self.isOpeningBids:
                self.isOpeningBids = False
                for i in range(6):
                    if len(self.tracks[i].cards) < 1:
                        self.isOpeningBids = True
    
    def discardCard(self):
        if len(self.current_hand.parent.cards):
            draw = 1
        else:
            draw = 0
        self.current_hand.remove(self.current_hand.cards[self.card_in_focus], draw=draw)
        if not self.isOpeningBids:
            if self.state == P1SELECT or self.state == P1PLAY:
                self.changeState(P2PLAY)
            elif self.state == P2PLAY:
                self.changeState(P1SELECT)
    
    def discardTrack(self):
        if not self.isOpeningBids and len(self.tracks[self.track_in_focus].cards) > 0:
            if (self.state == P1PLAY and self.track_in_focus < 3) or (self.state == P2PLAY and self.track_in_focus >= 3):
                self.tracks[self.track_in_focus].remove()
                self.changeState()
    
    def isLegal(self):
        if self.state == P1SELECT:
            return True
            
        elif self.state == P1PLAY or self.state == P2PLAY:
            if self.isOpeningBids and len(self.tracks[self.track_in_focus].cards) > 0:
                return False
            
            elif self.selected_card.value <= 10:
                if len(self.tracks[self.track_in_focus].cards):
                    if self.selected_card.value == self.tracks[self.track_in_focus].cards[-1][0].value:
                        return False
                    
                    if self.tracks[self.track_in_focus].direction == 0 or (self.selected_card.value < self.tracks[self.track_in_focus].cards[-1][0].value and self.tracks[self.track_in_focus].direction == -1) or (self.selected_card.value > self.tracks[self.track_in_focus].cards[-1][0].value and self.tracks[self.track_in_focus].direction == 1) or (self.selected_card.suit == self.tracks[self.track_in_focus].cards[-1][0].suit):
                        return True
                    else:
                        return False
                else:
                    return True
            
            elif self.selected_card.value > 10:
                if len(self.tracks[self.track_in_focus].cards):
                    return True
                else:
                    return False
            
        else:
            return False
    
    def changeState(self, new_state=NEXT):
        if new_state == P1SELECT or (new_state == NEXT and self.state == P2PLAY) or (new_state == PREVIOUS and self.state == P1PLAY):
            self.card_in_focus = 0
            self.track_in_focus = 0
            self.current_hand = self.p1_hand
            self.state = P1SELECT
        elif new_state == P1PLAY or (new_state == NEXT and self.state == P1SELECT) or (new_state == PREVIOUS and self.state == P2PLAY):
            self.card_in_focus = 0
            self.track_in_focus = 0
            self.current_hand = self.p1_hand
            self.state = P1PLAY
        elif new_state == P2PLAY or (new_state == NEXT and self.state == P1PLAY) or (new_state == PREVIOUS and self.state == P1SELECT):
            self.current_hand = self.p2_hand
            self.state = P2PLAY
            if not self.getWinner():
                self.ai.makePlay(self.ai.getEndNode())
        elif new_state == GAMEOVER:
            self.state = GAMEOVER
    
    def getWinner(self):
        won = 0
        p1_score = 0
        p2_score = 0
        
        if (self.tracks[0].total >= 21 and self.tracks[0].total <= 26) or (self.tracks[3].total >= 21 and self.tracks[3].total <= 26):
            if (self.tracks[0].total > self.tracks[3].total or self.tracks[3].total > 26) and self.tracks[0].total <= 26:
                won += 1
                p1_score += 1
            elif (self.tracks[3].total > self.tracks[0].total or self.tracks[0].total > 26) and self.tracks[3].total <= 26:
                won += 1
                p2_score += 1
            
        if (self.tracks[1].total >= 21 and self.tracks[1].total <= 26) or (self.tracks[4].total >= 21 and self.tracks[4].total <= 26):
            if (self.tracks[1].total > self.tracks[4].total or self.tracks[4].total > 26) and self.tracks[1].total <= 26:
                won += 1
                p1_score += 1
            elif (self.tracks[4].total > self.tracks[1].total or self.tracks[1].total > 26) and self.tracks[4].total <= 26:
                won += 1
                p2_score += 1
        
        if (self.tracks[2].total >= 21 and self.tracks[2].total <= 26) or (self.tracks[5].total >= 21 and self.tracks[5].total <= 26):
            if (self.tracks[2].total > self.tracks[5].total or self.tracks[5].total > 26) and self.tracks[2].total <= 26:
                won += 1
                p1_score += 1
            elif (self.tracks[5].total > self.tracks[2].total or self.tracks[2].total > 26) and self.tracks[5].total <= 26:
                won += 1
                p2_score += 1
        
        if won == 3 and p1_score > p2_score:
            return 1
        elif won == 3 and p2_score > p1_score:
            return 2
        else: return 0
    
def wrap(start, stop, number):
    while(number < start or number >= stop):
        if number < start: number += (stop-start)
        elif number >= stop: number -= (stop-start)
    
    return number

if __name__ == '__main__':
    app = Main()
    app.mainLoop()