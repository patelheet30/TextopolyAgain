def buying_properties(player, location):
    correct_type = ("Street", "Utility", "Railroad")
    if location.property_type in correct_type:
        if location.owner == "none":
            print(f"The location you've landed is {location.name} and is currently unowned")
            print(f"Do you want to buy {location.name} for {location.price}?")
            answer = input("Enter yes or no: ")
            if answer == "yes":
                location.buy(answer, player)
                return "You've bought the location. Congrats."
            else:
                return "You have not bought the location."
        else:
            rent_price = determineRent(location)
            player.remove_balance(rent_price)
            return f"The location is owned by {location.owner.name} and you have to pay {rent_price}"
    else:
        return f"The location is {location.name}"


def determineRent(location):
    rent_price = location.rent_levels[location.improvement_lvl]
    return rent_price
