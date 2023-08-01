def get_player_properties_names(player):
    properties = player.properties
    names = []
    for _ in properties:
        names.append(_.name)

    return names


def check_type(location):
    return type(location)


def pay_tax(player, location):
    player.remove_balance(location.pay_tax(player))
    return f"You've paid {location.pay_tax(player)} in tax because you landed on {location.name}"