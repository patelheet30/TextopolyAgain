from Models.Property import *
from Utils.properties import buy_property, check_type


def check_movement(player, location, roll_tuple, all_players):

    print("You rolled a", roll_tuple[0], "and a", roll_tuple[1])
    completed_roll_size = roll_tuple[0] + roll_tuple[1]
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
            player.remove_balance((determine_rent(location, player, completed_roll_size)))
            print("You paid", determine_rent(location, player, completed_roll_size), "to", is_owned.name)
            return
        else:
            print(buy_property(location, player, all_players))

    return


def determine_rent(location, player, roll_size):
    if location.is_mortgaged() or player == location.owner:
        return 0

    if location.property_type == "Utility":
        utility_count = sum(isinstance(_, Utility) for _ in location.owner.properties)
        if utility_count == 1:
            return roll_size * 4
        elif utility_count == 2:
            return roll_size * 10

    return location.rent_levels[location.improvement_lvl]
