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
        """
        self.allstones=stones;
        self.stones=stones;
    
    def reset(self):
        """ Resets player's stones stones to the default max
        """
        self.stones=self.allstones;
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
    def tellsum(self, sumstones):
        """ Tells the player the real sum
        """
        pass
    def tellguess(self, sumstones):
        """ Tells the player the real sum
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
        self.allstones=stones;
        self.stones=stones;
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
    """
    strat='memory'

    def __init__(self, stones=3):
        """ Initialize instance attributes
            allstones -- how many stones in general
            stones -- how many it has right now
            memory -- a more structured memory with the following format:
                [mymove, hismove, hisavailable, hisguessed]
        """
        self.allstones=stones;
        self.stones=stones;
        self.memory = [];
    
    def full_reset(self):
        """ Resets player's memory and knowledge of the opponent/s, 
            if he has one.
        """
        self.memory=[];
    def dump_memory(self):
        """ Outputs the content of its memory on the screen
        """
        print("Dumping raw memory");
        print("[mymove, hismove, hisavailable, hisguessed]");
        for i in self.memory:
            print(i);

    def memorize(self, what, n):
        """ Function to memorize "what" as the number "n"
        """
        if what=="mymove":
            self.memory.append([n, "0", "0", "0"])
        if what=="nstones_opp":
            self.memory[-1][2]=int(n);
        if what=="hismove":
            self.memory[-1][1]=int(n-self.memory[-1][0]);
        if what=="hisguess":
            self.memory[-1][3]=int(n);

    def play(self):
        """ Puts stones in the hand.
        """
        number = random.randint(0, 1);
        self.memorize("mymove", number)
        return number;

    def guess(self, nstones_played,  nstones_opp):
        """ Guess the sum of the stones
        """
        self.memorize("nstones_opp", nstones_opp);
        return random.randint(0, 1);
    def tellsum(self, sumstones):
        """ Tells the player the real sum
        """
        
        #Gets calculated in memorize()!
        self.memorize("hismove", sumstones)

    def tellguess(self, guess):
        """ Tells the player the guess of the other opponent
        """
        self.memorize("hisguess", guess)
class AveragePlayer(MemoryPlayer):
    """ Uses the opponents average stones as prediction
    """
    strat='average'

    def __init__(self, stones=3, startnumber=1):
        """ Initialize instance attributes
            allstones -- how many stones in general
            stones -- how many it has right now
            memory -- a more structured memory with the following format:
                [mymove, hismove, hisavailable, hisguessed]
            startnumber -- before we get an average, what number should it guess the opponent will use
        """
        self.allstones=stones;
        self.stones=stones;
        self.memory = [];
        self.startnumber=startnumber;

    def play(self):
        """ Puts stones in the hand, like RandomPlayer
        """
        number = random.randint(0, self.stones);
        self.memorize("mymove", number)
        return number;

    def guess(self, nstones_played,  nstones_opp):
        """ Guess the sum of the stones
            We try to guess the opponent's move by taking an average of all his moves.
            TODO -- make the memorization of stuff more logical. The fact that this function gets nstones_opp doesn't mean this is the best place to memorize it.
        """

        self.memorize("nstones_opp", nstones_opp)

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

        return myguess;

class Round:
    """ A single game, played until one of the players has no more stones left.
        stalemate_limit -- how many times does a stalemate have to occur, both inside turns and rounds, until it renders them invalid. 
    """
    def __init__(self, p1, p2, stalemate_limit=5):
        self.p1=p1
        self.p2=p2
        self.stale_steps=0;
        self.stalemate_limit=stalemate_limit;
        print("Initialized round between players ",self.p1.strat," and ",self.p2.strat)

    def play_turn(self):
        p1stones=self.p1.play();
        p2stones=self.p2.play();
        sumstones=p1stones+p2stones;
        self.stale_steps+=1;

        p1guess=self.p1.guess(p1stones, self.p2.stones);
        p2guess=self.p2.guess(p2stones, self.p1.stones);

        print("p1 played:", p1stones, "/", self.p1.stones)
        print("p2 played:", p2stones, "/", self.p2.stones);
        print("Sum is", sumstones);

        print("p1 guessed", p1guess);
        print("p2 guessed", p2guess);

        self.p1.tellsum(sumstones)
        self.p2.tellsum(sumstones)
        self.p1.tellguess(p2guess)
        self.p2.tellguess(p1guess)

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
            self.results.append(r.start_round())

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
