import math
from fractions import Fraction
import random
from typing import List, Tuple

from commonpy import my_utils
from zscorescam.cst import INPUT_PATH, INPUT_FILENAME, LBERNARD, PROJECT as PJ, MINI_STEP_ALGO


# General comments
# 1: Please read the theory on the solution file first
# 2: Notes are multiplied by 100 through during calculations, so we can work with integers.
#   Ex: 65.73% becomes 6573
# 3: Way less code was needed by participants. The optimal solution turns out to be a hard
#   floor (raise all notes below that floor to the floor) rather than being a
#   soft floor (more complicated), requiring to choose how many results we want to raise to
#   floor + 1 rather than floor.
#   In practical terms, inside optimize_cote_z(...) [see below], a participant could stop coding
#   after find_approx_flor(...) is called because the latter already returns the optimal solution, luckily.
#   The additional code serves safety, because the step above is not theoretically 100% safe.
#   As a result, the complicated optimize_cote_z_from_floor(...) was not needed by the participant.

def note_to_int(note: str) -> int:
    return int(''.join(filter(str.isdigit, note)))


# Returns the sum and the sum of squares of a list of integers
def create_summary(tricked_notes: List[int]) -> Tuple[int, int]:
    sum_notes = sum(tricked_notes)
    sum_square_notes = sum([r * r for r in tricked_notes])
    return sum_notes, sum_square_notes


# Returns z2, the square of the z-score of a note, using summary of data
def compute_z2_with_summary(note: int, n: int, sum_notes: int, sum_square_notes: int) -> Fraction:
    # Might seem weird calculations, but if you do the algebra on paper,
    # you will find that these calculations give the correct result.
    numer = n * note - sum_notes
    numer = numer * numer
    denom = n * sum_square_notes - sum_notes * sum_notes
    return Fraction(numer, denom)


# Returns z2, the square of the z-score of a note, using detailed data
def compute_z2_with_data(note_idx: int, tricked_notes: List[int]) -> Fraction:
    sum_notes, sum_square_notes = create_summary(tricked_notes)
    return compute_z2_with_summary(tricked_notes[note_idx], len(tricked_notes), sum_notes, sum_square_notes)


# Computes z2 after applying a hard floor, which means that all notes below
# that floor will be raised to that floor specifically.
# Note: this is different from other functions using soft floor (raising to floor or floor + 1)
def compute_z2_with_hard_floor(note_idx: int, initial_notes: List[int],
                               floor: int) -> Fraction:
    n = len(initial_notes)
    sum_notes = 0
    sum_square_notes = 0
    for i in range(n):
        idx = n - 1 - i
        if initial_notes[idx] > floor:
            sum_notes = sum_notes + initial_notes[idx]
            sum_square_notes = sum_square_notes + initial_notes[idx] * initial_notes[idx]
        else:
            sum_notes = sum_notes + (idx + 1) * floor
            sum_square_notes = sum_square_notes + (idx + 1) * floor * floor
            break
    return compute_z2_with_summary(initial_notes[note_idx], n, sum_notes, sum_square_notes)


# Finds an approximative hard floor
def find_approx_floor(bern_idx: int, initial_notes: List[int]) -> int:
    left = initial_notes[0]
    right = initial_notes[bern_idx]
    while left < right:
        mid = left + (right - left) // 2
        if compute_z2_with_hard_floor(bern_idx, initial_notes, mid) < \
                compute_z2_with_hard_floor(bern_idx, initial_notes, mid + 1):
            left = mid + 1
        else:
            right = mid

    return left


# Optimizes cote_z by working with a specific soft floor
# All modified notes must be set to floor or floor + 1 for reasons explained in theory file.
def optimize_cote_z_from_floor(target_idx: int, initial_notes: List[int],
                               floor: int) -> List[int]:
    n = len(initial_notes)
    notes_copy = initial_notes[:]
    target_note = initial_notes[target_idx]
    stop_buffer = target_idx
    for idx in range(target_idx):
        if notes_copy[idx] < floor + 1:
            notes_copy[idx] = floor + 1
        else:
            stop_buffer = idx
            break

    sum_notes, sum_square_notes = create_summary(notes_copy)

    best_z2 = compute_z2_with_summary(target_note, n, sum_notes, sum_square_notes)
    best_jump_idx = 0
    square_jump = 2 * floor + 1
    for jump_idx in range(1, stop_buffer + 1):
        sum_notes = sum_notes - 1
        sum_square_notes = sum_square_notes - square_jump
        # notes_copy[jump_idx - 1] = notes_copy[jump_idx - 1] - 1
        z2 = compute_z2_with_summary(target_note, n, sum_notes, sum_square_notes)
        if z2 > best_z2:
            best_z2 = z2
            best_jump_idx = jump_idx

    notes_copy = list(initial_notes)
    for idx in range(best_jump_idx):
        notes_copy[idx] = floor
    for idx in range(best_jump_idx, stop_buffer):
        notes_copy[idx] = floor + 1

    # Test be sure nothing is wrong
    z2_validation = compute_z2_with_data(target_idx, notes_copy)
    if best_z2 != z2_validation:
        print("Warning: z2 failed validations, mistakes in calculations likely")
        print("{0} vs {1}".format(best_z2, z2_validation))

    return notes_copy


# Finds the modification of notes that optimizes LilyBern's z-score
# Returns the list of optimally modified notes
def optimize_cote_z(bern_idx: int, initial_notes: List[int]) -> List[int]:
    n = len(initial_notes)
    print("Lily ranking {} of {}".format(n - bern_idx, n))
    floor_approx = find_approx_floor(bern_idx, initial_notes)

    best_solution = initial_notes[:]
    best_floor = 0
    best_z2 = compute_z2_with_data(bern_idx, initial_notes)
    print("Initial z2: {}".format(float(best_z2)))
    print("Initial z: {}".format(math.sqrt(float(best_z2))))

    # We want to look around the approximate floor to be sure
    for temp_floor in range(floor_approx - 2, floor_approx + 2):
        best_solution_for_that_floor = optimize_cote_z_from_floor(bern_idx,
                                                                  initial_notes,
                                                                  temp_floor)
        temp_z2 = compute_z2_with_data(bern_idx, best_solution_for_that_floor)
        if best_z2 <= temp_z2:
            best_z2 = temp_z2
            best_floor = temp_floor
            best_solution = best_solution_for_that_floor

    print(f"best_floor: {best_floor}")
    print(f"best_z2: {float(best_z2)}")
    print(f"best_z: {math.sqrt(float(best_z2))}")
    return best_solution


def main():
    profiles: List[str]

    # Load profiles
    with open(INPUT_PATH, 'r') as file:
        default_answer = file.read()
        profiles = default_answer.split(",")
        PJ.put_flag_steps_in_file(default_answer, real_answer=False, use_sha1=True)

    print("original data:" + profiles.__str__())

    n = len(profiles)
    names_and_notes: List[List[str]] = [line.split(":") for line in profiles]
    names: List[str] = [line[0] for line in names_and_notes]
    notes: List[int] = [note_to_int(line[1]) for line in names_and_notes]

    bern_idx: int = names.index(LBERNARD)

    # It's easier to work with notes in ascending order, so:
    sorted_notes, tracking = my_utils.sort_with_indices(notes)
    # tracking[i] is the before-sorting position of what's at index i after-sorting,

    sorted_bern_idx: int = tracking.index(bern_idx)

    if MINI_STEP_ALGO:
        # MINI_STEP_ALGO on this dataset does NOt work since it gets stuck in a local maximum (not global maximum)
        # Many teams fell in this trap and got a hard floor of 84.08%
        print(f"MINISTEPALGO solution: {optimize_cote_z_with_ministepsalgo(sorted_bern_idx, sorted_notes)}")
    tricked_notes: List[int] = optimize_cote_z(sorted_bern_idx, sorted_notes)
    print(f"valid solution: {tricked_notes}")

    # Put back the notes in alphabetic order of students
    remapped_notes: List[int] = my_utils.restore_to_original_order(tricked_notes, tracking)

    def temp_profile_maker(i: int) -> str:
        note_str = str(remapped_notes[i])
        note_percent = note_str[:2] + "." + note_str[2:] + "%"
        return names[i] + ":" + note_percent

    out_profiles = [temp_profile_maker(i) for i in range(n)]

    answer = ",".join(out_profiles)

    # Store flag steps
    PJ.put_flag_steps_in_file(answer,
                              real_answer=True,
                              use_sha1=True)
    # That's for the CSGames CO
    flag = my_utils.my_sha1_flag(answer)

    PJ.make_writeup(flag, 2024)
    PJ.make_challenge_yml(flag, [INPUT_FILENAME])
    # make_info_co_file(sha1_answer)


################################################################################

# ----------------- Everything below is not needed by participants -------------


# begin ------- Only for testing, not used for solving --------

def apply_hard_floor_on_notes(initial_notes: List[int], hard_floor):
    return [note if note > hard_floor else hard_floor for note in initial_notes]


def validate_hard_floor_z2_calculation(initial_notes: List[int], hard_floor, note_idx):
    tricked_notes = apply_hard_floor_on_notes(initial_notes, hard_floor)
    res_safe = compute_z2_with_data(note_idx, tricked_notes)
    res = compute_z2_with_hard_floor(note_idx, initial_notes, hard_floor)
    print(res)
    print(res_safe)


def validations():
    temp = 0
    initial_notes = [0]
    nb_notes = 75
    for _ in range(nb_notes - 1):
        temp = temp + random.randint(1, 7)
        initial_notes.append(temp)
    target_idx = int(0.8 * nb_notes)
    floor = initial_notes[int(0.6 * nb_notes)]
    validate_hard_floor_z2_calculation(initial_notes, floor, target_idx)


# end --------- Only for testing, not used for solving --------

# begin ------- Naive convergent method --------


# This might NOT work since it can get stuck in a local maximum (not global maximum)
def optimize_cote_z_with_ministepsalgo(target_idx, initial_notes):
    notes = initial_notes[:]
    summ, sum_sq = create_summary(notes)
    n = len(notes)
    target_note = notes[target_idx]
    while True:
        change = False
        z2 = compute_z2_with_summary(target_note, n, summ, sum_sq)
        for i in range(target_idx):
            for sg in (1, -1):
                if (notes[i] < notes[i + 1] and sg == 1) or (
                        sg == -1 and notes[i] > notes[i - 1] and notes[i] > initial_notes[i]):
                    # Check if  changing ith grade by 1 improves z score
                    new_sum = summ + sg
                    new_sum_sq = sum_sq + notes[i] * 2 * sg + 1
                    new_z2 = compute_z2_with_summary(target_note, n, new_sum, new_sum_sq)
                    if new_z2 > z2:
                        # Apply change
                        z2 = new_z2
                        summ = new_sum
                        sum_sq = new_sum_sq
                        notes[i] = notes[i] + sg
                        change = True
                        # No reason to try opposite sign
                        continue
        if not change:
            # z2 can't be improved from here by changing only one note
            # We are in local optimum, let's hope it's global optimum
            return notes

# end --------- Naive convergent method --------
