from Models.Game import Game
from Models.Player import Player
from Utils.property_collection import load_squares


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
players = game.players
squares = game.squares

game.start()
