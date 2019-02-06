# Implementation of the 3 stones game, as described by O.K.
# This file contains the basic classes
# Serhii Hamotskyi, Wed 06 Feb 2019 11:09:21 AM CET

import random
random.seed(420)

class Player:
    """ Each player has stones.
        TODO: rewrite with getters, setters and memory-ready.
    """
    strat='basic'

    def __init__(self, stones=3):
        """ Initialize instance attributes
            allstones -- how many stones in general
            stones -- how many it has right now
        """
        self.allstones=stones;
        self.stones=stones;
    
    def reset(self):
        #print("reset number of stones");
        self.stones=self.allstones;

    def play(self):
        """ Puts stones in the hand.
        """
        return random.randint(0, 1);

    def guess(self, nstones_played,  nstones_opp):
        """ Guess the sum of the stones
        """
        return random.randint(0, 1);

class RandomPlayer(Player):
    """ Inherited from Player
        TODO: rewrite with getters, setters and memory-ready.
    """
    
    strat='random'

    def play(self):
        """ Puts stones in the hand.
        """
        return random.randint(0, self.stones);

    def guess(self, nstones_played,  nstones_opp):
        """ Guess the sum of the stones
        """
        return random.randint(nstones_played, nstones_played+nstones_opp);

class Round:
    """ A single game, played until one of the players has no more stones left.
    """
    def __init__(self, p1, p2):
        self.p1=p1
        self.p2=p2
        print("Initialized round between players ",self.p1.strat," and ",self.p2.strat)

    def play_turn(self):
        p1stones=self.p1.play();
        p2stones=self.p2.play();
        sumstones=p1stones+p2stones;

        print("p1 played:", p1stones, "/", self.p1.stones)
        print("p2 played:", p2stones, "/", self.p2.stones);
        print("Sum is", sumstones);

        p1guess=self.p1.guess(p1stones, self.p2.stones);
        p2guess=self.p2.guess(p2stones, self.p1.stones);

        print("p1 guessed", p1guess);
        print("p2 guessed", p2guess);

        if (p1guess==sumstones):
            print("p1 guessed right!");
            self.p1.stones-=1;
        if (p2guess==sumstones):
            print("p2 guessed right!");
            self.p2.stones-=1;

    def start_round(self):
        """ Starts a game until one of the two players 
        win. """

        turns=0;

        while (self.p1.stones>0) and (self.p2.stones>0):
            print();
            print("== Turn", turns, "==");
            self.play_turn();
            turns+=1;

        if self.p2.stones==0:
            print("p2 WON!")
        else:
            print("p1 WON!");

        return(turns, self.p1.stones, self.p2.stones);
            
class Game:
    """ A single game, composed of arbitrarily many Rounds
    """
    def __init__(self, p1, p2, rounds=8):
        """ Initializes a whole game of however many rounds
        """
        self.p1=p1
        self.p2=p2
        self.rounds=rounds

        self.results=[]
        print("Initialized ", self.rounds, "-round game between players ",self.p1.strat," and ",self.p2.strat)

    def start_game(self):
        for i in range(self.rounds):
            print("====")
            print(" ROUND ", i);
            print("====")
            r=Round(self.p1, self.p2);
            self.results.append(r.start_round())

            self.p1.reset();
            self.p2.reset();
    def print_results(self):
        print("=============")
        print("FINAL RESULTS")
        print("=============")
        print("turns\tp1\tp2");
        for r in self.results:
            print(str(r[0])+"\t"+str(r[1])+"\t"+str(r[2]))
        print("------------")

        tsum, p1sum, p2sum=0, 0, 0;
        for r in self.results:
            tsum+=r[0];
            p1sum+=r[1];
            p2sum+=r[2];
        print(str(tsum)+"\t"+str(p1sum)+"\t"+str(p2sum))




# TODO
# Implement some variation of the 50-steps-rule
# Ideas for players:
# guess-average-of-stones-thrown-vs-all-opp-stones
# 
