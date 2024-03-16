import math
from fractions import Fraction
from typing import List

from commonpy import my_utils
from iaccuse.cst import get_question_params, DYNAMIC_PROGRAMMING_USE

# In following code, most of the time:
# i is the number of clean cards that still to be discovered by player whose turn it is.
# j is the number of clean cards that still to be discovered by opponent.
#
# So probas[i][j] is the probability of p1 winning,
# assuming we are now in state (i,j)

# Sometimes i, j are instead represented by nb_i_havnt_seen, nb_you_havnt_seen

NB_DRAW_AMONG: int = 0
NB_GUILTY: int = 0
NB_TURNS_ROOF: int = 0


def set_params(question_id: int):
    global NB_DRAW_AMONG
    global NB_GUILTY
    global NB_TURNS_ROOF

    NB_DRAW_AMONG, NB_GUILTY, NB_TURNS_ROOF = get_question_params(question_id)


def create_empty_probas() -> List[List[Fraction]]:
    return [[Fraction(0, 1) for _ in range(NB_DRAW_AMONG)] for _ in range(NB_DRAW_AMONG)]


# Probability of randomly making a perfect guess if we accuse now
def guess_proba(nb_i_havnt_seen: int) -> Fraction:
    return Fraction(1, math.comb(nb_i_havnt_seen + NB_GUILTY, NB_GUILTY))


def build_probas() -> List[List[Fraction]]:
    probas = create_empty_probas()
    for i in range(NB_DRAW_AMONG):
        probas[0][i] = Fraction(1, 1)
        probas[i][0] = guess_proba(i)
    for k in range(2, 2 * NB_DRAW_AMONG - 1):
        for i in range(1, k + 1):
            j = k - i
            if i >= NB_DRAW_AMONG or j >= NB_DRAW_AMONG:
                continue
            if j == 0:
                # We must not draw because opponent found the guilty cards. We have to guess.
                probas[i][j] = guess_proba(i)
                continue
            n = NB_DRAW_AMONG  # shorten following expressions
            numer: Fraction = i * n * (1 - probas[j][i - 1]) + (n - i) * j * probas[i][j - 1]
            denom: int = n * k - i * j
            probas[i][j] = numer / denom
    return probas


# UNUSED
# Calculates a probability without keeping calculations in list for efficiency.
# So It's very inefficient. Just for testing
# Turns out it still works within seconds because parameters of Q1 are small
def blind_get_proba(i: int = NB_DRAW_AMONG, j: int = NB_DRAW_AMONG - 1) -> Fraction:
    if i == 0:
        return Fraction(1, 1)
    if j == 0:
        return guess_proba(i)
    n = NB_DRAW_AMONG  # shorten following expressions
    numer: Fraction = i * n * (1 - blind_get_proba(j, i - 1)) + (n - i) * j * blind_get_proba(i, j - 1)
    denom: int = n * (i + j) - i * j
    return Fraction(numer, denom)


# It's mostly like returning probas[nb_i_havnt_seen][nb_you_havnt_seen]
# But it covers exception cases
def get_proba(probas: List[List[Fraction]],
              nb_i_havnt_seen,
              nb_you_havnt_seen) -> Fraction:
    if nb_you_havnt_seen >= NB_DRAW_AMONG:
        raise ValueError(nb_you_havnt_seen)
    if nb_i_havnt_seen > NB_DRAW_AMONG:
        raise ValueError(nb_i_havnt_seen)
    if nb_i_havnt_seen == NB_DRAW_AMONG:
        if nb_you_havnt_seen == 0:
            return guess_proba(nb_i_havnt_seen)
        return 1 - probas[nb_you_havnt_seen][nb_i_havnt_seen - 1]
    return probas[nb_i_havnt_seen][nb_you_havnt_seen - 1]


def get_goal_proba(probas: List[List[Fraction]]) -> Fraction:
    return get_proba(probas, NB_DRAW_AMONG, NB_DRAW_AMONG - 1)


def print_details(probas: List[List[Fraction]]) -> None:
    for i in range(len(probas)):
        for j in range(len(probas[i])):
            print("P[{},{}]={}={}".format(i, j, probas[i][j], float(probas[i][j])))


def main(question: int) -> Fraction:
    set_params(question)
    proba: Fraction
    if DYNAMIC_PROGRAMMING_USE:
        probas = build_probas()
        proba = get_goal_proba(probas)
        # print_details(probas)
    else:
        proba = blind_get_proba()
    print("Initial state probability of first player winning: ")
    print(f"proba: {proba} = {float(proba)}")
    print(my_utils.my_flag(str(proba)))

    return proba
