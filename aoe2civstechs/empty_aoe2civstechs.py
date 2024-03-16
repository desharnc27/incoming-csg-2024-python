from commonpy import my_utils, path_making
from aoe2civstechs.cst import PROJECT as PJ


def make_fake_flag(question_id: int):
    answer = my_utils.read_from_path(path_making.answer_path(PJ.name(),
                                                             fake=True,
                                                             question_id=question_id))
    PJ.put_flag_steps_in_file(answer,
                              real_answer=False,
                              use_sha1=True,
                              question_detail=question_id)


def make_files_for_question(question_id: int):
    """
    my_utils.make_writeup(PROJECT_PATH,
                          TITLES[question_id - 1],
                          FLAGS[question_id - 1],
                          2024,
                          question_id=question_id)
    my_utils.make_challenge_yml(PROJECT_PATH,
                                PROJECT_NAME,
                                TITLES[question_id - 1],
                                FLAGS[question_id - 1],
                                TAGS,
                                [] if question_id < 2 else ["flag-steps-fake-2.txt"],
                                question_id=question_id)
    """

    answer = my_utils.read_from_path(path_making.answer_path(PJ.name(), False, question_id))
    PJ.put_flag_steps_in_file(answer,
                              real_answer=True,
                              use_sha1=True,
                              question_detail=question_id)
    flag = my_utils.my_sha1_flag(answer)
    PJ.make_writeup(flag, 2024, question_id, "java")
    PJ.make_challenge_yml(flag, [],
                          bilingual_pdfs=True,
                          question_id=question_id)


def main_empty():
    for q in (1, 2):
        make_fake_flag(q)
        make_files_for_question(q)
