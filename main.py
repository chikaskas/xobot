import tkinter as tk

def start_training(previous_root, bot_code, automation_settings):

    previous_root.destroy()
    trainer_root = tk.Tk()
    trainer_root.title("Trainer")
    
    def on_square_click(index):
        return

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
    
    trainer_root.mainloop()

def make_bot(previous_root):

    previous_root.destroy()
    settings_root = tk.Tk()
    settings_root.title("Settings")

    automation_settings = {
        "bot_win": False,
        "human_win": False,
        "last_square": True
    }
    widgets = [
        tk.Label(settings_root, text = "Already started training? Paste bot code below. If not, leave empty."),
        tk.Entry(settings_root),
        tk.Label(settings_root, text = "Automatically choose if..."),
        tk.Button(settings_root, text = "Bot can win instantly: OFF", background = "#FF0000"),
        tk.Button(settings_root, text = "Human can win in next turn: OFF", background = "#FF0000"),
        tk.Button(settings_root, text = "It is the last square: ON", background = "#00FF00"),
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

    widgets[3].configure(command = lambda: toggle(widgets[3]))
    widgets[4].configure(command = lambda: toggle(widgets[4]))
    widgets[5].configure(command = lambda: toggle(widgets[5]))

    def destroy():
        automation_settings["bot_win"]= widgets[3].cget("text").endswith("ON")
        automation_settings["human_win"] = widgets[4].cget("text").endswith("ON")
        automation_settings["last_square"] = widgets[5].cget("text").endswith("ON")
        if widgets[1].get() == "":
            widgets[1].insert(0, "0")
        start_training(settings_root, int(widgets[1].get(), 16), automation_settings)
    widgets[6].configure(command = destroy)

    settings_root.mainloop()

def play_bot(previous_root):
    previous_root.destroy()
    play_root = tk.Tk()
    play_root.title("Play")

    def on_square_click(index):
        return

    #create grid
    squares = []
    for index in range(9):
        square = tk.Button(play_root, command = lambda index=index: on_square_click(index))
        squares.append(square)
        square.grid(row = index // 3, column = index % 3, sticky = "nsew")
    for row in range(3):
        play_root.rowconfigure(row, weight = 1)
    for column in range(3):
        play_root.columnconfigure(column, weight = 1)
    
    play_root.mainloop()

def options():
    options_root = tk.Tk()
    options_root.title("Make or play?")
    tk.Button(options_root, text = "Make a bot", command = lambda: make_bot(options_root)).grid(row = 0, column = 0, sticky = "nsew")
    tk.Button(options_root, text = "Play a bot", command = lambda: play_bot(options_root)).grid(row = 1, column = 0, sticky = "nsew")
    options_root.rowconfigure(0, weight = 1)
    options_root.rowconfigure(1, weight = 1)
    options_root.columnconfigure(0, weight = 1)
    options_root.mainloop()

options()