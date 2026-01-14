# Design overview
The program will run a two-player card game between two authorised users. The deck is composed of thirty cards with a colour (red, yellow or black) and a number. Cards are numbered from 1 to 10 with three instances of each number, one of each colour. The deck is shuffled, then on every round each player takes the top card from the deck. If the colours are different, red beats black, yellow beats red and black beats yellow. If the colours are the same, the highest number wins. The player with the winning card takes both. The objective is to get the most cards. When the deck is exhausted, the game ends and the player with the most cards wins. The winner's name and card count are stored to a file, and the top 5 players by card count are displayed.

## Assumptions
- Cards are not dealt to players. Instead, they take the top card from the main deck.
- Player 1 always picks their card first, followed by Player 2.
- Authentication is by username and password (hashed) against a stored allow list.
- Leaderboard file stores all winners while the top 5 (most cards) are displayed **at the end of a round**.

``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```