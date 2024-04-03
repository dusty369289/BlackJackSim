import random


class Settings:
    def __init__(self):
        # Print All Logs
        self.verbose = False
        # Export data to CSV
        self.csvmode = False
        # Enable 3/2 Blackjack Payout for player
        self.blackjackpayout = True
        self.betsize = 10
        self.maxturns = 100000
        self.shuffleseed = random.randint(0, 1000000)