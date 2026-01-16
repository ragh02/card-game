# Program structure

## Function details
**Database functions:**<br>
Functions that interact with the database

| Function name | Parameters | Output | Purpose |
| ------------- | ---------- | ------ | ------- |
| init_db | db_name (str) | None | Initialise the database and create required tables if missing |
| execute_query | query (str) | list (str) | Runs an SQL query on the database |

**Configuration functions:**<br>
Functions that interact with the YAML config file

| Function name | Parameters | Output | Purpose |
| ------------- | ---------- | ------ | ------- |
| load_config_file | filename (str) | config (dictionary) | Reads the YAML config file and converts it into a dictionary. |
| create_config_file | filename (str, default="config.yml"), config_dict (dict, default="{"version": 1,"database_file": "card_game.db"}") | None | Creates a new YAML config file |
