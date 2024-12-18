bot_data = ""

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
    return bot_data[index]

def get_table(total_scenario: list):
    return