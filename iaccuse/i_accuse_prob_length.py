from fractions import Fraction
from typing import List

from commonpy import my_utils
from iaccuse.cst import get_question_params, DYNAMIC_PROGRAMMING_USE

# In following code, most of the time:
# i is the number of clean cards that still to be discovered by player whose turn it is.
# j is the number of clean cards that still to be discovered by opponent.
# k is a specific number of turns
#
# So probas[k][i][j] is the probability that the rest of the game will take exactly k draws,
# assuming we are now in state (i,j)

NB_DRAW_AMONG: int = 0
NB_GUILTY: int = 0
NB_TURNS_ROOF: int = 0


def set_params(question_id: int):
    global NB_DRAW_AMONG
    global NB_GUILTY
    global NB_TURNS_ROOF
    NB_DRAW_AMONG, NB_GUILTY, NB_TURNS_ROOF = get_question_params(question_id)


def create_empty_probas(nb_turns_roof: int) -> List[List[List[Fraction]]]:
    return [[[Fraction(0, 1) for _ in range(NB_DRAW_AMONG)]
             for _ in range(NB_DRAW_AMONG + 1)]
            for _ in range(nb_turns_roof)]


def build_probas(nb_turns_roof: int) -> List[List[List[Fraction]]]:
    probas = create_empty_probas(nb_turns_roof)

    for k in range(nb_turns_roof):
        for i in range(NB_DRAW_AMONG + 1):
            for j in range(NB_DRAW_AMONG):

                if i == 0 or j == 0:
                    # If you know or the opponent knows, you have to accuse right away
                    # So no more draws will be done
                    probas[k][i][j] = Fraction(1 if k == 0 else 0, 1)
                elif k == 0:
                    probas[k][i][j] = Fraction(0, 1)
                else:
                    temp = i * probas[k - 1][j][i - 1]
                    if NB_DRAW_AMONG - i > 0:
                        temp = temp + (NB_DRAW_AMONG - i) * probas[k - 1][j][i]
                    probas[k][i][j] = temp / NB_DRAW_AMONG

    return probas


# UNUSED
# Calculates a probability without keeping calculations in list for efficiency.
# So It's very inefficient. Just for testing
# Obviously with Q2 parameters, calculations time explose
def get_proba(k: int, i: int, j: int) -> Fraction:
    if i == 0 or j == 0:
        # If you know or the opponent knows, you have to accuse right away
        # So no more draws will be done
        return Fraction(1 if k == 0 else 0, 1)
    elif k == 0:
        return Fraction(0, 1)
    else:
        temp = i * get_proba(k - 1, j, i - 1)
        if NB_DRAW_AMONG - i > 0:
            temp = temp + (NB_DRAW_AMONG - i) * get_proba(k - 1, j, i)
        return temp / NB_DRAW_AMONG


def get_bust_proba():
    prob_of_not_reaching_threshold_turn: Fraction
    if DYNAMIC_PROGRAMMING_USE:
        print(NB_DRAW_AMONG)
        print(NB_TURNS_ROOF)
        probas = build_probas(NB_TURNS_ROOF)
        prob_of_not_reaching_threshold_turn = \
            sum([probas[k][NB_DRAW_AMONG][NB_DRAW_AMONG - 1] for k in range(NB_TURNS_ROOF)])
    else:
        prob_of_not_reaching_threshold_turn = \
            sum([get_proba(k, NB_DRAW_AMONG, NB_DRAW_AMONG - 1) for k in range(NB_TURNS_ROOF)])

    return 1 - prob_of_not_reaching_threshold_turn


def main(question) -> Fraction:
    set_params(question)
    bust_prob = get_bust_proba()

    print(f"Prob of reaching {NB_TURNS_ROOF} :{bust_prob} = {float(bust_prob)}")
    print(my_utils.my_flag(str(bust_prob)))
    """
    my_utils.put_flag_steps_in_file(PROJECT.path(), str(bust_prob),
                                    real_answer=True,
                                    use_sha1=False,
                                    question_detail=2)
    """
    return bust_prob
