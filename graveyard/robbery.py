import random
import math

GRID_SIZE = 5

def display_instructions():
    print("Welcome to the Graveyard Robbery Game!")
    print("You are on a 5x5 grid, and your goal is to find the hidden treasure.")
    print("You can move using the commands: 'up', 'down', 'right', 'left'")
    print("The grid will show your positions as '🕴️'")
    print("Try to find the treasure by getting 'warmer' or 'colder' clues!")
    print("Good luck!")

def display_grid(player_position):
    for y in range(GRID_SIZE):
        row = ""
        for x in range(GRID_SIZE):
            if (x, y) == player_position:
                row += " 🕴️ "
            else:
                row += " 🪦 "
        print(row)

def calculate_distance(pos1, pos2): #pos = (x,y)
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]

    delta_distance = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
    rounded_distance = round(delta_distance)

    return abs(rounded_distance)

def get_random_position():
    return (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE -1))

def treasure_hunt_game():
    display_instructions()

    player_position = get_random_position()
    treasure_position = get_random_position()

    while player_position == treasure_position: #no spawn same location
        player_position = get_random_position()

    previous_distance = calculate_distance(player_position, treasure_position)

    while True:
        print("\nHere is your current location on the grid: ") # \n ~ escape character
        display_grid(player_position)

        move = input("Move (up/down/left/right): ").lower()

        if move == "up" and player_position[1] > 0:
            player_position = (player_position[0], player_position[1] - 1)

        elif move == "down" and player_position[1] < GRID_SIZE - 1:
            player_position = (player_position[0], player_position[1] + 1)

        elif move == "left" and player_position[0] > 0:
            player_position = (player_position[0] - 1, player_position[1])

        elif move == "right" and player_position[0] < GRID_SIZE - 1:
            player_position = (player_position[0] + 1, player_position[1])
        
        else:
            print("Invalid move. Please try again.")
            continue

        current_distance = calculate_distance(player_position, treasure_position)

        if current_distance == 0:
            print("\nCongradulations! You found the treasure!")
            print(f"The treasure was hidden at {treasure_position}!")
            break
        elif current_distance < previous_distance:
            print("Warmer! You're getting closer!")
        else:
            print("Colder! You're moving away.")

        previous_distance = current_distance

treasure_hunt_game()