class Player:

    def __init__(
            self,
            name: int,
            location,
            balance: int,
            properties: list | None,
            extras: dict[str, int] | None
    ):
        self._name = name
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras
        self.in_jail = False


    @property
    def name(self):
        return self._name

    def location(self):
        return self.location.name

    def change_location(self, value):
        self.location = value
        return self.location

    def balance(self):
        return self.balance

    def properties(self):
        return self.properties

    def extras(self):
        return self.extras

    def in_jail(self):
        return self.in_jail

    def add_balance(self, value):
        self.balance += value

    def remove_balance(self, value):
        self.balance -= value

    def get_out_of_jail(self):
        pass
