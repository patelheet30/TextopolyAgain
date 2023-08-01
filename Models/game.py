from Models.player import Player
from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner
from Utils.properties import get_player_properties_names, check_type, pay_tax
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
                print(
                    """What would you like to do:
                     1. Roll dice
                     2. View your properties
                     3. View your balance
                     4. View your location
                     5. Build houses/hotels
                     6. Sell houses/hotels
                     7. Mortgage properties
                     8. Unmortgage properties
                     """
                )
                move_on = False
                while not move_on:
                    choices = int(input("Enter your choice: "))
                    if choices == 1:
                        self.move_the_player(player)
                        move_on = True
                    elif choices == 2:
                        print(get_player_properties_names(player))
                    elif choices == 3:
                        print(player.balance)
                    elif choices == 4:
                        print(player.location.name)

                if player.balance < 0:
                    print("You are bankrupt.")
                    self.players.remove(player)

                if len(self.players) == 1:
                    print(f"Player {self.players[0].name} won the game.")
                    return

    def move_the_player(self, player):
        self._rolled_dice = (randint(1, 6), randint(1, 6))
        self.move_player(player, self._rolled_dice)
        location: Street | Utility | Railroad = player.location
        check_type(location)

        if check_type(location) == Tax:
            pay_tax(player, location)

        print(buying_properties(player, location))
