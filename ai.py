import random

class AI():
    def __init__(self, root):
        self.root = root
        
    def getEndNode(self):
        starting_node = Node(self.getTracks())
        
        #Create list of current bids
        current_bids = []
        for i in range(6):
            bid_total = 0
            for ii in range(len(starting_node.tracks[i])):
                bid_total += starting_node.tracks[i][ii][0]*(2**starting_node.tracks[i][ii][2])
            current_bids.append(bid_total)
        
        low_card = 11
        high_card = 0
        queen = False
        for card in self.root.p2_hand.cards:
            if card.value <= 10:
                if card.value < low_card:
                    low_card = card.value
                if card.value > high_card:
                    high_card = card.value
            elif card.value == 12:
                queen = True
        
        repair = []
        reverse = []
        for i in range(3, 6):
            if current_bids[i] > 26:
                repair.append(i)
            if high_card > 0 and queen:
                if (self.root.tracks[i].direction == 1 and self.root.tracks[i].cards[-1][0].value > high_card) or (self.root.tracks[i].direction == -1 and self.root.tracks[i].cards[-1][0].value < low_card):
                    reverse.append(i)
        
        if len(repair):
            repair_track = random.randrange(len(repair))    
                
        end_node = None
        end_node_difference = 0
        end_node_bids = []
        nodes = self.getNodes()
        print('There are ' + str(len(nodes)) + ' nodes.')
           
        for node in nodes:
            #Create list of bids
            node_bids = []
            difference = 0
            for i in range(6):
                bid_total = 0
                for ii in range(len(node.tracks[i])):
                    bid_total += node.tracks[i][ii][0]*(2**node.tracks[i][ii][2])
                node_bids.append(bid_total)
                
                if (i < 3 and node_bids[i] <= 26) or (i >= 3 and node_bids[i] > 26):
                    difference -= node_bids[i] - current_bids[i]
                else:
                    difference += node_bids[i] - current_bids[i]
                    
            if len(repair):
                if node_bids[repair_track] <= 26:
                    if end_node is not None:
                        if end_node_bids[repair_track] < node_bids[repair_track]:
                            end_node = node
                            end_node_bids = node_bids
                    else:
                        end_node = node
                        end_node_bids = node_bids
            elif len(reverse):
                if node.selected_card is not None:
                    if node.selected_card.value == 12 and node.track_in_focus in reverse and node.card_in_focus == len(starting_node.tracks[node.track_in_focus]):
                        end_node = node
            
            if end_node is None:
                if difference > end_node_difference and (node.track_in_focus < 3 or node_bids[node.track_in_focus] <= 26 or node.selected_card.value == 14):
                    end_node = node
                    end_node_bids = node_bids
                    end_node_difference = difference
        
        if end_node is None:
            end_node = nodes[random.randrange(len(nodes))]
        
        print('End node will add ' + str(end_node_difference))
        return end_node
    
    def makePlay(self, node):
        print('Making play..')
        self.root.selected_card = node.selected_card
        self.root.track_in_focus = node.track_in_focus
        if node.card_in_focus >= 0:
            self.root.card_in_focus = node.card_in_focus
        if node.discard_track:
            print('Discarding track ' + str(node.track_in_focus))
            self.root.discardTrack()
        elif node.discard_card:
            if node.selected_card.value == 11:
                card = 'Jack'
            elif node.selected_card.value == 12:
                card = 'Queen'
            elif node.selected_card.value == 13:
                card = 'King'
            elif node.selected_card.value == 14:
                card = 'Joker'
            else:
                card = str(node.selected_card.value)
            
            print('Discarding ' + card)
            self.root.discardCard()
            if self.root.isOpeningBids:
                self.makePlay(self.getEndNode())
        else:
            if node.selected_card.value == 11:
                card = 'Jack'
            elif node.selected_card.value == 12:
                card = 'Queen'
            elif node.selected_card.value == 13:
                card = 'King'
            elif node.selected_card.value == 14:
                card = 'Joker'
            else:
                card = str(node.selected_card.value)
            
            print('Playing ' + card)
            self.root.playCard()
    
    def getNodes(self):
        tracks = self.getTracks()
        
        nodes = []
        for card in self.root.p2_hand.cards:
            nodes.append(Node(self.getTracks(), selected_card=card, discard_card=True))
            self.root.selected_card = card
            for i in range(6):
                if i >= 3 and len(tracks[i]) and not self.root.isOpeningBids: nodes.append(Node(self.getTracks(), track_in_focus=i, discard_track=True))
                self.root.track_in_focus = i
                if card.value <= 10 and i < 3:
                    continue
                elif card.value <= 10 and i >= 3:
                    if self.root.isLegal():
                        nodes.append(Node(self.getTracks(), card, i))
                else:
                    for ii in range(len(tracks[i])):
                        self.root.card_in_focus = ii
                        if self.root.isLegal():
                            nodes.append(Node(self.getTracks(), card, i, ii))
        
        return nodes
    
    def getTracks(self):
        tracks = []
        for i in range(6):
            tracks.append([])
            for ii in range(len(self.root.tracks[i].cards)):
                tracks[i].append([self.root.tracks[i].cards[ii][0].value, self.root.tracks[i].cards[ii][0].suit, 0])
                for iii in range(len(self.root.tracks[i].cards[ii])):
                    if self.root.tracks[i].cards[ii][iii] == 13:
                        tracks[i][ii][2] += 1
        return tracks
    
class Node():
    def __init__(self, tracks, selected_card=None, track_in_focus=-1, card_in_focus=-1, discard_track=False, discard_card=False):
        self.tracks = tracks
        self.selected_card = selected_card
        self.track_in_focus = track_in_focus
        self.card_in_focus = card_in_focus
        self.discard_track = discard_track
        self.discard_card = discard_card
        
        if selected_card is not None and not discard_card:
            #Number card
            if selected_card.value <= 10:
                self.tracks[self.track_in_focus].append([selected_card.value, selected_card.suit, 0])
                
            #Jack
            elif selected_card.value == 11:
                self.tracks[self.track_in_focus].pop(self.card_in_focus)
            
            #King
            elif selected_card.value == 13:
                self.tracks[self.track_in_focus][self.card_in_focus][2] += 1
            
            #Joker
            elif selected_card.value == 14:
                kill_value = self.tracks[track_in_focus][card_in_focus][0]
                kill_suit = self.tracks[track_in_focus][card_in_focus][1]
                for i in range(6):
                    kill_list = []
                    for ii in range(len(self.tracks[i])):
                        if (i != track_in_focus or ii != card_in_focus) and (self.tracks[i][ii][0] == kill_value or self.tracks[i][ii][1] == kill_suit):
                            kill_list.append(ii)
                            
                    kill_list.reverse()
                    for ii in range(len(kill_list)):
                        self.tracks[i].pop(kill_list[ii])
        
        elif discard_track:
            self.tracks[track_in_focus] = []