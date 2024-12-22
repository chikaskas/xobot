bot_file = open("bot_data.txt", "a+")
bot_file.seek(0)
bot_data = bot_file.readline()
def prompt(table: str):
    print(table[0:3])
    print(table[3:6])
    print(table[6:9])
    valid = False
    while not valid:
        str_input = input()
        valid = str_input in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "exit"]
        if valid:
            if str_input == "exit":
                bot_file.close()
                exit()
            if table[int(str_input)] == "-":
                return int(str_input)
            else:
                valid = False
        print("Invalid input, try again.")

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

def choose(table: str):
    print("Choosing a square...")

    #picks a square if it will make bot win instantly
    squares_left = get_squares_left("X", table)
    for condition in squares_left:
        if len(condition) == 0:
            return 0
        if (len(condition) == 1) and (table[condition[0]] == "-"):
            return condition[0]
    
    #pick a square if it will stop human win instantly
    squares_left = get_squares_left("O", table)
    for condition in squares_left:
        if len(condition) == 0:
            return 0
        if (len(condition) == 1) and (table[condition[0]] == "-"):
            return condition[0]
        
    #pick the first availabe square if less than 3 left
    if table.count("-") < 3:
        return table.index("-")
    
    #manually choose a square
    return prompt(table)

def add_data(data: str):
    global bot_data
    if not (data in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]):
        raise ValueError("Invalid input")
    bot_file.write(data)
    bot_data += data

def next_human_scenario(current_human_scenario: list):
    if len(current_human_scenario) == 0: #special case: first scenario
        return [0]
    #increase the scenario
    current_human_scenario[0] += 1
    #validate scenario
    lenght = len(current_human_scenario)
    for index in range(lenght):
        max = 10 +2*index -2*lenght
        if current_human_scenario[index] == max:
            current_human_scenario[index] = 0
            if index == lenght-1: #special case: enough senarios in class
                return [0]*(lenght+1)
            current_human_scenario[index+1] += 1
    if len(current_human_scenario) == 5: #special case: enough senarios
        return False
    return current_human_scenario

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
    print(f"Human scenario: {human_scenario}")

    moves_left = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    moves_done = []
    table = "-"*9

    for index in range(len(human_scenario)-1, -1, -1):
        moves_done.append(moves_left[get_move(human_scenario[index+1:])]) #bot move
        moves_left.pop(get_move(human_scenario[index+1:]))
        moves_done.append(moves_left[human_scenario[index]]) #human move
        moves_left.pop(human_scenario[index])
    
    print(moves_done)
    print(moves_left)

    bot_to_move = True
    for move in moves_done:
        table = table[:move] + ["O", "X"][int(bot_to_move)] + table[move+1:]
        bot_to_move = not bot_to_move
    return table

length = len(bot_data)
leftover = length
human_scenario = []
while True:
    if leftover > 0: #skip already trained senario
        leftover -= 1
        human_scenario = next_human_scenario(human_scenario)
        continue

    table = get_table(human_scenario)
    choice = choose(table)
    print(f"Chose {choice}")
    dashes = 0
    for index in range(choice):
        if table[index] == "-":
            dashes += 1
    add_data(str(dashes))

    human_scenario = next_human_scenario(human_scenario)
    if len(human_scenario) == 5:
        break

bot_file.close()
