# Copyright (c) 2026 Harish Raghavan. All rights reserved
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Two-player card game
import sqlite3
import random
from warnings import warn
from libs.col import *
import os
import sys
import yaml
import hashlib
import time

# Initialise the SQLite DB and create tables if they don't exist
def init_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # table 1: users
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    result = c.fetchall()
    # print(result)
    if len(result) == 0:
        c.execute('''CREATE TABLE users (
                username TEXT,
                password TEXT
                )''')

    # table 2: leaderboard
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leaderboard';")
    result = c.fetchall()
    if len(result) == 0:
        c.execute('''CREATE TABLE leaderboard (
                    username TEXT,
                    score INTEGER
                    )''')
    conn.commit()
    conn.close()

# Execute an SQL query and return a result
def execute_query(query,params,db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(query,params)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result


# Loads the YAML config file
def load_config_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            config_dict = yaml.safe_load(f)
            return config_dict
    else:
        return("That file doesn't exist!")

# Creates a new YAML config file
def create_config_file(filepath="config.yml", config_dict=None):
    if config_dict is None:
        config_dict = {
            "version": 1,
            "database_file": "card_game.db",
            "admin": "admin",
            "admin_pw": "12345"
        }
    with open(filepath, "w") as f:
        yaml.dump(config_dict, f)

# Does authentication. Reads the global config file
def do_authentication_inner(username, password, db_file):
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    users = execute_query("SELECT password FROM users WHERE username = ? LIMIT 1",(username,),db_file)
    if len(users) != 0:
        return True if users[0][0] == pw_hash else False
    else:
        return False

def add_user(username, password, db_file):
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    execute_query("""INSERT INTO users (username, password) VALUES (?, ?)""", (username, pw_hash), db_file)


# THI SECTION DEFINES FUNCTIONS MANAGING THE AUTHENTICATION SYSTEM
def do_authentication(user,db, admin_pw, admin_user, forbidden):
    print(f"{col.bold}{user}{col.end}")
    username = input("--> ")
    print()
    print(f"{col.bold}Please enter your password.{col.end}")
    password = input(f"{col.end}--> ")
    if username in forbidden:
        return False
    if password == admin_pw and username == admin_user:
        print(f"Admin mode enabled. Type command 1 to add a user, 2 to remove a user and 3 to see all users or 4 to reset the leaderboard")
        choice = input("--> ")
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            add_user(username, password, db)
            print(f"Success. Added {username}")
        elif choice == "2":
            username = input("Username: ")
            execute_query("DELETE FROM users WHERE username = ?", (username,), db)
            print(f"Success. Removed {username}")
        elif choice == "3":
            a = execute_query("SELECT username,password FROM users",(),db)
            print(f"{col.bold}List of users:{col.end}")
            print(a)
        elif choice == "4":
            execute_query("DELETE FROM leaderboard",(),db)
            print(f"{col.bold}{col.red}Reset the leaderboard{col.end}")
        else:
            print("Invalid choice! Go away now")
        sys.exit("Admin mode disabled!")
    # print(password)
    if do_authentication_inner(username, password,db):
        print(f"{col.green}You have logged in successfully. Username: {username}.{col.end}")
        return username
    else:
        print(f"{col.red}Invalid username or password.{col.end}")
        return False


# THIS SECTION DEFINES FUNCTIONS RELATED TO LEADERBOARD
def fetch_leaderboard(db_file):
    results = execute_query("SELECT * FROM leaderboard",(),db_file)
    return results[0]

def add_lb_entry(username,score,db_file):
    execute_query("INSERT INTO leaderboard (username, score) VALUES (?, ?)",(username,score),db_file)

# THIS SECTION DEFINES FUNCTIONS MANAGING THE CORE GAME LOOP
# Define a card object
class Card:
    def __init__(self,suit,number):
        self.suit = suit
        self.number = number

    def __str__(self):
        if self.suit == 0:
            return f"Red {self.number}"
        elif self.suit == 1:
            return f"Yellow {self.number}"
        elif self.suit == 2:
            return f"Black {self.number}"
        else:
            return ""


# Custom error
class SetupError(Exception):
    pass


# Create a deck of cards
def create_deck():
    suits = [0,1,2]
    deck = []
    for i in range(3):
        for j in range(10):
            deck.append(Card(suits[i],j+1))

    # make sure to shuffle the deck
    random.shuffle(deck)
    return deck


# Function to compare two cards and select a winner
# Returns '0' if card1 wins or '1' if card2 wins
# NOTE: If the suits are the same and numbers are the same, raise exception as this doesn't happen in a regular game
def compare_cards(card1: Card, card2: Card):
    c1 = card1.suit
    c2 = card2.suit
    if (c1==2 and c2==0) or (c1==0 and c2==2):
        if c1 == 0:
            c2 = -1
        else:
            c1 = -1
    if c1 != c2:
        if c1 > c2:
            return 0
        else:
            return 1

    else:
        if card1.number > card2.number:
            return 0
        elif card2.number > card1.number:
            return 1
        else:
            raise SetupError("There are two identical cards!")

def draw_card(deck):
    a = deck[0]
    deck.pop(0)
    return deck,a

def do_new_lines():
    # print a bunch of new lines since os system clear is broken in pycharm
    for i in range(4):
        print()

def do_colour_formatting(card):
    if card.suit == 0:
        return col.red
    elif card.suit == 1:
        return col.yellow
    else:
        return col.end



# MAIN PROGRAM
if __name__ == "__main__":

    # TEMP CONFIG - FOR DEV USE ONLY
    auto_mode = True
    bypass_auth = False
    wait_x_seconds = 0
    auto_play = False
    require_two_names = False

    # Start by initialising the configuration file
    config = load_config_file("config.yml")
    db_name = config["database_file"]
    admin_user = config["admin"]
    admin_pw = config["admin_pw"]
    init_db(db_name)

    # Authorise user 1
    print(f"{col.bold}Mr Raghavan's {col.blue}FANTASTIC{col.end}{col.bold} two-player card game!{col.end}")

    # top 5 users
    print(f"Top 5 users by score:")
    lb = execute_query("SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5", (), db_name)
    c = 1
    for i in lb:
        print(f"{c}. {i[0]} - {i[1]} cards")
        c += 1

    # press enter
    input(f"{col.bold}Press ENTER to log in...{col.end}")
    do_new_lines()
    do_new_lines()
    do_new_lines()
    if not bypass_auth:
        user_1 = do_authentication("Welcome Player 1, please enter your username below:", db_name, admin_pw, admin_user, [])
        print()
        print("------------------------")
        attempts = 5
        while not user_1:
            attempts -= 1
            if attempts < 1:
                sys.exit("Sorry, you do not have permission to run this program!")
            user_1 = do_authentication(f"{col.red}({attempts} attempts left) Try again. Username:{col.end}",db_name,admin_pw,admin_user, [])
            print()
            print("------------------------")
            print()

        # Authorise user 2
        user_2 = do_authentication("Welcome Player 2, please enter your username below:", db_name, admin_pw, admin_user, [user_1])
        print()
        print("------------------------")
        attempts = 5
        while not user_2:
            attempts -= 1
            if attempts < 1:
                sys.exit("Sorry, you do not have permission to run this program!")
            user_2 = do_authentication(f"{col.red}({attempts} attempts left) Try again. Username:{col.end}", db_name, admin_pw,
                                       admin_user,[user_1])
            print()
            print("------------------------")
            print()
    else:
        user_1 = "Test User A"
        user_2 = "Test User B"



    card1 = Card(1,1)
    # print(compare_cards(card1,card1))
    deck = create_deck()



    # Main game loop (anti-KeyboardInterrupt aka handling errors gracefully coming soon)
    p1_cards = 0
    p2_cards = 0
    player_names = [user_1, user_2]
    round = 0
    while len(deck) > 1:
        round += 1
        if not auto_mode:
            print(f"{col.bold}===== ROUND {round} ====={col.end}")
            print(f"{user_1}'s turn!")
            input("Press ENTER to draw a card:")
            deck,a = draw_card(deck)
            print(f"You took a{do_colour_formatting(a)}{col.bold} {a}{col.end}")

            # do_new_lines()
            print()

            print(f"{user_2}'s turn!")
            input("Press ENTER to draw a card:")
            deck, b = draw_card(deck)
            print(f"You took a{do_colour_formatting(b)}{col.bold} {b}{col.end}")

            do_new_lines()
        else:
            # New refined UI with less user requirements
            print(f"{col.bold}===== ROUND {round}/15 ====={col.end}")
            if p1_cards > p2_cards:
                print(f"{col.green}{user_1}'s cards: {p1_cards}  {col.end}")
                print(f"{col.red}{user_2}'s cards: {p2_cards}  {col.end}")
            elif p2_cards > p1_cards:
                print(f"{col.red}{user_1}'s cards: {p1_cards}  {col.end}")
                print(f"{col.green}{user_2}'s cards: {p2_cards}  {col.end}")
            else:
                print(f"{user_1}'s cards: {p1_cards}  {col.end}")
                print(f"{user_2}'s cards: {p2_cards}  {col.end}")

            if not auto_play:
                if require_two_names:
                    try:
                        input("Player 1: Press ENTER to draw cards:")
                        input("Player 2: Press ENTER to draw cards:")
                        print("Please wait...")
                    except KeyboardInterrupt:
                        sys.exit(f"Exited program. The current game has NOT been saved.")
                else:
                    try:
                        input("Press ENTER to draw cards:")
                        print("Please wait...")
                    except KeyboardInterrupt:
                        sys.exit(f"Exited program. The current game has NOT been saved.")
                do_new_lines()
            else:
                print("Cards draw automatically!")
                time.sleep(wait_x_seconds)
            print("===== RESULTS =====")
            deck,a = draw_card(deck)
            deck, b = draw_card(deck)
        result = compare_cards(a, b)

        if result == 0:
            print(f"{user_1}'s card: {do_colour_formatting(a)}{col.green}{col.bold}{a}{col.end}")
            print(f"{user_2}'s card: {do_colour_formatting(b)}{col.red}{col.bold}{b}{col.end}")
            print(f"{col.blue}{col.bold}{player_names[result]} wins and takes both cards.{col.end}")
            print()
            p1_cards += 2
            print(f"{user_1}'s cards: {col.green}{p1_cards} (+2) {col.end}")
            print(f"{user_2}'s cards: {col.red}{p2_cards}  {col.end}")
        else:
            print(f"{user_1}'s card: {do_colour_formatting(a)}{col.red}{col.bold}{a}{col.end}")
            print(f"{user_2}'s card: {do_colour_formatting(b)}{col.green}{col.bold}{b}{col.end}")
            print(f"{col.blue}{col.bold}{player_names[result]} wins and takes both cards.{col.end}")
            print()
            p2_cards += 2
            print(f"{user_1}'s cards: {col.red}{p1_cards} {col.end}")
            print(f"{user_2}'s cards: {col.green}{p2_cards} (+2) {col.end}")

        print(f"{col.bold}Next round starts in {wait_x_seconds} seconds. {col.end}")

        try:
            time.sleep(wait_x_seconds)
        except KeyboardInterrupt:
            sys.exit(f"Exited program. The current game has NOT been saved.")
        do_new_lines()
        do_new_lines()

    # handle end of game
    print(f"{col.bold}{col.blue}END OF GAME!{col.end}")
    if p1_cards > p2_cards:
        print(f"{user_1}'s cards: {col.green}{p1_cards} {col.end}")
        print(f"{user_2}'s cards: {col.red}{p2_cards} {col.end}")
        print(f"{col.bold}{col.blue}{user_1} wins! {col.end}")


    else:
        print(f"{user_1}'s cards: {col.red}{p1_cards} {col.end}")
        print(f"{user_2}'s cards: {col.green}{p2_cards} {col.end}")
        print(f"{col.bold}{col.blue}{user_2} wins! {col.end}")


    # Save data to the leaderboard
    # (remove print statements in final program)
    # print(f"Player {user_1} finished game with {p1_cards} cards")
    # print(f"Player {user_2} finished game with {p2_cards} cards")
    # print("Saving now.")
    add_lb_entry(user_1,p1_cards,db_name)
    add_lb_entry(user_2, p2_cards, db_name)
    # print("All done. Hopefully no tracebacks show up.")
    input("Press ENTER for the leaderboard")
    lb = execute_query("SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5",(),db_name)
    c = 1
    for i in lb:
        print(f"{c}. {i[0]} - {i[1]} cards")
        c += 1

