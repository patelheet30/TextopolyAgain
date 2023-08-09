from Models.player import Player
from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner
from Utils.properties import get_player_properties_names, check_type, get_player_properties, get_colors, build_house, \
    remove_house, sell_property, mortgage, unmortgage
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
        """
        Choices:
        1. Roll dice # Done
        2. View your properties # Done - Clean Up
        3. View your balance # Done
        4. View your location # Done
        5. Build houses/hotels # Done
        6. Sell houses/hotel # Done
        7. Mortgage properties # Done
        8. Unmortgage properties # Done
        9. Sell properties # Done
        10. Color Group Information # Done
        11. Continue # Done

        Add to the game:
        1. Jail - Important
        2. Chance
        3. Community Chest
        4. View other players properties
        5. Trade
        6. Auction
        7. A GUI to see information cleanly
        8. A rework to moving and renting. - Important
        """
        while True:
            for player in self.players:
                input("Enter to continue...")
                print(
                    """What would you like to do:
                     1. Roll dice # Done
                     2. View your properties
                     3. View your balance
                     4. View your location
                     5. Build houses/hotels
                     6. Sell houses/hotel
                     7. Mortgage properties
                     8. Unmortgage properties
                     9. Sell properties
                     10. Color Group Information
                     11. Continue
                     """
                )
                move_on = False
                rolled_dice = False
                while not move_on:
                    try:
                        choices = int(input(f"Enter your choice ({player.name}): "))
                    except ValueError:
                        choices = 2
                    if choices == 1:
                        if rolled_dice:
                            move_on = True
                            print("You have already rolled the dice.")
                        else:
                            rolled_dice = True
                            self.move_the_player(player)
                    elif choices == 2:
                        print(get_player_properties_names(player))
                        print(get_player_properties(player))
                    elif choices == 3:
                        print(player.balance)
                    elif choices == 4:
                        print(player.location.name)
                    elif choices == 5:
                        print(build_house(player))
                    elif choices == 6:
                        print(remove_house(player))
                    elif choices == 7:
                        print(mortgage(player))
                    elif choices == 8:
                        print(unmortgage(player))
                    elif choices == 9:
                        print(sell_property(player))
                    elif choices == 10:
                        print(get_colors(player))
                    elif choices == 11:
                        if rolled_dice:
                            move_on = True
                            print("Moving on...")
                        else:
                            print("You have to roll the dice first.")

                if player.balance < 0:
                    print("You are bankrupt.")
                    self.players.remove(player)

                if len(self.players) == 1:
                    print(f"Player {self.players[0].name} won the game.")
                    return

    def move_the_player(self, player):
        self._rolled_dice = (randint(1, 6), randint(1, 6))
        self.move_player(player, self._rolled_dice)
        location: Street | Utility | Railroad | Tax = player.location
        check_type(location)

        if check_type(location) == Tax:
            location.pay_tax(player)
        complete_roll_size = self._rolled_dice[0] + self._rolled_dice[1]
        print(buying_properties(player, location, complete_roll_size))
