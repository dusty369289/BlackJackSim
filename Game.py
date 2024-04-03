import os
import random
from ExternalTools import vprint
from Settings import Settings
class Game:
    def __init__(self,player, dealer):
        self.curturn = 0
        self.player = player
        self.dealer = dealer
        self.settings = Settings()
        self.deck = []
        self.shuffleseed = self.settings.shuffleseed
        self.newdeck()
        self.shuffledeck()
        vprint("New Game Created. Deck Initialized and shuffled:\n"+str(self.deck), self.settings.verbose)

    def newdeck(self):
        self.deck=[]
        numbers = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        suits = ["♠","♥","♦","♣"]
        for suit in suits:
            for num in numbers:
                self.deck.append(num + suit)

    def shuffledeck(self):
        random.Random(self.shuffleseed).shuffle(self.deck)
        self.shuffleseed += 1

    def getdeck(self):
        return self.deck
    def winner_loser_balanceupdate(self, winner, loser, transferamount):
        winner.add_balance(transferamount)
        loser.sub_balance(transferamount)

    def dealcard(self):
        if not self.deck:
            self.newdeck()
            self.shuffledeck()
            vprint("Deck empty, new deck created and shuffled:\n"+str(self.deck), self.settings.verbose)
        return self.deck.pop()

    def run(self):
        gamewinner = None
        vprint("Player Balance: " + str(self.player.get_balance()), self.settings.verbose)
        vprint("Dealer Balance: " + str(self.dealer.get_balance()), self.settings.verbose)
        if self.settings.csvmode:
            # reset file
            try:
                os.remove("BlackJackRun.txt")
            except OSError:
                pass
            f = open("BlackJackRun.txt", "a")
            f.write("TurnNumber,PlayerBalance\n")
        while self.curturn < self.settings.maxturns:
            if self.settings.csvmode:
                f.write(str(self.curturn)+","+str(self.player.get_balance())+"\n")
            winner = None
            loser = None
            self.player.set_hand([self.dealcard(), self.dealcard()])
            vprint("Dealt player hand: "+str(self.player.get_hand()), self.settings.verbose)
            self.dealer.set_hand([self.dealcard(), self.dealcard()])
            vprint("Dealt dealer hand: "+str(self.dealer.get_hand()), self.settings.verbose)
            # Single Turn Here (player and dealer)
            vprint("Player Turn", self.settings.verbose)
            playerresult = self.player.play_hand(self.dealer.get_hand()[0], self, self.settings.verbose, "Player")
            # Only Bother playing dealer is player didnt bust
            if playerresult <= 21:
                vprint("Dealer Turn", self.settings.verbose)
                dealerresult = self.dealer.play_hand(self.player.get_hand()[0], self, self.settings.verbose, "Dealer")
            else:
                dealerresult = 0
            # Check for Blackjack
            if self.player.hand_is_blackjack(self.player.get_hand()) and self.settings.blackjackpayout:
                # Player has blackjack
                vprint("Player has Blackjack", self.settings.verbose)
                # Check for Dealer Blackjack
                if self.dealer.hand_is_blackjack(self.dealer.get_hand()):
                    vprint("Dealer has Blackjack, Push", self.settings.verbose)
                else:
                    vprint("Player wins "+str(self.settings.betsize*1.5)+" chips     BLACKJACK!!!!", self.settings.verbose)
                    winner = self.player
                    loser = self.dealer
                    self.winner_loser_balanceupdate(winner, loser, self.settings.betsize*1.5)
            else:
                # No Blackjack from player, calculate normal scores
                # Check for Bust
                if playerresult > 21:
                    vprint("Player Busts, Dealer wins "+str(self.settings.betsize)+" chips", self.settings.verbose)
                    winner = self.dealer
                    loser = self.player
                    self.winner_loser_balanceupdate(winner, loser, self.settings.betsize)
                else:
                    if dealerresult > 21:
                        vprint("Dealer Busts, Player wins "+str(self.settings.betsize)+" chips", self.settings.verbose)
                        winner = self.player
                        loser = self.dealer
                        self.winner_loser_balanceupdate(winner, loser, self.settings.betsize)
                if not winner:
                    # If nobody has bust or blackjacked, compare hands
                    if playerresult > dealerresult:
                        vprint("Player wins "+str(self.settings.betsize)+" chips", self.settings.verbose)
                        winner = self.player
                        loser = self.dealer
                        self.winner_loser_balanceupdate(winner, loser, self.settings.betsize)
                    elif dealerresult > playerresult:
                        vprint("Dealer wins "+str(self.settings.betsize)+" chips", self.settings.verbose)
                        winner = self.dealer
                        loser = self.player
                        self.winner_loser_balanceupdate(winner, loser, self.settings.betsize)
                    else:
                        vprint("Push, no chips exchanged", self.settings.verbose)
            vprint("Player Balance: "+str(self.player.get_balance()), self.settings.verbose)
            vprint("Dealer Balance: "+str(self.dealer.get_balance()), self.settings.verbose)
            if self.player.get_balance() <= self.settings.betsize*1.5:
                vprint("Player has run out of chips, Dealer wins!", self.settings.verbose)
                gamewinner = "Dealer"
                break
            if self.dealer.get_balance() <= self.settings.betsize*1.5:
                vprint("Dealer has run out of chips, Player wins!", self.settings.verbose)
                gamewinner = "Player"
                break
            self.curturn += 1
        if not self.settings.verbose:
            print("Player Balance: "+str(self.player.get_balance()))
            print("Dealer Balance: "+str(self.dealer.get_balance()))
        print("Total Rounds: "+str(self.curturn))
        print("THEORETICAL RTP: "+str(1-(self.player.get_balance()/(self.settings.betsize*self.curturn))))
        if self.settings.csvmode:
            f.close()
        if gamewinner:
            return gamewinner
        else:
            return -1

