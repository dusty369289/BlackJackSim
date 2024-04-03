from PlayerStrategy import decide as playerdecide
from DealerStrategy import decide as dealerdecide
from ExternalTools import vprint
class Player:
    def __init__(self, InitialMoney, StrategyTable):
        self.balance = InitialMoney
        self.strategy = StrategyTable
        self.hand = []

    def get_balance(self):
        return self.balance

    def set_balance(self, new_balance):
        self.balance = new_balance

    def add_balance(self, amount):
        self.balance += amount

    def sub_balance(self, amount):
        self.balance -= amount

    def set_hand(self, new_hand):
        self.hand = new_hand

    def get_hand(self):
        return self.hand

    def hand_is_soft(self, hand):
        temptotal = 0
        containsace = False
        for card in self.hand:
            if card[:-1] in ["J", "Q", "K"]:
                temptotal += 10
            elif card[:-1] == "A":
                containsace = True
                temptotal += 1
            else:
                temptotal += int(card[:-1])
        if not containsace:
            return False
        else:
            if temptotal + 10 <= 21:
                return True
            else:
                return False

    def get_hand_total(self, hand, softhand):
        if softhand:
            # Initialise at 10 because at least 1 ace can be High
            temptotal = 10
            for card in hand:
                if card[:-1] in ["J", "Q", "K"]:
                    temptotal += 10
                elif card[:-1] == "A":
                    temptotal += 1
                else:
                    temptotal += int(card[:-1])
            # Returns between 12 and 21
            return temptotal
        else:
            temptotal = 0
            for card in hand:
                if card[:-1] in ["J", "Q", "K"]:
                    temptotal += 10
                elif card[:-1] == "A":
                    # No aces can be high in hardhand
                    temptotal += 1
                else:
                    temptotal += int(card[:-1])
            # Retruns between 4 and 21
            return temptotal
    def get_printable_total(self, hand):
        softhand = self.hand_is_soft(hand)
        total = self.get_hand_total(hand, softhand)
        if softhand:
            return str(total-10)+"/"+str(total)
        else:
            return str(total)

    def play_hand(self, opponentcard, game, verbose, displayname):
        handterminated = False
        vprint("TURN BEGINS: "+str(self.hand) + "   " + self.get_printable_total(self.hand), verbose)
        while not handterminated:
            softhand = self.hand_is_soft(self.hand)
            handtotal = self.get_hand_total(self.hand, softhand)
            if self.strategy == "PLAYER":
                decision = playerdecide(handtotal, softhand, opponentcard)
            elif self.strategy == "DEALER":
                decision = dealerdecide(handtotal, softhand)
            else:
                print("Invalid Strategy Table: "+self.strategy)
                return
            if decision == "HIT":
                vprint(displayname+" Hits", verbose)
                self.hand.append(game.dealcard())
                vprint(displayname+" Hand: "+str(self.hand)+ "   " + self.get_printable_total(self.hand), verbose)
            elif decision == "STAND":
                handterminated = True
                softhand = self.hand_is_soft(self.hand)
                vprint(displayname+" Stands at "+str(self.get_hand_total(self.hand, softhand)), verbose)
            softhand = self.hand_is_soft(self.hand)
            if self.get_hand_total(self.hand, softhand) > 21:
                handterminated = True
                vprint(displayname+" Busts", verbose)
        softhand = self.hand_is_soft(self.hand)
        return self.get_hand_total(self.hand, softhand)

    def hand_is_blackjack(self, hand):
        if len(hand) == 2:
            # Check for ace in first card
            if hand[0][:-1] == "A":
                # Check for 10 in second card
                if hand[1][:-1] in ["10", "J", "Q", "K"]:
                    return True
            # Check for ace in second card
            if hand[1][:-1] == "A":
                # Check for 10 in first card
                if hand[0][:-1] in ["10", "J", "Q", "K"]:
                    return True
        return False

