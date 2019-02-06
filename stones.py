# Implementation of the 3 stones game, as described by O.K.
# This file contains the basic classes
# Serhii Hamotskyi, Wed 06 Feb 2019 11:09:21 AM CET

import random
random.seed()

class Player:
    """ Each player has stones.
        Base class with simple strategy.

        TODO: rewrite with getters, setters and memory-ready.
    """
    strat='basic'

    def __init__(self, stones=3):
        """ Initialize instance attributes
            allstones -- how many stones in general
            stones -- how many it has right now
            name -- unique id
        """
        self.allstones=stones;
        self.stones=stones;
        self.name="BOT"+str(random.randint(0, 100));
        print("Hi, I'm bot "+self.name);
    
    def reset(self):
        """ Resets player's stones stones to the default max
        """
        self.stones=self.allstones;
        self.first=0;
        self.lastmoves=0;
        self.turns=-1;

    def full_reset(self):
        """ Resets player's memory and knowledge of the opponent/s, 
            if he has one.
        """
        pass

    def play(self):
        """ Puts stones in the hand.
        """
        return random.randint(0, 1);

    def guess(self, nstones_played,  nstones_opp):
        """ Guess the sum of the stones
        """
        return random.randint(0, 1);
    def decrease(self):
        """ Decreases the stones the player has by one
        """
        self.stones-=1;
    def receiveguess(self, sumstones):
        """ receive The real guess
        """
        pass
    def receivehismove(self, move):
        """ receive the opponents move
        """
        pass
    
    def receivehisstones(self, stones):
        """ Receives the number of stones the opponeent has
        """
        pass
    def won(self):
        """ Returns true if player has no stones left
        """
        return self.stones==0;

class RandomPlayer(Player):
    """ Makes random realistic predictions.
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

class OneLoverPlayer(Player):
    """ Always guesses one and puts one stone in the hand
    """
    strat="one"

    def play(self):
        """ Puts stones in the hand.
        """
        return 1;

    def guess(self, nstones_played,  nstones_opp):
        """ Guess the sum of the stones
        """
        return 1;

class NumberLoverPlayer(OneLoverPlayer):
    """ Guesses whatever number it got in the constructor
    """
    strat="number";
    def __init__(self, stones=3, n=2):
        """ Initialize instance attributes
            allstones -- how many stones in general
            stones -- how many it has right now
            n -- the number it will prefer
        """

        OneLoverPlayer.__init__(self, stones=3);
        self.n=n;

    def play(self):
        """ Puts stones in the hand.
            Whatever number it loves, but not more than it has.
        """
        if self.stones>=self.n:
            return self.n;
        else:
            return self.stones;

    def guess(self, nstones_played,  nstones_opp):
        """ Guess the sum of the stones
        """
        return self.n;

class HumanPlayer(Player):
    """ Human player
    Actions are made based on keyboard input
    TODO: input checking etc.
    """
    strat="human"

    def play(self):
        """ Puts stones in the hand.
        """
        ok=0;
        print("You have", self.stones, " stones, how many you want to use?");
        number=int(input("->"))
        return number;
    def guess(self, nstones_played, nstones_opp):
        """ Guess the sum of the stones
        """
        print("Your guess. You have", self.stones, "stones, your opponent", nstones_opp);
        guess=int(input("->"));
        return guess;

class MemoryPlayer(Player):
    """ First player with memory!
        It just remembers everyone's moves.
        Doesn't try to use them for now though.
        Also it now takes care of the last rounds and knows the numbers it can't guess
        Also it implements the receivehismove() and receiveguess()
    """
    strat='memory'

    def __init__(self, first=0, stones=3):
        """ Initialize instance attributes
            allstones -- how many stones in general
            stones -- how many it has right now
            memory -- a more structured memory with the following format:
                [mymove, hismove, hisavailable, hisguessed]
            lastmoves -- a check if we're in the last moves
            first -- whether he's the first player to play or not.
        """
        Player.__init__(self, stones);
        self.allstones=stones;
        self.stones=stones;
        self.memory = [];
        self.lastmoves=0;
        self.first = first;
    
    def full_reset(self):
        """ Resets player's memory and knowledge of the opponent/s, 
            if he has one.
        """
        self.memory=[];
    def dump_memory(self):
        """ Outputs the content of its memory on the screen
        """
        print(self.name+": Dumping raw memory");
        print("[mymove, hismove, hisavailable, hisguessed]");
        for i in self.memory:
            print(i);

    def memorize(self, what, n):
        """ Function to memorize "what" as the number "n"
        """
        if what=="mymove":
            self.memory.append([n, "0", "0", "0"])
        if what=="hisstones":
            self.memory[-1][2]=int(n);
        if what=="hismove":
            #self.memory[-1][1]=int(n-self.memory[-1][0]);
            self.memory[-1][1]=n;
        if what=="hisguess":
            self.memory[-1][3]=int(n);

    def play(self):
        """ Puts stones in the hand.
        """
        self.turns+=1
        number = random.randint(0, 1);
        self.memorize("mymove", number)
        return number;

    def currentTurn(self):
        """ Returns the number of the current turn, used for priority
        """
        return(len(self.memory));

    def guess(self):
        """ Guess the sum of the stones
        """

        return random.randint(0, 1);

    def decrease(self):
        """ Decreases the stones the player has by one
            This version with memory check for lastmoves
        """
        self.stones-=1;
        if self.stones<2:
            self.lastmoves=1;

    def receiveguess(self, guess):
        """ tells the guess of the other opponent
        """
        self.memorize("hisguess", guess)
    def receivehismove(self, move):
        """ receives the move of the other opponent
        """
        self.memorize("hismove", move);
    def receivehisstones(self, stones):
        """ Receives the number of stones the opponent has
        """
        self.memorize("hisstones", stones);
        if stones<2:
            self.lastmoves=1;

class AveragePlayer(MemoryPlayer):
    """ Uses the opponents average stones as prediction
    """
    strat='average'

    def __init__(self, stones=3, first=0, startnumber=1):
        """ Initialize instance attributes
            startnumber -- before we get an average, what number should it guess the opponent will use
        """
        MemoryPlayer.__init__(self, first, stones);
        self.startnumber=startnumber;

    def play(self):
        """ Puts stones in the hand, like RandomPlayer
        """
        self.turns+=1
        number = random.randint(0, self.stones);
        self.memorize("mymove", number)
        self.dump_memory();
        return number;

    def guess(self, nstones_played,  nstones_opp):
        print("I'm "+self.name+" and first/turn is ", self.first, self.turns);
        """ Guess the sum of the stones
            We try to guess the opponent's move by taking an average of all his moves.
        """

        # Calculate the average of all the moves of the opponent till now
        mymove=self.memory[-1][0];
        opponent_sum=0;
        
        #If it's the first guess, assume the opponent will use self.startnumber, otherwise count the average of his moves
        if (len(self.memory)==1):
            opponent_average=self.startnumber;
        else:
            for i in self.memory:
                opponent_sum+=int(i[1]);
            opponent_average=opponent_sum/(len(self.memory)-1);
        myguess=int(opponent_average+mymove);
        #print("My current guess for the opponent average is", opponent_average);

        # Now let's take care of turns!

        if self.lastmoves:
            if (self.currentTurn()%2==0 and self.first==0) or (self.currentTurn()%2==1 and self.first==1):
                if myguess==self.memory[-1][2]:
                    print(self.name, ": I think I'm going to need to change from", myguess);
                    myguess+=1;

        return myguess;

class Round:
    """ A single game, played until one of the players has no more stones left.
        stalemate_limit -- how many times does a stalemate have to occur, both inside turns and rounds, until it renders them invalid. 
        turns -- how many turns are we into, used to decide who guesses first.
    """
    def __init__(self, p1, p2, stalemate_limit=5):

        self.p1=p1
        self.p2=p2

        self.p1.reset();
        self.p2.reset();

        self.p1.first=1;

        self.stale_steps=0;
        self.stalemate_limit=stalemate_limit;
        self.turns=0;
        print("Initialized round between players ",self.p1.strat," and ",self.p2.strat)

    def play_turn(self):
        
        # We're actually missing some pieces of crucial info. When the first player guesses, it's info available to the second one for decision-making (that's one), and it's info which controls second's player choices if we're at the last rounds. I need to fix this.

        #I'll start by implementing an order

        self.turns+=1;
        
        p1stones=self.p1.play();
        p2stones=self.p2.play();

        self.p1.receivehismove(p2stones);
        self.p2.receivehismove(p1stones);
        self.p1.receivehisstones(self.p2.stones);
        self.p2.receivehisstones(self.p1.stones);

        sumstones=p1stones+p2stones;
        self.stale_steps+=1;

        lastmoves=(self.p1.stones==1 or self.p2.stones==1);
        if lastmoves:
            print("LAST TURNS");

        if self.turns%2==0:
            p1guess=self.p1.guess(p1stones, p2stones);
            self.p2.receiveguess(p1guess)

            p2guess=self.p2.guess(p2stones, p1stones);
            if (lastmoves and p2guess==p1guess):
                print("ILLEGAL MOVE, p2 ["+self.p2.name+"]!")
                p2guess+=1;
                print(p2guess, "for you instead of ", p2guess-1)
            self.p1.receiveguess(p2guess)

        else:
            p2guess=self.p2.guess(p2stones, p1stones);
            self.p1.receiveguess(p2guess)

            p1guess=self.p1.guess(p1stones, p2stones);
            if (lastmoves and p2guess==p1guess):
                print("ILLEGAL MOVE, p1 ["+self.p1.name+"]!")
                p1guess+=1;
                print(p1guess, "for you instead of ", p1guess-1)
            self.p2.receiveguess(p1guess)

        print("p1 ["+self.p1.name+"] played:", p1stones, "/", self.p1.stones)
        print("p2 ["+self.p2.name+"] played:", p2stones, "/", self.p2.stones);
        print("Sum is", sumstones);

        print("p1 ["+self.p1.name+"] guessed", p1guess);
        print("p2 ["+self.p2.name+"] guessed", p2guess);

        if (p1guess==sumstones):
            print("p1 guessed right!");
            self.p1.decrease();
            self.stale_steps=0;
        if (p2guess==sumstones):
            print("p2 guessed right!");
            self.stale_steps=0;
            self.p2.decrease();

        if self.stale_steps>self.stalemate_limit:
            return 'stale';

    def start_round(self):
        """ Starts a game until one of the two players 
        win. """

        turns=0;
        stales=0;
        valid=1;

        while not (self.p1.won() or self.p2.won() or stales>=self.stalemate_limit):
            print();
            print("== Turn", turns, "==");
            result=self.play_turn();
            if result=="stale":
                stales+=1;
            turns+=1;

        if self.p2.won():
            print("p2 WON!")
        elif self.p1.won():
            print("p1 WON!");
        else:
            print("STALEMATE");
            valid=0;

        return(turns, self.p1.stones, self.p2.stones, valid);
            
class Game:
    """ A single game, composed of arbitrarily many Rounds
    """
    def __init__(self, p1, p2, rounds=8, stalemate_limit=5):
        """ Initializes a whole game of however many rounds
        """
        self.p1=p1
        self.p2=p2
        self.rounds=rounds
        self.stalemate_limit=stalemate_limit;

        self.results=[]
        print("Initialized ", self.rounds, "-round game between players ",self.p1.strat," and ",self.p2.strat)

    def start_game(self):
        for i in range(self.rounds):
            print("====")
            print(" ROUND ", i);
            print("====")
            r=Round(self.p1, self.p2, stalemate_limit=self.stalemate_limit);
            self.results.append(r.start_round()) #TODO add dynamically changing first/round!

            self.p1.reset();
            self.p2.reset();

    def print_results(self):
        """ Prints the results.
            If valid=0 will print a "-" instead of the remaining points
            and won't count them as the sum.
        """
        print("=============")
        print("FINAL RESULTS")
        print("=============")
        print("turns\tp1\tp2");
        for r in self.results:
            if r[3]==1:
                print(str(r[0])+"\t"+str(r[1])+"\t"+str(r[2]))
            else:
                print(str(r[0])+"\t"+"-"+"\t"+"-")
        print("------------")

        tsum, p1sum, p2sum=0, 0, 0;
        for r in self.results:
            if r[3]==1:
                tsum+=r[0];
                p1sum+=r[1];
                p2sum+=r[2];
        print(str(tsum)+"\t"+str(p1sum)+"\t"+str(p2sum))

# TODO
# Ideas for players:
# guess-average-of-stones-thrown-vs-all-opp-stones
# Implement players with some basic memory?
# REWRITE __INIT__ as inheritance: https://www.python-course.eu/python3_inheritance.php
