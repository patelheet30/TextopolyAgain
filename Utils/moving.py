from Models.Property import *
from Utils.properties import check_type


def check_movement(player, location, completed_roll_size):

    print("You rolled a", completed_roll_size)
    print("You are now on", location.name)
    print("You are on a", location.property_type)

    location_type = check_type(location)

    if location_type in [Street, Utility, Railroad]:
        is_owned = location.owner

        if is_owned:
            if location.is_mortgaged():
                print("This property is mortgaged.")
                return
            if location.owner == player:
                print("This is your property.")
                return
            print("This property is owned by", is_owned.name)
            player.remove_balance((determineRent(location, player, completed_roll_size)))
            print("You paid", determineRent(location, player, completed_roll_size), "to", is_owned.name)
            return
        else:
            print(buy_property(location, player))

    return


def determineRent(location, player, roll_size):
    rent_price = 0
    if location.is_mortgaged():
        return 0
    utility_count = 0
    if player != location.owner:
        if location.property_type == "Utility":
            for _ in location.owner.properties:
                if isinstance(_, Utility):
                    utility_count += 1
            if utility_count == 1:
                rent_price = roll_size * 4
            elif utility_count == 2:
                rent_price = roll_size * 10
            return rent_price
        rent_price = location.rent_levels[location.improvement_lvl]
        return rent_price
    return rent_price


def buy_property(location, player):
    if player.balance < location.price:
        return "You don't have enough money to buy this property."
    else:
        answer = input("Do you want to buy this property? (yes/no): ")
        return location.buy(answer, player)
