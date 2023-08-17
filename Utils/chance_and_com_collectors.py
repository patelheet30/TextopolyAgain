def load_chance_and_coms():
    with open("./Data/chance.txt", "r") as chanceFile:
        chance = eval(chanceFile.read())

    with open("./Data/comchest.txt", "r") as comChestFile:
        com_chest = eval(comChestFile.read())

    return chance, com_chest
