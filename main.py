# Copyright (c) 2026 Harish Raghavan. All rights reserved
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Two-player card game
import sqlite3
import random
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
def execute_query(query,params):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(query,params)
    result = c.fetchall()
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
            "database_file": "card_game.db"
        }
    with open(filepath, "w") as f:
        yaml.dump(config_dict, f)

# Does authentication. Reads the global config file
def do_authentication(username, password, db_file):
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    users = execute_query("SELECT password FROM users WHERE username = ?",username)