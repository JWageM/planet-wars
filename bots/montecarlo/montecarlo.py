#Coded is based on or taken over from: https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/



#!/usr/bin/env python

"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one 
uniformly at random.
"""

# Import the API objects
from api import State
import random
import datetime


class Bot:

    def __init__(self):
        self.calculation_time = datetime.timedelta(seconds=2)
        self.max_moves = 100
        self.max_turns = 100 # this has to be the same as the tournament or play.
        

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.

        Be sure to make a legal move. Illegal moves, like giving a source planet you
        don't own, will lose you the game.

        If you return a source and destination, 50% of the ships of the source
        planet (rounded down) will be sent to the destination. If that planet is
        owned by the enemy or neutral when they arrive, they will attack it, if it is
        owned by you, they will reinforce it (add to the number of ships stationed).

        :param State state: An object representing the gamestate. This includes a link to the
            map, ownership of each planet, garrisons on each plant, and all fleets in transit.

        :return: None, indicating no move is made, or a pair of integers,
            indicating a move; the first indicates the source planet, the second the
            destination.
        """

        self.wins = {}#dictionary where each state is kept as a hash, and the value is the number of wins of that state
        self.plays = {}#dictionary where each state is kept as a hash, and the value is the number of plays of that state

        self.max_depth = 0

        player = state.whose_turn()
        legal_moves = state.moves()

        #Check if there are any moves that can be made, or only None.
        if len(legal_moves) == 1: # Only move 'None' available
            return legal_moves[0]
        
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:#run simulations as long as there is time.
            self.run_simulation(state)
            games += 1
        
        moves_states = [(p, state.next(p)) for p in legal_moves]
        
        #Display the number of calls of 'run_simulation' and the time elapsed
        print games, datetime.datetime.utcnow() - begin
        
        #Pick the move with the highest percentage of wins.
#         percent_wins, move = max(
#             (self.wins.get(hash((player, S)), 0)/self.plays.get(hash((player, S)), 1), p) for p, S in moves_states # What does the ,0 do? -> Those are the default parameters.
#             
#             )
        
        best_move = moves_states[0][0]
        best_value = 0
        for p, S in moves_states:
            value = float(self.wins.get(hash((player, S)), 0))/float(self.plays.get(hash((player, S)), 1))
            if  value > best_value:
                best_value = value
                best_move = p
        move = best_move    
        
        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get(hash((player, S)), 0) /
              self.plays.get(hash((player, S)), 1),
              self.wins.get(hash((player, S)), 0),
              self.plays.get(hash((player, S)), 0), p)
             for p, S in moves_states),
            reverse=True
        ):
            print "{3}: {0:.2f}% ({1} / {2})".format(*x)

        print "Maximum depth searched:", self.max_depth        
            
        return move



#     def update(self, state):
#         # Takes a game state, and appends it to the history.
#         self.states.append(state)

    def run_simulation(self, state):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        
        states_copy = [state] # states_copy will contain all states encountered during the rollout.
        

        
        player = state.whose_turn()
        visited_states = set()
        
        expand = True #expanding the search tree
        
        
        for t in xrange(self.max_moves):
            legal_moves = state.moves()
            play = random.choice(legal_moves)#choose a move
            
            state = state.next(play)
            states_copy.append(state)
            
    
            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and hash((player, state)) not in self.plays:#does this check whether that hash is in there? -> If not I can enclose it in hash.
                expand = False
                self.plays[hash((player, state))] = 0 #Expand the node: (player, state)#here it goes wrong: it takes string instead of hash.
                self.wins[hash((player, state))] = 0
                if t > self.max_depth:
                    self.max_depth = t
                
                
                
            visited_states.add((player, state))
            
#             player = state.whose_turn() # do we use this?

#         
#             if winner:#seems wrong to me because winner is player id, or None, but no boolean.
#                 break

            if state.finished() or (self.max_turns - state.turn_nr() < 0):
                break
        
        
        winner = state.winner()#note that our implementation is diff: in their case when the game is ongoing the return is 0, here it is None
        
        
        #Perform back propagation: # it probably behaves a bit strange when there is no winner, or it will just be pesimistic.
        for player, state in visited_states:
            if hash((player, state)) not in self.plays:
                continue # When will this happen? When the node is not expanded, but is visited during a rollout.
            self.plays[hash((player, state))] +=1
            if player == winner:
                self.wins[hash((player, state))] += 1 # What about a loss, or a draw? 




