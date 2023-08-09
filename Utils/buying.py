import Models.Property


def buying_properties(player, location, roll_size):
    correct_type = ("Street", "Utility", "Railroad")
    if location.property_type in correct_type:
        if location.owner == "none":
            print(f"The location you've landed is {location.name} - {location.property_type} and is currently unowned")
            print(f"Do you want to buy {location.name} for {location.price}?")
            answer = input("Enter yes or no: ")
            if answer.lower() == "yes":
                location.buy(answer, player)
                return "You've bought the location. Congrats."
            else:
                return "You have not bought the location."
        else:
            rent_price = determineRent(location, player, roll_size)
            player.remove_balance(rent_price)
            if rent_price == 0:
                return f"You own the location {location.name} and you don't have to pay rent."
            else:
                return f"The location is owned by {location.owner.name} and you have to pay ${rent_price}"
    else:
        return f"The location is {location.name}"


def determineRent(location, player, roll_size):
    rent_price = 0
    if location.is_mortgaged():
        return 0
    utility_count = 0
    if player != location.owner:
        if location.property_type == "Utility":
            for _ in location.owner.properties:
                if isinstance(_, Models.Property.Utility):
                    utility_count += 1
            if utility_count == 1:
                rent_price = roll_size * 4
            elif utility_count == 2:
                rent_price = roll_size * 10
            return rent_price
        rent_price = location.rent_levels[location.improvement_lvl]
        return rent_price
    return 0
