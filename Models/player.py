class Player:

    def __init__(
            self,
            name: int,
            location,
            balance: int,
            properties: list | None,
            extras: dict[str, str] | None
    ):
        self._name = name
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras


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

    def add_balance(self, value):
        self.balance += value

    def remove_balance(self, value):
        self.balance -= value
