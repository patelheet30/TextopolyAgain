def get_player_properties_names(player):
    properties = player.properties
    names = []
    for _ in properties:
        names.append(_.name)

    return names
