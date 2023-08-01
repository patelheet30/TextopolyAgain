from Models.player import Player
from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner
from Utils.get_player_properties import get_player_properties_names

from random import randint


class Game:

    def __init__(self,
                 players: list[Player],
                 squares: dict[int, Street | Tax | Utility | Railroad | ComChest | Chance | Corner]
                 ):
        self._rolled_dice = None
        self._players = players
        self._squares = squares

    @property
    def players(self):
        return self._players

    @property
    def squares(self):
        return self._squares

    def move_player(self,
                    player: Player,
                    rolled_dice: tuple[int, int]
                    ):
        if player in self._players:
            player_location = player.location
            ploc_in_squares = [key for key in self._squares if self._squares[key] == player_location][0]
            move_points = rolled_dice[0] + rolled_dice[1]
            if ploc_in_squares + move_points > 39:
                ploc_in_squares += (39 - ploc_in_squares)
                ploc_in_squares = (ploc_in_squares + move_points) % 39
            else:
                ploc_in_squares += move_points

            player.change_location(self._squares[ploc_in_squares])
            return player.location.name


    def start(self):
        while True:
            for player in self._players:
                input("Enter to continue...")

                self._rolled_dice = (randint(1, 6), randint(1, 6))
                self.move_player(player, self._rolled_dice)
                location: Street | Utility | Railroad = player.location
                correct_type = ("Street", "Utility", "Railroad")
                print(f"You are player: {player.name} and you currently have {player.balance} and own {get_player_properties_names(player)}")
                if location.property_type in correct_type:
                    if location.owner == "none":
                        print(f"The location you've landed is {location.name} and is currently unowned")
                        print(f"Do you want to buy {location.name} for {location.price}?")
                        answer = input("Enter yes or no: ")
                        if answer == "yes":
                            location.buy(answer, player)
                            print("You've bought the location. Congrats.")
                        else:
                            location.buy(answer, player)
                    else:
                        print(f"The location you've landed is {location.name} and is currently owned by {location.owner.name}")
                else:
                    print(f"The location is {location.name}")
