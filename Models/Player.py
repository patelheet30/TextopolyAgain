class Player:

    def __init__(
            self,
            name: int,
            location,
            balance: int,
            properties: list | None,
    ):
        self._name = name
        self.location = location
        self.balance = balance
        self.properties = properties
        self.in_jail = False
        self.jail_turns = 0
        self.previous_dice_role = None
        self.double_roll_count = 0


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

    def turns_in_jail(self):
        return self.jail_turns

    def add_turn_in_jail(self):
        self.jail_turns += 1
        return self.jail_turns

    def put_in_jail(self):
        self.in_jail = True
        return self.in_jail

    def get_out_jail(self):
        self.in_jail = False
        return self.in_jail
