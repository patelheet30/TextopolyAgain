from Models.Game import Game
from Models.Player import Player
from Utils.property_collection import load_squares
from Utils.chance_and_com_collectors import load_chance_and_coms


def setup() -> Game:
    print("Game is initialising...")

    all_squares = load_squares()

    player_list: list[Player] = []

    while True:
        try:
            player_count: int = int(input("How many players do you want? (2-8 players): "))
            if 2 <= player_count <= 8:
                break
            raise ValueError
        except ValueError:
            print("Enter a valid number")
    count = 1
    for _ in range(0, player_count):
        player_list.append(
            Player(
                name=count,
                location=all_squares[0],
                balance=1500,
                properties=[]
            )
        )
        count += 1

    return Game(
        players=player_list,
        squares=all_squares
    )


game = setup()
players_in_game = game.players
squares_in_game = game.squares
chance_cards, com_chest_cards = load_chance_and_coms()
print(game.update_com_chest_dict(com_chest_cards))
print(game.update_chance_dict(chance_cards))
print("Game is ready to start.")

game.start()
