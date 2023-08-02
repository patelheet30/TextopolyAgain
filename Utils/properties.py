def get_player_properties_names(player):
    properties = player.properties
    names = []
    for _ in properties:
        names.append(_.name)

    return names


def check_type(location):
    return type(location)


def get_player_properties(player):
    property_list = []
    for _ in player.properties:
        if _.property_type == "Street":
            property_list.append(f"{_.name} - {_.property_type} - {_.improvement_lvl} Build houses? - {_.can_you_build_houses()}")
        else:
            property_list.append(f"{_.name} - {_.property_type} - {_.improvement_lvl}")

    return property_list


def get_colors(player):
    property_list = {}
    for _ in player.properties:
        if _.property_type == "Street":
            property_list[_.color] = property_list.get(_.color, 0) + 1

    return property_list


def build_house(player):
    where_to_build = input("Where do you want to build a house? ")
    for _ in player.properties:
        if _.name == where_to_build:
            if _.can_you_build_houses:
                _.build_house(player)
                return "You've built a house."
            else:
                return "You can't build a house here."
        else:
            continue
    return "You don't own this property or invalid Property name"


def remove_house(player):
    where_to_remove = input("Where do you want to remove a house? ")
    for _ in player.properties:
        if _.name == where_to_remove:
            if _.improvement_lvl > 0:
                _.remove_house(player)
                return "You've removed a house."
        else:
            continue
    return "You don't have any houses here or invalid Property name"


def sell_property(player):
    where_to_sell = input("Where do you want to sell a property? ")
    for _ in player.properties:
        if _.name == where_to_sell:
            _.sell(player)
            return "You've sold this property."
        else:
            continue
    return "You don't own this property or invalid Property name"


colour_sizes = {
    "brown": 2,
    "lightBlue": 3,
    "pink": 3,
    "orange": 3,
    "red": 3,
    "yellow": 3,
    "green": 3,
    "darkBlue": 2,

}
