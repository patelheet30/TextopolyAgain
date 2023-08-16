from Models.Player import Player
from Utils.properties import get_colors, colour_sizes


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


class Street(Property):

    def __init__(self, name: str, price: int, property_type: str, color: str, improvement_lvl: int = 0,
                 improvement_price: int = 0, mortgaged: bool = False, rent_levels: dict[int, int] = None,
                 owner: Player = None):
        super().__init__(name, property_type)
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


class Railroad(Property):

    def __init__(self, name: str, property_type: str, price: int, improvement_lvl: int = 0, mortgaged: bool = False,
                 rent_levels: dict[int, int] = None, owner=None):
        super().__init__(name, property_type)
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

    def buy(self, answer: str, player: Player):
        if answer == "yes":
            player.remove_balance(self._price)
            self.owner = player
            player.properties.append(self)
            self.update_improvement_level()
            return "You now own this property."
        else:
            return "Going for auction..."

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


class Utility(Property):

    def __init__(self, name: str, property_type: str, price: int, improvement_lvl: int = 0, mortgaged: bool = False,
                 owner: Player = None):
        super().__init__(name, property_type)
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

    def buy(self, answer: str, player: Player):
        if answer == "yes":
            player.remove_balance(self._price)
            self.owner = player
            player.properties.append(self)
            return "You now own this property."
        else:
            return "Going for auction..."

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

    def pay_tax(self, player):
        player.remove_balance(self._tax)


class ComChest(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)


class Chance(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)


class Corner(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)
