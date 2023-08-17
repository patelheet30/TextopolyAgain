from Models.Player import Player
from Utils.properties import get_colors, colour_sizes

import random


class Property:

    def __init__(self, name: str, property_type: str):
        self._name = name
        self._property_type = property_type

    @property
    def name(self):
        return self._name

    @property
    def property_type(self):
        return self.__class__.__name__


class Ownable(Property):

    def __init__(self, name: str, property_type: str, price: int, owner: Player = None,):
        super().__init__(name, property_type)
        self._price = price
        self.owner = owner

    def buy_property(self, player, players):
        if player.balance < self._price:
            return "You don't have enough money to buy this property."
        else:
            answer = input(f"Do you want to buy this property for ${self._price}? (yes/no): ")
            if answer == "yes":
                return self.buy(player)
            else:
                return self.auction(players)

    def buy(self, player):
        player.remove_balance(self._price)
        self.owner = player
        player.properties.append(self)
        return "You now own this property."

    def auction(self, players):
        highest_bid = 0
        highest_bidder = None
        players_left = []

        for _ in players:
            want_to_buy = input(f"Player {_.name}, do you want to participate in this auction? (yes/no): ")
            if want_to_buy == "yes":
                players_left.append(_)
            if want_to_buy == "no":
                continue
        if len(players_left) == 0:
            return "Nobody wanted to buy this property."
        for _ in players_left:
            print(f"Player {_.name} has {_.balance} balance.")
            while True:
                try:
                    bid = int(input(f"Player {_.name}, enter your bid: "))
                    if bid > _.balance:
                        raise ValueError
                    break
                except ValueError:
                    print("Enter a valid number.")
            if bid > highest_bid:
                highest_bid = bid
                highest_bidder = _

        highest_bidder.remove_balance(highest_bid)
        highest_bidder.properties.append(self)
        self.owner = highest_bidder
        return f"Player {highest_bidder.name} won the auction with {highest_bid} bid."


class Street(Ownable):

    def __init__(
            self, name: str, price: int, property_type: str, color: str, improvement_lvl: int = 0,
            improvement_price: int = 0, mortgaged: bool = False, rent_levels: dict[int, int] = None,
            owner: Player = None
            ):
        super().__init__(name, property_type, price)
        self._price = price
        self._color = color
        self.improvement_lvl = improvement_lvl
        self._improvement_price = improvement_price
        self.mortgaged = mortgaged
        self._rent_levels = rent_levels
        self.owner = owner

    @property
    def price(self):
        return self._price

    @property
    def color(self):
        return self._color

    @property
    def improvement_price(self):
        return self._improvement_price

    @property
    def rent_levels(self):
        return self._rent_levels

    def owner(self):
        return self.owner

    def is_mortgaged(self):
        return self.mortgaged

    def can_you_build_houses(self):
        player_colors = get_colors(self.owner)
        if self.color in player_colors:
            if player_colors[self.color] == colour_sizes[self.color]:
                return True
        return False

    def build_house(self, player: Player):
        if self.can_you_build_houses():
            if player.balance >= self.improvement_price:
                player.remove_balance(self.improvement_price)
                self.improvement_lvl += 1
                return "You've built a house."
            else:
                return "You don't have enough money to build a house."
        else:
            return "You don't have all the properties of this color."

    def remove_house(self, player: Player):
        if self.improvement_lvl > 0:
            self.improvement_lvl -= 1
            player.add_balance(self.improvement_price * 0.5)
            return "You've removed a house."
        else:
            return "You don't have any houses on this property."

    def sell(self, player: Player):
        if self.improvement_lvl == 0:
            player.add_balance(self._price * 0.5)
            self.owner = None
            player.properties.remove(self)
            return "You've sold this property."
        else:
            return "You can't sell this property because it has houses on it."

    def mortgage(self):
        if self.mortgaged:
            return False
        if self.improvement_lvl > 0:
            return False
        self.mortgaged = True
        self.owner.add_balance(self._price * 0.5)
        return True

    def unmortgage(self):
        if not self.mortgaged:
            return False
        self.mortgaged = False
        self.owner.remove_balance(self._price * 0.6)
        return True


class Railroad(Ownable):

    def __init__(
            self, name: str, property_type: str, price: int, improvement_lvl: int = 0, mortgaged: bool = False,
            rent_levels: dict[int, int] = None, owner=None
            ):
        super().__init__(name, property_type, price)
        self._price = price
        self._rent_levels = rent_levels
        self.improvement_lvl = improvement_lvl
        self.mortgaged = mortgaged
        self.owner = owner

    @property
    def price(self):
        return self._price

    @property
    def rent_levels(self):
        return self._rent_levels

    def owner(self):
        return self.owner

    def is_mortgaged(self):
        return self.mortgaged

    def update_improvement_level(self):
        owner_properties = self.owner.properties
        railroad_count = 0
        for _ in owner_properties:
            if isinstance(_, Railroad):
                railroad_count += 1
        self.improvement_lvl += railroad_count - 1
        for _ in owner_properties:
            if isinstance(_, Railroad):
                _.improvement_lvl = self.improvement_lvl

    def mortgage(self):
        self.mortgaged = True
        self.owner.add_balance(self._price * 0.5)
        return True

    def unmortgage(self):
        if not self.mortgaged:
            return False
        self.mortgaged = False
        self.owner.remove_balance(self._price * 0.6)
        return True


class Utility(Ownable):

    def __init__(
            self, name: str, property_type: str, price: int, improvement_lvl: int = 0, mortgaged: bool = False,
            owner: Player = None
            ):
        super().__init__(name, property_type, price)
        self._price = price
        self.improvement_lvl = improvement_lvl
        self.mortgaged = mortgaged
        self.owner = owner

    @property
    def price(self):
        return self._price

    def owner(self):
        return self.owner

    def is_mortgaged(self):
        return self.mortgaged

    def mortgage(self):
        self.mortgaged = True
        self.owner.add_balance(self._price * 0.5)
        return True

    def unmortgage(self):
        if not self.mortgaged:
            return False
        self.mortgaged = False
        self.owner.remove_balance(self._price * 0.6)
        return True


class Tax(Property):

    def __init__(self, tax, name: str, property_type: str):
        super().__init__(name, property_type)
        self._tax = tax

    @property
    def tax(self):
        return self._tax

    def pay_tax(self, player):
        player.remove_balance(self._tax)


class ComChest(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)
        self._info_dict = None

    @property
    def info_dict(self):
        return self._info_dict

    def set_dict(self, info_dict):
        self._info_dict = info_dict
        return self._info_dict

    def draw_card(self):
        key = random.choice(list(self._info_dict.keys()))
        return self._info_dict[key]

    def perform_action(self, player: Player, squares: dict[int, Property]):
        drawn_card = self.draw_card()
        print(drawn_card["name"])

        if drawn_card["type"] == "balanceadd":
            player.add_balance(drawn_card["value"])
            return f"You've gained ${drawn_card['value']}."

        if drawn_card["type"] == "balanceremove":
            player.remove_balance(drawn_card["value"])
            return f"You've lost ${drawn_card['value']}."

        if drawn_card["type"] == "go":
            player.change_location(squares[0])
            player.add_balance(200)
            return "You've moved to Go and gained $200."

        if drawn_card["type"] == "GOOJF":
            player.goojf_cards += 1
            return "You've gained a Get Out Of Jail Free card."

        if drawn_card["type"] == "jail":
            player.change_location(squares[10])
            player.in_jail = True
            player.jail_turns = 0
            player.is_going_jail = True
            return "You've been sent to jail."


class Chance(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)
        self._info_dict = None

    def set_dict(self, info_dict):
        self._info_dict = info_dict
        return self._info_dict

    def draw_card(self):
        key = random.choice(list(self._info_dict.keys()))
        return self._info_dict[key]

    def perform_action(self, player: Player, squares: dict[int, Property], players: list[Player]):
        drawn_card = self.draw_card()
        print(drawn_card["name"])

        if drawn_card["type"] == "balanceadd":
            player.add_balance(drawn_card["value"])
            return f"You've gained ${drawn_card['value']}."

        if drawn_card["type"] == "balanceremove":
            player.remove_balance(drawn_card["value"])
            return f"You've lost ${drawn_card['value']}."

        if drawn_card["type"] == "moveremove":
            player.change_location(squares[player.location_number - drawn_card["value"]])
            player_location = player.location
            if player_location in [Street, Railroad, Utility]:
                if player_location.owner is not None:
                    if player_location.is_mortgaged():
                        return f"You've moved back {drawn_card['value']} spaces to {player.location.name}."
                    else:
                        player.remove_balance(player_location.rent_levels[player_location.improvement_lvl])
                        player_location.owner.add_balance(player_location.rent_levels[player_location.improvement_lvl])
                        return f"You've moved back {drawn_card['value']} spaces to {player.location.name} and paid "
                else:
                    print(player.location.buy_property(player, players))

        if drawn_card["type"] == "jail":
            player.change_location(squares[10])
            player.in_jail = True
            player.jail_turns = 0
            player.is_going_jail = True
            return "You've been sent to jail."

        if drawn_card["type"] == "GOOJF":
            player.goojf_cards += 1
            return "You've gained a Get Out Of Jail Free card."

        if drawn_card["type"] == "go":
            player.change_location(squares[0])
            player.add_balance(200)
            return "You've moved to Go and gained $200."

        if drawn_card["type"] == "set_loc_property":
            if player.location_number > drawn_card["value"]:
                player.add_balance(200)
                player.change_location(squares[drawn_card["value"]])
                player_location = player.location
                if player_location in [Street, Railroad, Utility]:
                    if player_location.owner is not None:
                        if player_location.is_mortgaged():
                            return f"You've moved back {drawn_card['value']} spaces to {player.location.name}."
                        else:
                            player.remove_balance(player_location.rent_levels[player_location.improvement_lvl])
                            player_location.owner.add_balance(
                                    player_location.rent_levels[player_location.improvement_lvl]
                                    )
                            return f"You've moved back {drawn_card['value']} spaces to {player.location.name} and paid "
                    else:
                        print(player.location.buy_property(player, players))
                return f"You've moved to {player.location.name} and gained $200."
            else:
                player.change_location(squares[drawn_card["value"]])
                player_location = player.location
                if player_location in [Street, Railroad, Utility]:
                    if player_location.owner is not None:
                        if player_location.is_mortgaged():
                            return f"You've moved back {drawn_card['value']} spaces to {player.location.name}."
                        else:
                            player.remove_balance(player_location.rent_levels[player_location.improvement_lvl])
                            player_location.owner.add_balance(
                                    player_location.rent_levels[player_location.improvement_lvl]
                                    )
                            return f"You've moved back {drawn_card['value']} spaces to {player.location.name} and paid "
                    else:
                        print(player.location.buy_property(player, players))
                return f"You've moved to {player.location.name}."



class Corner(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)
