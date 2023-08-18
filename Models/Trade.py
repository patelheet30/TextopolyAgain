import Models.Property


class Trade:

    def __init__(self, receiver, sender, all_properties):
        self.all_properties: dict[int, Models.Property.Street | Models.Property.Utility | Models.Property.Railroad] = all_properties
        self.sender = sender
        self.receiver = receiver
        self.properties_offered = []
        self.properties_asked = []
        self.money_offered = 0
        self.money_asked = 0
        self.get_out_of_jail_free_offered = 0
        self.get_out_of_jail_free_asked = 0
        self.accepted = False

    def start(self):
        print(f"{self.receiver.name} is offering a trade to {self.sender.name}")
        self.ask_for_offer()
        if self.money_asked != 0:
            print(f"{self.receiver.name} is asking for ${self.money_asked}")
        if self.get_out_of_jail_free_asked != 0:
            print(f"{self.receiver.name} is asking for {self.get_out_of_jail_free_asked} get out of jail free cards")
        if len(self.properties_asked) != 0:
            print(f"{self.receiver.name} is asking for {[property_asked.name for property_asked in self.properties_asked]} in return")
        self.what_do_you_offer()
        if self.money_offered != 0:
            print(f"{self.sender.name} is asking for ${self.money_offered} in return")
        if self.get_out_of_jail_free_offered != 0:
            print(f"{self.sender.name} is asking for {self.get_out_of_jail_free_offered} get out of jail free cards in return")
        if len(self.properties_offered) != 0:
            print(f"{self.sender.name} is asking for {[property_offered.name for property_offered in self.properties_offered]} in return")
        self.do_you_accept_receiver()
        if self.accepted:
            print(f"{self.receiver.name} has accepted the trade")
            self.do_you_accept_sender()
            if self.accepted:
                print(f"{self.sender.name} has accepted the trade")
                self.transfer_goojf()
                self.transfer_money()
                self.transfer_properties()
            else:
                print(f"{self.sender.name} has declined the trade")


    def ask_for_offer(self):
        what_do_you_want = input(f"Player {self.receiver.name} What do you want? (money/property/get out of jail free card(goojf)): ")
        match what_do_you_want:
            case "money":
                self.money_asked = int(input("How much money do you want? "))
            case "property":
                property_matcher = input("What property do you want? ")
                for _ in self.all_properties:
                    if self.all_properties[_].name == property_matcher:
                        self.properties_asked.append(self.all_properties[_])
                        break
                    else:
                        continue
            case "goojf":
                self.get_out_of_jail_free_asked = int(input("How many get out of jail free cards do you want? "))
            case _:
                print("Invalid input")

    def what_do_you_offer(self):
        what_do_you_offer = input(f"Player {self.sender.name} What do you want in return? (money/property/get out of jail free card(goojf)): ")
        match what_do_you_offer:
            case "money":
                self.money_offered = int(input("How much money do you want in return? "))
            case "property":
                property_matcher = input("What property do you want in return? ")
                for _ in self.all_properties:
                    if self.all_properties[_].name == property_matcher:
                        self.properties_offered.append(self.all_properties[_])
                        break
                    else:
                        continue
            case "goojf":
                self.get_out_of_jail_free_offered = int(input("How many get out of jail free cards do you want in return? "))
            case _:
                print("Invalid input")

    def do_you_accept_receiver(self):
        print(f"Player {self.receiver.name} do you accept this trade?")
        accept = input("Do you accept? (y/n): ")
        if accept == "y":
            self.accepted = True
            if self.receiver.balance < self.money_offered:
                print(f"You don't have enough money to accept this trade")
                self.accepted = False
                return self.accepted
            if self.receiver.goojf_cards < self.get_out_of_jail_free_offered:
                print(f"You don't have enough get out of jail free cards to accept this trade")
                self.accepted = False
                return self.accepted
            for _ in self.properties_offered:
                if _.owner != self.receiver:
                    print(f"You don't own all the properties you're offering")
                    self.accepted = False
                else:
                    self.accepted = True
                    break
            return self.accepted
        else:
            self.accepted = False
        return self.accepted

    def do_you_accept_sender(self):
        print(f"Player {self.sender.name} do you accept this trade?")
        accept = input("Do you accept? (y/n): ")
        if accept == "y":
            self.accepted = True
            if self.sender.balance < self.money_asked:
                print(f"You don't have enough money to accept this trade")
                self.accepted = False
                return self.accepted
            if self.sender.goojf_cards < self.get_out_of_jail_free_asked:
                print(f"You don't have enough get out of jail free cards to accept this trade")
                self.accepted = False
                return self.accepted
            for _ in self.properties_asked:
                if _.owner != self.sender:
                    print(f"You don't own all the properties you're offering")
                    self.accepted = False
                else:
                    self.accepted = True
                    break
            return self.accepted
        else:
            self.accepted = False
        return self.accepted

    def transfer_money(self):
        self.sender.remove_balance(self.money_asked)
        self.receiver.add_balance(self.money_asked)
        self.receiver.remove_balance(self.money_offered)
        self.sender.add_balance(self.money_offered)

    def transfer_goojf(self):
        self.sender.goojf_cards -= self.get_out_of_jail_free_asked
        self.receiver.goojf_cards += self.get_out_of_jail_free_asked
        self.receiver.goojf_cards -= self.get_out_of_jail_free_offered
        self.sender.goojf_cards += self.get_out_of_jail_free_offered

    def transfer_properties(self):
        if len(self.properties_offered) != 0:
            for _ in self.properties_offered:
                _.owner = self.sender
                self.receiver.properties.remove(_)
                self.sender.properties.append(_)
        if len(self.properties_asked) != 0:
            for _ in self.properties_asked:
                _.owner = self.receiver
                self.sender.properties.remove(_)
                self.receiver.properties.append(_)
