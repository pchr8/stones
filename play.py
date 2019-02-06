from stones import *

pp = RandomPlayer();
p = RandomPlayer();
h = HumanPlayer();

p = Player();
pp = Player();

m=MemoryPlayer();

#a = AveragePlayer(stones=10);
a = AveragePlayer();
t = NumberLoverPlayer(n=0);

n=15
g=Game(a, t, n);
g.start_game()
g.print_results()

#a.dump_memory();

#r = Round(p, m);
#r.start_round();
