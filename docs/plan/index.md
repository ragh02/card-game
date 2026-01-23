---
index: 1
---
# Design overview
The program will run a two-player card game between two authorised users. The deck is composed of thirty cards with a colour (red, yellow or black) and a number. Cards are numbered from 1 to 10 with three instances of each number, one of each colour. The deck is shuffled, then on every round each player takes the top card from the deck. If the colours are different, red beats black, yellow beats red and black beats yellow. If the colours are the same, the highest number wins. The player with the winning card takes both. The objective is to get the most cards. When the deck is exhausted, the game ends and the player with the most cards wins. The winner's name and card count are stored to a file, and the top 5 players by card count are displayed.

## Card rules
- Red beats black (0 --> 2)
- Yellow beats red (1 --> 0)
- Black beats yellow (2 --> 1)

Internally, red is represented by 0, yellow is 1 and black is 2

## Players
- Player 1 is represented as "0"
- Player 2 is represented as "1"

## Assumptions
- 15 cards are dealt to each player. Cards are dealt by taking the top card from the main deck and dealing it normally to 
- Player 1 always picks their card first, followed by Player 2.
- Players are given the top 5 cards in the deck. They may pick one to play.
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