from Game import Game
from Player import Player
player = Player(1000, "PLAYER")
dealer = Player(10000000, "DEALER")
newgame = Game(player,dealer)
GameResult = newgame.run()
print("seed: " + str(newgame.settings.shuffleseed))

