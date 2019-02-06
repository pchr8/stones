from stones import *

pp = RandomPlayer();
p = RandomPlayer();
h = HumanPlayer();

#p = Player(6);
#pp = Player(6);


#g=Round(p, pp);
#g.start_round();

r = Round(p, h);
r.start_round();

#n=200
#g=Game(p, pp, n);
#g.start_game()
#g.print_results()
