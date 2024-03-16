# That file is aimed to validate results by testing
# (by simulating tons of games with not too big parameter values)
# It is useless to the participants
# You have to manually change import between iaccuse.cst and iaccuse.cst_big
import random
from typing import List, Tuple

from iaccuse.cst import get_question_params

NB_DRAW_AMONG: int = 0
NB_GUILTY: int = 0
NB_TURNS_ROOF: int = 0


def set_params(question_id: int):
    global NB_DRAW_AMONG
    global NB_GUILTY
    global NB_TURNS_ROOF
    NB_DRAW_AMONG, NB_GUILTY, NB_TURNS_ROOF = get_question_params(question_id)


NB_CARDS = NB_GUILTY + 2 * NB_DRAW_AMONG - 1


def make_random_guess(cleared: List[bool]) -> List[int]:
    # Inefficient implementation but we don't care since it's called once a game only
    candidates = []
    for i in range(len(cleared)):
        if not cleared[i]:
            candidates.append(i)
    random.shuffle(candidates)
    selection = candidates[:NB_GUILTY]
    selection.sort()
    return selection


def simulate_a_game() -> Tuple[bool, int]:
    # ------- Initialize ------------

    nb_total_draws = 0

    p1_cleared = [False] * NB_CARDS
    p2_cleared = [False] * NB_CARDS

    cards = [i for i in range(NB_CARDS)]

    p1_nb_uncleared = NB_CARDS
    p2_nb_uncleared = NB_CARDS

    random.shuffle(cards)
    p1_cards = cards[:NB_DRAW_AMONG - 1]
    p2_cards = cards[NB_DRAW_AMONG - 1:2 * NB_DRAW_AMONG - 1]
    guilty = cards[2 * NB_DRAW_AMONG - 1:]
    guilty.sort()

    for card in p1_cards:
        p1_cleared[card] = True
        p1_nb_uncleared = p1_nb_uncleared - 1
    for card in p2_cards:
        p2_cleared[card] = True
        p2_nb_uncleared = p2_nb_uncleared - 1

    # print(f"guilty: {guilty}")

    # ------- Play ------------

    while True:
        # # print(f"current state: {p1_nb_uncleared} vs {p2_nb_uncleared}")
        # # print(p1_cards)
        # # print(p1_cleared)
        # # print(p2_cards)
        # # print(p2_cleared)

        # p1's turn
        if p2_nb_uncleared == NB_GUILTY:
            random_guess = make_random_guess(p1_cleared)
            return random_guess == guilty, nb_total_draws

        drawn_card = p2_cards.pop(random.randrange(len(p2_cards)))
        nb_total_draws = nb_total_draws + 1
        if not p1_cleared[drawn_card]:
            p1_cleared[drawn_card] = True
            p1_nb_uncleared = p1_nb_uncleared - 1
        p1_cards.append(drawn_card)

        # p2's turn
        if p1_nb_uncleared == NB_GUILTY:
            random_guess = make_random_guess(p2_cleared)
            return random_guess != guilty, nb_total_draws

        drawn_card = p1_cards.pop(random.randrange(len(p1_cards)))
        nb_total_draws = nb_total_draws + 1
        if not p2_cleared[drawn_card]:
            p2_cleared[drawn_card] = True
            p2_nb_uncleared = p2_nb_uncleared - 1
        p2_cards.append(drawn_card)


def simulate_a_ton_of_games(nb_games: int) -> List[Tuple[bool, int]]:
    results = []
    for i in range(nb_games):
        result = simulate_a_game()
        results.append(result)
    return results


def summarize_a_ton_of_games(nb_games: int) -> Tuple[float, float, float]:
    results = simulate_a_ton_of_games(nb_games)
    nb_p1_wins = sum([result[0] for result in results])
    total_draws = sum([result[1] for result in results])
    nb_busts = sum(1 for result in results if result[1] >= NB_TURNS_ROOF)
    return nb_p1_wins / nb_games, total_draws / nb_games, nb_busts / nb_games


def main(question):
    set_params(question)
    nb_games = 100000
    av_win, av_drawing, av_bust = summarize_a_ton_of_games(nb_games)
    print(f"p1 win proportion : {av_win}")
    print(f"mean of nb of draws : {av_drawing}")
    print(f"proportion of {NB_TURNS_ROOF}-draws-reached : {av_bust}")
