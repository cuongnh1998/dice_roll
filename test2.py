from diceroll import roll_the_dice, special_roll
from helpers import generate_surprises


def initialise_game() -> dict:
    players = {"Red": 0, "Blue": 0, "Green": 0, "White": 0}
    snakes = {"25": 6, "44": 23, "65": 34, "76": 28, "99": 56}
    ladders = {"8": 43, "26": 39, "38": 55, "47": 81, "66": 92}
    game = {
        "players": players,
        "snakes": snakes,
        "ladders": ladders,
    }
    return game


def get_num_players() -> int:
    numb_players = int(input("Please enter the number of players between 1 and 4: "))
    while numb_players > 4 or numb_players < 1:
        numb_players = int(input("Please enter the number of players between 1 and 4: "))
    return numb_players


def play_game(game: dict) -> str:
    surprise_tiles = generate_surprises()
    game["surprise_tiles"] = surprise_tiles
    game["skip"] = False
    while True:
        for player_name in game['players']:
            # ignore the next one
            if game["skip"]:
                game["skip"] = False
                print(f"Player {player_name} skiped")
                continue
            die_roll = roll_the_dice()
            print(f"{player_name} rolled a {die_roll}")
            move_player(game, player_name, die_roll)
            winner = pick_winner(game['players'])
            if winner:
                print(f"Congratulations {winner}, you have won the game!")
                return winner


def move_player(game, current_player, diceroll):
    position = game['players'][current_player]
    if position + diceroll <= 100:
        position += diceroll
        if str(position) in game["snakes"]:
            print(current_player, "step into a snakes")
            position = game["snakes"][str(position)]
        elif str(position) in game["ladders"]:
            print(current_player, "step into a ladders")
            position = game["ladders"][str(position)]

    print(f"Player {current_player} position {position}")
    game['players'][current_player] = position

    if position in game["surprise_tiles"]:
        print(f"Player : {current_player} is surprised")
        special_result = special_roll()
        handle_specical_roll(game, current_player, special_result)


def pick_winner(players: dict) -> str:
    for player, position in players.items():
        if position == 100:
            return player
    return None


def handle_specical_roll(game, current_player, special_result):
    if special_result == 0:
        print(f"{current_player} gets an extra roll!")
        extra_roll = roll_the_dice()
        move_player(game, current_player, extra_roll)
    elif special_result == 1:
        print(f"The next player loses a turn!")
        game['skip'] = True
    elif special_result == 2:
        print(f"All other players move back 5 spaces!")
        for player, position in game['players'].items():
            if player != current_player:
                game['players'][player] = max(0, position - 5)
                print(f"New position for player : {player} is : {game['players'][player]}")
        print(f"Position all player is : {game['players']}")


def turn_by_turn_gameplay():
    manual_game = initialise_game()
    numb_players = 2
    action = input("Please input 'roll' to roll the dice or 'quit' to quit the game: ")
    if action == "quit":
        return
    elif action == "roll":
        diceroll = roll_the_dice()

    winner = play_game(manual_game)
    print(f"The winner is {winner}!")

    return


def main():
    game = initialise_game()
    num_players = get_num_players()
    winner = play_game(game)
    print(f"The winner is {winner}!")
    # print(position)

    # Play a turn by turn game
    turn_by_turn_gameplay()


if __name__ == '__main__':
    main()
