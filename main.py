import tkinter as tk
import random

default_bots = [
    "244436424140330101141320232031323032001144044100223342022000000222210212012122012000002212100211101011020200010222022000012020000121012111000212020010012011011201101102220111200221200000000112100000000201100120120221211100210110000121020021200000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "531523633112222444440000330444442432210113222222133222033000000000011000000000000000000000000000000002222021121101111222011120122000000000000000000001122001100100000222221221122000000001102000000000000000000000000212200000000000000000000112200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "026161651444443113222000000432210100000222133111222300000000000000000000000000011000000002221000000000000222100000000000000000000222022210111111210002000222100000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
]

def end_training(previous_root, bot_code):

    previous_root.destroy()
    bot_code_root = tk.Tk()
    bot_code_root.title("Bot code")

    if len(bot_code) == 633:
        widgets = [
            tk.Label(bot_code_root, text = "Your bot has finished training!"),
            tk.Label(bot_code_root, text = "Here is your code, keep it somewhere safe!"),
            tk.Entry(bot_code_root, text = bot_code),
            tk.Button(bot_code_root, text = "Copy bot code", command = lambda: [bot_code_root.clipboard_clear(), bot_code_root.clipboard_append(str(bot_code))]),
            tk.Button(bot_code_root, text = "Play your bot!", command = lambda: play_bot(bot_code_root, bot_code)),
            tk.Button(bot_code_root, text = "Exit", command = bot_code_root.destroy)
        ]
    else:
        widgets = [
            tk.Label(bot_code_root, text = "Your bot has not finished training but you can finish training later."),
            tk.Label(bot_code_root, text = "Here is your code, keep it somewhere safe!"),
            tk.Entry(bot_code_root, text = bot_code),
            tk.Button(bot_code_root, text = "Copy bot code", command = lambda: [bot_code_root.clipboard_clear(), bot_code_root.clipboard_append(str(bot_code))]),
            tk.Button(bot_code_root, text = "Exit", command = bot_code_root.destroy)
        ]

    widgets[2].insert(0, bot_code)
    widgets[2].config(state = "readonly")
    for index, widget in enumerate(widgets):
        bot_code_root.rowconfigure(index, weight = 1)
        widget.grid(row = index, column = 0, sticky = "nsew")

    bot_code_root.columnconfigure(0, weight = 1)
    bot_code_root.mainloop()

def start_training(previous_root, bot_code, automation_settings):

    previous_root.destroy()
    trainer_root = tk.Tk()
    trainer_root.title("Trainer")

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
        print("Choosing a square, table: " + table)
        print(0)

        #picks a square if it will make bot win instantly
        squares_left = get_squares_left("X", table)
        for condition in squares_left:
            if len(condition) == 0:
                print("returning 0")
                return 0
            if (len(condition) == 1) and (table[condition[0]]) == "-" and (automation_settings["bot_win"]):
                return condition[0]
            
        print(1)
        
        #pick a square if it will stop human win instantly
        squares_left = get_squares_left("O", table)
        for condition in squares_left:
            if len(condition) == 0:
                return 0
            if (len(condition) == 1) and (table[condition[0]] == "-") and (automation_settings["human_win"]):
                return condition[0]
        print(2)
        if automation_settings["last_square"]:
            #pick the first availabe square if less than 3 left
            if table.count("-") == 1:
                return table.index("-")
        
        if automation_settings["random"]:
            #pick random square
            left = random.randint(1, table.count("-"))
            for index, character in enumerate(table):
                if character == "-":
                    left -= 1
                    if left == 0:
                        return index
            
        print("No available square found.")
        #manually choose a square
        return 9

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
        return int(bot_code[index])

    def get_table(human_scenario: list):

        moves_left = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        moves_done = []
        table = "-"*9

        for index in range(len(human_scenario)-1, -1, -1):
            moves_done.append(moves_left[get_move(human_scenario[index+1:])]) #bot move
            moves_left.pop(get_move(human_scenario[index+1:]))
            moves_done.append(moves_left[human_scenario[index]]) #human move
            moves_left.pop(human_scenario[index])

        bot_to_move = True
        for move in moves_done:
            table = table[:move] + ["O", "X"][int(bot_to_move)] + table[move+1:]
            bot_to_move = not bot_to_move
        return table

    def add_data(choice):
        nonlocal bot_code
        dashes = 0
        for index in range(choice):
            if table[index] == "-":
                dashes += 1
        bot_code += str(dashes)

    length = len(bot_code)
    human_scenario = []
    
    def on_square_click(index):
        nonlocal human_scenario
        if get_table(human_scenario)[index] != "-":
            return
        add_data(index)

        while True:
            table = get_table(human_scenario)
            choice = choose(table)

            if choice == 9:
                for index in range(9):
                    squares[index].config(text = table[index])
                break
            else:
                add_data(choice)

            human_scenario = next_human_scenario(human_scenario)
            if len(human_scenario) == 5:
                end_training(trainer_root, bot_code)
        
        human_scenario = next_human_scenario(human_scenario)
        table = get_table(human_scenario)
        for index in range(9):
            squares[index].config(text = table[index])

    #create grid
    squares = []
    for index in range(9):
        square = tk.Button(trainer_root, command = lambda index=index: on_square_click(index))
        squares.append(square)
        square.grid(row = index // 3, column = index % 3, sticky = "nsew")
    for row in range(3):
        trainer_root.rowconfigure(row, weight = 1)
    for column in range(3):
        trainer_root.columnconfigure(column, weight = 1)
    
    for index in range(length):
        human_scenario = next_human_scenario(human_scenario)
    while True:
        table = get_table(human_scenario)
        choice = choose(table)
        if choice == 9:
            for index in range(9):
                squares[index].config(text = table[index])
            break
        else:
            add_data(choice)

        human_scenario = next_human_scenario(human_scenario)
        if len(human_scenario) == 5:
            end_training(trainer_root, bot_code)

    trainer_root.bind("<Escape>", lambda event: end_training(trainer_root, bot_code))
    trainer_root.mainloop()

def make_bot(previous_root):

    previous_root.destroy()
    settings_root = tk.Tk()
    settings_root.title("Settings")

    automation_settings = {
        "bot_win": False,
        "human_win": False,
        "last_square": True,
        "random": False,
    }
    widgets = [
        tk.Label(settings_root, text = "Already started training? Paste bot code below. If not, leave empty."),
        tk.Entry(settings_root),
        tk.Label(settings_root, text = "Automatically choose if..."),
        tk.Button(settings_root, text = "Bot can win instantly: OFF", background = "#FF0000"),
        tk.Button(settings_root, text = "Human can win in next turn: OFF", background = "#FF0000"),
        tk.Button(settings_root, text = "It is the last square: ON", background = "#00FF00"),
        tk.Button(settings_root, text = "Pick random square: OFF", background = "#FF0000"),
        tk.Button(settings_root, text = "Start training!")
    ]

    settings_root.columnconfigure(0, weight = 1)
    for index, widget in enumerate(widgets):
        settings_root.rowconfigure(index, weight = 1)
        widget.grid(row = index, column = 0, sticky = "nsew")
    
    def toggle(button):
        if button.cget("background") == "#FF0000":
            button.config(text = button.cget("text").replace("OFF", "ON"), background = "#00FF00")
        else:
            button.config(text = button.cget("text").replace("ON", "OFF"), background = "#FF0000")

    for index in range(3, 7):
        widgets[index].configure(command = lambda index = index: toggle(widgets[index]))

    def destroy():
        automation_settings["bot_win"]= widgets[3].cget("text").endswith("ON")
        automation_settings["human_win"] = widgets[4].cget("text").endswith("ON")
        automation_settings["last_square"] = widgets[5].cget("text").endswith("ON")
        automation_settings["random"] = widgets[6].cget("text").endswith("ON")
        
        start_training(settings_root, widgets[1].get(), automation_settings)
    widgets[7].configure(command = destroy)

    settings_root.mainloop()

def end_play(previous_root, winner, bot_code):
    results_root = tk.Tk()
    results_root.title("Results")

    widgets = [
        tk.Label(results_root),
        tk.Button(results_root, text = "Play again", command = lambda: [previous_root.destroy(), play_bot(results_root, bot_code)]),
        tk.Button(results_root, text = "Make another bot", command = lambda: [previous_root.destroy(), make_bot(results_root)]),
        tk.Button(results_root, text = "Exit", command = lambda: [previous_root.destroy(), results_root.destroy()])
    ]

    if winner == "-":
        widgets[0].config(text = "Draw!")
    elif winner == "X":
        widgets[0].config(text = "The bot wins!")
    elif winner == "O":
        widgets[0].config(text = "You win!")

    for index, widget in enumerate(widgets):
        results_root.rowconfigure(index, weight = 1)
        widget.grid(row = index, column = 0, sticky = "nsew")

    results_root.mainloop()

def play(previous_root, bot_code):
    previous_root.destroy()
    play_root = tk.Tk()
    play_root.title("Play")

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
        return int(bot_code[index])

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
    turns = 0

    def on_square_click(choice):

        nonlocal human_scenario
        nonlocal turns
        table = get_table(human_scenario)
        if table[choice] != "-":
            return
        
        turns += 1
        dashes = 0
        for index in range(choice):
            if table[index] == "-":
                dashes += 1
        human_scenario.insert(0, dashes)

        table = get_table(human_scenario)
        for index in range(9):
            squares[index].config(text = table[index])

        if check_win(table):
            if check_win(table) == "X":
                end_play(play_root, "X", bot_code)
            else:
                end_play(play_root, "O", bot_code)
        elif turns == 4:
            end_play(play_root, "-", bot_code)

    #create grid
    squares = []
    for index in range(9):
        square = tk.Button(play_root, command = lambda choice=index: on_square_click(choice))
        squares.append(square)
        square.grid(row = index // 3, column = index % 3, sticky = "nsew")
    for row in range(3):
        play_root.rowconfigure(row, weight = 1)
    for column in range(3):
        play_root.columnconfigure(column, weight = 1)

    table = get_table(human_scenario)
    for index in range(9):
        squares[index].config(text = table[index])

    if check_win(table):
        if check_win(table) == "X":
            end_play(play_root, "X", bot_code)
        else:
            end_play(play_root, "O", bot_code)
    elif turns == 9:
        end_play(play_root, "-", bot_code)

def play_bot(previous_root, bot_code):
    previous_root.destroy()
    play_options = tk.Tk()
    play_options.title("Bot code")
    play_options.columnconfigure(0, weight = 1)

    code_entry = tk.Entry(play_options)
    code_entry.insert(0, bot_code)

    widgets = [
        tk.Label(play_options, text = "Enter bot code:"),
        code_entry,
        tk.Label(play_options, text = "Don't have a code? Use one of these or make your own!"),
        tk.Button(play_options, text = "Easy bot", background = "#00FF00", command = lambda: [code_entry.delete(0, "end"), code_entry.insert(0, default_bots[0])]),
        tk.Button(play_options, text = "Medium bot", background = "#FFFF00", command = lambda: [code_entry.delete(0, "end"), code_entry.insert(0, default_bots[1])]),
        tk.Button(play_options, text = "Hard bot", background = "#FF0000", command = lambda: [code_entry.delete(0, "end"), code_entry.insert(0, default_bots[2])]),
        tk.Button(play_options, text = "Random bot", background = "#0000FF", command = lambda: [code_entry.delete(0, "end"), code_entry.insert(0, default_bots[random.randint(0, 2)])]),
        tk.Button(play_options, text = "Make your own", command = lambda: make_bot(play_options)),
        tk.Button(play_options, text = "Play!", command = lambda: play(play_options, code_entry.get()))
    ]

    for index, widget in enumerate(widgets):
        play_options.rowconfigure(index, weight = 1)
        widget.grid(row = index, column = 0, sticky = "nsew")

    play_options.mainloop()

def options():
    options_root = tk.Tk()
    options_root.title("Make or play?")
    tk.Button(options_root, text = "Make a bot", command = lambda: make_bot(options_root)).grid(row = 0, column = 0, sticky = "nsew")
    tk.Button(options_root, text = "Play a bot", command = lambda: play_bot(options_root, "")).grid(row = 1, column = 0, sticky = "nsew")
    options_root.rowconfigure(0, weight = 1)
    options_root.rowconfigure(1, weight = 1)
    options_root.columnconfigure(0, weight = 1)
    options_root.mainloop()

options()