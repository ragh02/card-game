# Data design
## Main database
**game.db** - stores all game information in a SQLite database
Two tables:
- leaderboard - stores all scores and usernames
- users - stores usernames and passwords

**Table 1: leaderboard**
Keeps a record of all player scores
Contains two columns:
- username (TEXT) - stores the username of the player who got that score
- score (INTEGER) - stores the number of cards the player got

**Table 2: users**
Keeps a record of authorised users
Contains two columns:
- username (TEXT) - stores the username
- password (TEXT) - stores the hashed password provided by the user.

# Data dictionary (variables)

| Name      | Type | Example | Purpose | Validation/constraints |
| --------- | ---- | ------- | ------- | ---------------------- |
| **p1** | str | "thomas" | Stores the username of Player 1 | Cannot be empty, authorised |
| **p2** | str | "damian" | Stores the username of Player 2 | Cannot be empty, authorised, cannot equal p1 |
| **deck** | list | [card1,card2...] | Stores the main deck | Only contains instances of class 'card' |
| **p1_deck** | list | [card3,card4...] | Stores the cards that player 1 has | Only contains instances of class 'card', must not contain anything that's in p2_deck or deck |
| **p2_deck** | list | [card5,card6...] | Stores the cards that player 2 has | Only contains instances of class 'card', must not contain anything that's in p1_deck or deck |

