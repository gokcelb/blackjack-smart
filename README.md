# BlackjackSmart

This CLI blackjack game initially has two smart AIs joining you in your game. Their bet rates are random but their moves are not.
They actually play according to _Perfect Blackjack Strategy_, which is apparently a thing... There is no doubling or splitting at the moment. There are only two possible actions for all players (the ais and you): hit or stay.

The AIs and you have a starting fund of $500. When you run out of money, you can't play anymore and the same goes for the AIs. It's quite fun even though it's a fairly basic version of Blackjack, so I encourage you to give it a go!

## Preview

### Example Round 1

In this example, the dealer busts, which is good news for everybody because everybody wins their bet's value. If a player busts though, the player that busts loses their bet, and other players have their bets returned to them. Whether a player has busted or not is calculated immediately after they are dealt a card, so the player that plays first is the most disadvantaged.

```
You are starting with $500. Would you like to play a hand? yes
player1 has entered the game
player2 has entered the game
. . .
player1 has betted $300.0
. . .
player2 has betted $333.33
. . .
Place your bet: $300
. . .
player1: K♦, 4♦
. . .
player2: K♣, T♣
. . .
you: 5♣, 7♥
. . .
The dealer is dealt: A♠, Unknown
. . .
. . .
player1 hits and is dealt: 3♠
player1: K♦, 4♦, 3♠
. . .
player1 stays.
. . .
player2 stays.
Would you like to hit or stay? hit
you: 5♣, 7♥, 4♣
. . .
Would you like to hit or stay? stay
dealer: A♠, 3♦
. . .
The dealer hits and is dealt: Q♠
dealer: A♠, 3♦, Q♠
. . .
The dealer hits and is dealt: A♦
dealer: A♠, 3♦, Q♠, A♦
. . .
The dealer hits and is dealt: 7♠
dealer: A♠, 3♦, Q♠, A♦, 7♠
The dealer busts, you all win
player1 wins $300.0.
player2 wins $333.33.
you win $300.
```

### Example Round 2

In this example, player 1 gets a natural. When someone gets a natural, they win 1.5 times their bet. The other players' hand value is calculated and compared against the dealer's hand value. If they have a bigger value than the dealer, they win; if they have the same value, they tie; and if they have a smaller value, they lose.

```
You are starting with $450.0. Would you like to play a hand? yes
player1 has entered the game
player2 has entered the game
. . .
player1 has betted $32.0
. . .
player2 has betted $1822.91
. . .
Place your bet: $300
. . .
player1: K♠, A♥
. . .
player2: 7♥, K♥
. . .
you: Q♥, 4♠
. . .
The dealer is dealt: T♣, Unknown
. . .
Blackjack! player1 wins $48.0
dealer: T♣, K♦
The dealer wins, player2 loses $1822.91.
The dealer wins, you lose $300.
```

Example Round 3

In the previous round, player2 had betted their entire funds and so they can't join this round, only player1 and you play.

```
You are starting with $150.0. Would you like to play a hand? yes
player1 has entered the game
. . .
player1 has betted $74.67
. . .
Place your bet: $50 
. . .
player1: 6♦, 3♥
. . .
you: J♣, 8♠
. . .
The dealer is dealt: Q♠, Unknown
. . .
. . .
player1 hits and is dealt: 9♣
player1: 6♦, 3♥, 9♣
. . .
player1 stays.
Would you like to hit or stay? stay
dealer: Q♠, Q♣
. . .
The dealer stays.
The dealer wins, player1 loses $74.67.
The dealer wins, you lose $50.
```