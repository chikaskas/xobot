bot_file = open("good_bot.txt", "r")
bot_data = bot_file.readline()
bot_file.close()

def get_move(human_scenario: list):
    min = [1, 9, 57, 249][len(human_scenario)-1]
    lenght = len(human_scenario)
    if lenght == 0:
        index = 0
    elif lenght == 1:
        index = 1 + human_scenario[0]
    elif lenght == 2:
        index = 9 + human_scenario[1]*6 + human_scenario[0]
    elif lenght == 3:
        index = 57 + human_scenario[2]*6*4 + human_scenario[1]*4 + human_scenario[0]
    elif lenght == 4:
        index = 249 + human_scenario[3]*6*4*2 + human_scenario[2]*4*2 + human_scenario[1]*2 + human_scenario[0]
    return int(bot_data[index])

def get_table(human_scenario: list):
    moves_left = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    moves_done = []
    table = "-"*9

    moves_done.append(moves_left[get_move([])]) #bot move
    moves_left.pop(get_move([]))

    for index in range(len(human_scenario)-1, -1, -1):
        moves_done.append(moves_left[human_scenario[index]]) #human move
        moves_left.pop(human_scenario[index])
        moves_done.append(moves_left[get_move(human_scenario[index:])]) #bot move
        moves_left.pop(get_move(human_scenario[index:]))

    bot_to_move = True
    for move in moves_done:
        table = table[:move] + ["O", "X"][int(bot_to_move)] + table[move+1:]
        bot_to_move = not bot_to_move
    return table

def display_table(table: str):
    print(table[0:3])
    print(table[3:6])
    print(table[6:9])

def get_squares_left(player_char: str, table: str):
    squares_left = [
    [0, 1, 2], #row 1
    [3, 4, 5], #row 2
    [6, 7, 8], #row 3
    [0, 3, 6], #column 1
    [1, 4, 7], #column 2
    [2, 5, 8], #column 3
    [0, 4, 8], #diagonal 1
    [2, 4, 6]  #diagonal 2
]
    for index, character in enumerate(table):
        if character == player_char:
            for condition in squares_left:
                if index in condition:
                    condition.remove(index)
    return squares_left

def check_win(table: str):

    X_squares_left = get_squares_left("X", table)
    for condition in X_squares_left:
        if len(condition) == 0:
            return "X"
    
    O_squares_left = get_squares_left("O", table)
    for condition in O_squares_left:
        if len(condition) == 0:
            return "O"
    
    return False
        

human_scenario = []
for turn in range(4):
    table = get_table(human_scenario)
    display_table(table)

    choice = int(input())
    if table[choice] != "-":
        print("That square is already taken!")
        exit()
    dashes = 0
    for index in range(choice):
        if table[index] == "-":
            dashes += 1
    human_scenario.insert(0, dashes)

    table = get_table(human_scenario)
    display_table(table)

    if check_win(table):
        if check_win(table) == "X":
            print("Bot wins the game!")
            exit()
        else:
            print("You win the game!")
            exit()
        break
print("No one wins!")