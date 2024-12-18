bot_file = open("good_bot.txt", "a+")
bot_file.seek(0)
bot_data = bot_file.readlines()[0]
def prompt(table: str):
    print(table[0:3])
    print(table[3:6])
    print(table[6:9])
    valid = False
    while not valid:
        str_input = input()
        valid = str_input in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        if valid:
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

    #picks a square if it will make bot win instantly
    squares_left = get_squares_left("X", table)
    for condition in squares_left:
        if len(condition) == 1:
            return condition[0]
    
    #pick a square if it will stop human win instantly
    squares_left = get_squares_left("O", table)
    for condition in squares_left:
        if len(condition) == 1:
            return condition[0]
        
    #pick the first availabe square if less than 3 left
    if table.count("-") < 3:
        return table.index("-")
    
    #manually choose a square
    return prompt(table)

def add_data(data: str):
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


bot_file.close()