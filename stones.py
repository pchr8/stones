# Implementation of the 3 stones game, as described by O.K.
# This file contains the basic classes
# Serhii Hamotskyi, Wed 06 Feb 2019 11:09:21 AM CET

import random
random.seed(42)

class Player:
    """ Each player has stones and a strat.
    """
    def __init__(self, strat='random'):
        """ Initialize instance attributes
        """
        self.stones=3;
        self.strat=strat

    def play(self):
        """ Puts stones in the hand.
        """
        if (self.strat=='random'):
            return random.randint(0, self.stones);

    def guess(self, nstones_played,  nstones_opp):
        """ Guess the sum of the stones
        """
        if (self.strat=='random'):
            return random.randint(nstones_played, nstones_played+nstones_opp);

class Game:
    """ A single game
    """
    def __init__(self, turns, p1, p2):
        self.turns=turns;
        self.p1=p1
        self.p2=p2
        print("Initialized game with ", self.turns ," turns between players ",self.p1.strat," and ",self.p2.strat)

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








