---
index: 2
---
# UI Design

## Screens
``` title="Screen 1 - Welcome"
Mr Raghavan's FANTASTIC two-player card game

REMEMBER:
Red beats black, yellow beats red and black beats yellow.
Higher numbers beat lower numbers

Press enter to log in
```

``` title="Screen 2 - Authentication"
Mr Raghavan's FANTASTIC two-player card game

Enter first player's credentials
Enter second player's credentials

Invalid username or password. Try again.
Sorry, you do not have access to this game.
Success.
```

``` title="Screen 3 - Player's turn"
Mr Raghavan's FANTASTIC two-player card game

[username]'s turn.
Press ENTER to take card 

You took: '[card]'
```

``` title="Screen 4 - Results"
Mr Raghavan's FANTASTIC two-player card game

[username 1]'s card: [card]
[username 2]'s card: [card]
Winner: [winner]

[losing player] has [num] cards (0)
[winning player] has [num] cards (+2)
```

``` title="Screen 5 - Game over"
Mr Raghavan's FANTASTIC two-player card game

GAME OVER
[winning player] has won the game with [num] cards
([losing player] had [num] cards)

You are [place] in the leaderboard. Here are the top [number of results]
1 [name] [score]
2 [name] [score]
3 [name] [score]
4 [name] [score]
5 [name] [score]
```

## Validation
- Usernames and passwords must not be empty.
- Player 1 and Player 2 must have different usernames
- 'Press Enter' prompts accept any input.
- Use sanitization to prevent SQL injection through username file (as usernames and passwords are stored using SQLite)
