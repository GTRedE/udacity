
## RESULTS
Here is how the three custom heuristics that I created for this project peformed against the other agents:

![results table](results.png)


### AB_Custom_3
[(link to code)](https://github.com/tommytracey/udacity/blob/master/ai-nano/projects/2-isolation/game_agent.py#L109)

This was my original exploration of heuristics that exploit board position. This function rewards moves toward the center of the board, since these squares have more legal moves available to them. Meanwhile, the function penalizes moves along the edges and corners, since these squares have fewer moves available to them. 

To achieve this, the board is divided into four sections (see diagram below).

<img src='color-board.png' width="65%"/>

The scoring logic can be summarized as follows:
- Moves in the center portion of the board (green) receive a higher score of 5 throughout the game, and a score of 10 at the beginning of the game (first seven moves)
- Moves in the second ring of the board (yellow) receive a score of 3
- Moves along the edges receive a score of 1
- Moves in the corners receive a score of 0

This heuristic does not outperform AB_Improved. However, it still managed a respectable 44% winning percentage in direct competion with AB_Improved. And, it does much better than the Random and Minimax agents, winning 80% of the time. Given these results, I continued iterating on this 'center is better' strategy and utilized elements of it when developing the subsequent function. 


### AB_Custom_2
[(link to code)](https://github.com/tommytracey/udacity/blob/master/ai-nano/projects/2-isolation/game_agent.py#L57)

This was my second attempt to exploit board position, but this time I tried to do it more systematically. The goal of this heurisitic is to reduce the mobility of the opponent &mdash; while simultaneously improving the active player's mobility. This would naturally favor positions in the middle of the board, but I wanted to get away from hard coding this into the strategy as I did previously in AB_Custom_3.

After many iterations on this concept, I eventually found a simple tactic that performed well. The final heuristic function calculates the number of available squares a player could reach within two moves (see diagram below). It then rewards moves that: (a) increase the number of reachable squares for the active player, and (b) decrease the number of squares reachable by the opponent. 

<img src='empty-spaces.png' width="65%"/>

This heuristic peforms as well as AB_Improved, maybe slightly better. However, after much testing, I wasn't able to consistently beat the AB_Improved heuristic by a significant margin. So, I concluded that since the game of Isolation is won by the player who makes the most moves, that focusing on the number of moves remaining (not the number of open spaces) would be the best avenue to pursue if I wanted get over the hump. 

### AB_Custom
[(link to code)](https://github.com/tommytracey/udacity/blob/master/ai-nano/projects/2-isolation/game_agent.py#L13)

If you can't beat 'em, join 'em. After many different permutations, my final AB_Custom heuristic is essentially an improved version of AB_Improved, but there is one big difference. The AB_Custom heuristic consistently adjusts its tactics throughout the match.

In the beginning of the match, the function is more aggresive at reducing the number of opponent moves. But, as the game goes on, it becomes less concerned with minimizing opponent moves, and becomes increasingly aggressive at maximizing the active player's moves. To me this made intuitive sense, since you want to limit your opponent's options as much as possible in the beggining of the match, but at some point you have to focus on creating the longest string of moves possible for yourself. 

You can see in the code snippet below that this is accomplished using a weight that is inversely proportional to the number of the moves in the match. This approach consistently outperformed AB_Improved, winning 73.3% of its matches (compared to 69.7% by AB_Improved).

```python

    # get current move count
    move_count = game.move_count

    # count number of moves available
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # calculate weight
    w = 10 / (move_count + 1)

    # return weighted delta of available moves
    return float(own_moves - (w * opp_moves))

```
---
