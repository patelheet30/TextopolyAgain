from Models.Player import Player
from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner
from Utils.properties import get_player_properties_names, check_type, get_player_properties, get_colors, build_house, \
    remove_house, sell_property, mortgage, unmortgage
from Utils.moving import check_movement

from random import randint


class Game:

    def __init__(
            self,
            players: list[Player],
            squares: dict[int, Street | Tax | Utility | Railroad | ComChest | Chance | Corner]
            ):
        self._rolled_dice = None
        self.players = players
        self.squares = squares

    def move_player(
            self,
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

            player.previous_dice_role = rolled_dice
            if player.double_roll_count == 3:
                player.change_location(self.squares[10])
                player.in_jail = True
                player.jail_turns = 0
                player.double_roll_count = 0
                return player.location.name

            if not player.in_jail:
                player.change_location(self.squares[ploc_in_squares])
                if player.location == self.squares[29]:
                    player.location = self.squares[10]
                    player.in_jail = True
                    player.jail_turns = 0
                return player.location.name
            else:
                self.jail_handler(player, rolled_dice)

    def jail_handler(self, player, dice_roll):
        if player.jail_turns == 3:
            player.remove_balance(50)
            player.in_jail = False
            player.jail_turns = 0
            self.move_player(player, dice_roll)
        else:
            print("""
                You are in jail. What would you like to do:
                1. Pay $50 to get out of jail
                2. Roll dice
                3. Use a get out of jail free card
            """)
            choices = int(input("Enter your choice: "))
            if choices == 1:
                player.remove_balance(50)
                player.in_jail = False
                player.jail_turns = 0
                self.move_player(player, dice_roll)
            if choices == 2:
                if dice_roll[0] == dice_roll[1]:
                    player.in_jail = False
                    player.jail_turns = 0
                    self.move_player(player, dice_roll)
                else:
                    player.jail_turns += 1

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
        11. Trade # Not Done
        12. View other players properties # Not Done
        11. Continue # Done

        Add to the game:
        1. Chance
        2. Community Chest
        3. View other players properties
        4. Trade
        5. A GUI to see information cleanly
        """
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
                        choices = int(input(f"Enter your choice (Player {player.name}): "))
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
                    for _ in player.properties:
                        _.owner = None
                        _.improvement_lvl = 0
                        _.mortgaged = False
                    self.players.remove(player)

                if len(self.players) == 1:
                    print(f"Player {self.players[0].name} won the game.")
                    return

    def move_the_player(self, player):
        double_roll = True
        while double_roll:
            self._rolled_dice = (randint(1, 6), randint(1, 6))
            double_roll = self._rolled_dice[0] == self._rolled_dice[1]
            if double_roll:
                player.double_roll_count += 1
            else:
                player.double_roll_count = 0
            self.move_player(player, self._rolled_dice)
            location: Street | Utility | Railroad | Tax = player.location
            check_type(location)

            if check_type(location) == Tax:
                location.pay_tax(player)
            movement = check_movement(player, location, self._rolled_dice, self.players)
            if movement is not None:
                print(movement)
