import os

from guizero import *


def start_automation():
    os.system('bash gui.bash')
    # text.value = "automation started"


def full_screen_switch(self):
    if self.full_screen:
        self.full_screen = False
        self.width = 480
        self.height = 480
    else:
        self.full_screen = True


def add_account(ig_username, ig_password):
    with open("IGAccounts.txt", "a") as f:
        f.write(ig_username + "\n")
        f.write(ig_password)
        f.write("\n")
    f.close()


def remove_account(ig_username, ig_password):
    with open("IGAccounts.txt", "r") as f:
        lines = f.readlines()
    with open("IGAccounts.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != ig_username and line.strip("\n") != ig_password:
                f.write(line)
    f.close()


def gui():
    # window = Window(app, title="2nd window")
    # open_button = PushButton(app, text="Open", command=open_window)
    # close_button = PushButton(window, text="Close", command=close_window)

    # bkgrd color

    # write info to file

    app = App(title="Instagram Bot")
    app.full_screen = True

    box_1 = Box(app, width="fill", height=int(app.height / 25), align="top")
    button_minimize = PushButton(box_1, command=lambda: full_screen_switch(app), align="left")
    text_title = Text(box_1, text="Bot Controller", align="bottom", size="20")

    box_2 = Box(app, width=int(app.width * .75), align="left")
    box_2_1 = Box(box_2, width=box_2.width)  # text portion

    # while loop method based on the txt file loaded

    '''
    box_2 = Box(app, width="fill", align="top")
    box_2_1 = Box(box_2, align="left", width=app.width / 3)
    button_automation = PushButton(box_2_1, command=lambda: fun.start_automation(), text="Automation", align="bottom")
    box_2_2 = Box(box_2, align="bottom", width=app.width / 3)
    text_account_number = Text(box_2_2, align="left", text="num.")
    text_account_name = Text(box_2_2, align="left", text="Account")

    text_box = TextBox(app)
    button = PushButton(app, text="submit", align="bottom")
    '''

    app.display()


if __name__ == "__main__":
    username = input("username: ")
    password = input("password: ")
    add_rem = input("add or rem: ")
    if add_rem == "rem":
        remove_account(username, password)
    else:
        add_account(username, password)
