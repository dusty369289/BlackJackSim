# Player, Dealer or -1 for timeout
from Game import Game
from Player import Player
idealwinner = "Player"
GameResult = None
while GameResult != idealwinner:
    player = Player(1000, "PLAYER")
    dealer = Player(10000, "DEALER")
    newgame = Game(player, dealer)
    GameResult = newgame.run()
print("seed: "+str(newgame.settings.shuffleseed))
