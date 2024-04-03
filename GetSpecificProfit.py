from Game import Game
from Player import Player

# Enter the profit you want player to make
idealprofit = 4000
# Player Starting Cash
playercash = 1000
GameResult = None
while GameResult != "Player":
    player = Player(playercash, "PLAYER")
    dealer = Player(idealprofit, "DEALER")
    newgame = Game(player, dealer)
    GameResult = newgame.run()
print("seed: "+str(newgame.settings.shuffleseed))