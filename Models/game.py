from Models.player import Player
from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner
from Utils.get_player_properties import get_player_properties_names
from Utils.buying import buying_properties

from random import randint


class Game:

    def __init__(self,
                 players: list[Player],
                 squares: dict[int, Street | Tax | Utility | Railroad | ComChest | Chance | Corner]
                 ):
        self._rolled_dice = None
        self.players = players
        self.squares = squares

    def move_player(self,
                    player: Player,
                    rolled_dice: tuple[int, int]
                    ):
        if player in self.players:
            player_location = player.location
            ploc_in_squares = [key for key in self.squares if self.squares[key] == player_location][0]
            move_points = rolled_dice[0] + rolled_dice[1]
            if ploc_in_squares + move_points > 39:
                ploc_in_squares += (39 - ploc_in_squares)
                ploc_in_squares = (ploc_in_squares + move_points) % 39
            else:
                ploc_in_squares += move_points

            player.change_location(self.squares[ploc_in_squares])
            return player.location.name

    def start(self):
        while True:
            for player in self.players:
                input("Enter to continue...")

                self._rolled_dice = (randint(1, 6), randint(1, 6))
                self.move_player(player, self._rolled_dice)
                location: Street | Utility | Railroad = player.location

                print(f"You are player: {player.name} and you currently have {player.balance} and own {get_player_properties_names(player)}")
                print(buying_properties(player, location))

                if player.balance < 0:
                    print("You are bankrupt.")
                    self.players.remove(player)

                if len(self.players) == 1:
                    print(f"Player {self.players[0].name} won the game.")
                    return
