# Running this file is not necessary for participants. It's for testing.

import os

from iaccuse import i_accuse_simulator, i_accuse_prob_win, i_accuse_prob_length

question = 0
print(os.getcwd())
print("Watch out, this main only matches the parameters of one question")
print("---- Simulator -------")
i_accuse_simulator.main(question)
print("---- Theoretical P(p1 winning) -------")
i_accuse_prob_win.main(question)
print("---- Theoretical P(nb_draws >= 50) -------")
i_accuse_prob_length.main(question)
