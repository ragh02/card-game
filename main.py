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
def do_authentication(username, password, db_file):
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    users = execute_query("SELECT password FROM users WHERE username = ? LIMIT 1",(username,),db_file)
    return True if users[0][0] == pw_hash else False

def add_user(username, password, db_file):
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    execute_query("""INSERT INTO users (username, password) VALUES (?, ?)""", (username, pw_hash), db_file)

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


# testing area
# warn("go away")
db_name = "main.db"
init_db(db_name)
# add_user("parabola","tomas",db_name)
print(do_authentication("parabola","tomas",db_name))

card1 = Card(1,1)
# print(compare_cards(card1,card1))
deck = create_deck()

# TEMP CONFIG - FOR DEV USE ONLY
auto_mode = False

# Main game loop (anti-KeyboardInterrupt coming soon)
p1_cards = 0
p2_cards = 0
round = 0
while len(deck) > 1:
    round += 1
    if not auto_mode:
        print(f"{col.bold}===== ROUND {round} ====={col.end}")
        print(f"Player 1's turn!")
        input("Press ENTER to draw a card:")
        deck,a = draw_card(deck)
        print(f"You took a{do_colour_formatting(a)}{col.bold} {a}{col.end}")

        # do_new_lines()
        print()

        print(f"Player 2's turn!")
        input("Press ENTER to draw a card:")
        deck, b = draw_card(deck)
        print(f"You took a{do_colour_formatting(b)}{col.bold} {b}{col.end}")

        do_new_lines()
    else:
        deck,a = draw_card(deck)
        deck, b = draw_card(deck)
    result = compare_cards(a, b)

    if result == 0:
        print(f"Player 1's card: {do_colour_formatting(a)}{col.green}{col.bold}{a}{col.end}")
        print(f"Player 2's card: {do_colour_formatting(b)}{col.red}{col.bold}{b}{col.end}")
        print(f"{col.blue}{col.bold}Player {result + 1} wins and takes both cards.{col.end}")
        print()
        p1_cards += 2
        print(f"Player 1's cards: {col.green}{p1_cards} (+2) {col.end}")
        print(f"Player 2's cards: {col.red}{p2_cards}  {col.end}")
    else:
        print(f"Player 1's card: {do_colour_formatting(a)}{col.red}{col.bold}{a}{col.end}")
        print(f"Player 2's card: {do_colour_formatting(b)}{col.green}{col.bold}{b}{col.end}")
        print(f"{col.blue}{col.bold}Player {result + 1} wins and takes both cards.{col.end}")
        print()
        p2_cards += 2
        print(f"Player 1's cards: {col.red}{p1_cards} {col.end}")
        print(f"Player 2's cards: {col.green}{p2_cards} (+2) {col.end}")

    input("Press ENTER to go to the next round")
    do_new_lines()

# handle end of game
print(f"{col.bold}{col.blue}END OF GAME!{col.end}")
if p1_cards > p2_cards:
    print(f"Player 1's cards: {col.green}{p1_cards} {col.end}")
    print(f"Player 2's cards: {col.red}{p2_cards} {col.end}")
    print(f"{col.bold}{col.blue}Player 1 wins! {col.end}")
    raise SyntaxWarning("Bye bye!")

else:
    print(f"Player 1's cards: {col.red}{p1_cards} {col.end}")
    print(f"Player 2's cards: {col.green}{p2_cards} {col.end}")
    print(f"{col.bold}{col.blue}Player 2 wins! {col.end}")
    raise SyntaxWarning("Bye bye!")

