def buying_properties(player, location):
    correct_type = ("Street", "Utility", "Railroad")
    if location.property_type in correct_type:
        if location.owner == "none":
            print(f"The location you've landed is {location.name} and is currently unowned")
            print(f"Do you want to buy {location.name} for {location.price}?")
            answer = input("Enter yes or no: ")
            if answer.lower() == "yes":
                location.buy(answer, player)
                return "You've bought the location. Congrats."
            else:
                return "You have not bought the location."
        else:
            rent_price = determineRent(location, player)
            player.remove_balance(rent_price)
            if rent_price == 0:
                return f"You own the location {location.name} and you don't have to pay rent."
            else:
                return f"The location is owned by {location.owner.name} and you have to pay ${rent_price}"
    else:
        return f"The location is {location.name}"


def determineRent(location, player):
    if player not in location.owner:
        rent_price = location.rent_levels[location.improvement_lvl]
        return rent_price
    return 0
