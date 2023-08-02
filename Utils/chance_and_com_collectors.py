def load_chance_and_coms():
    with open("./Data/chance.txt", "r") as chanceFile:
        chance = eval(chanceFile.read())

    with open("./Data/comchest.txt", "r") as comChestFile:
        comChest = eval(comChestFile.read())

