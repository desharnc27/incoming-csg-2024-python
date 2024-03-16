import commonpy.common_cst as cst

import os


def leafing(path: str, end_name: str = None):
    return path + ("" if end_name is None else os.sep + end_name)


def zero_ignore(question_id: int):
    return f"{question_id}" if question_id != 0 else ""


def hyphen_zero_ignore(question_id: int):
    return f"-{question_id}" if question_id != 0 else ""


def hyphen_zero_or_one_ignore(question_id: int):
    return f"-{question_id}" if question_id > 1 else ""


def hyphen_empty_ignore(string: str):
    return f"-{string}" if (string is not None and len(string) > 0) else ""


def pdf_name(project_name: str, lang: str):
    return f"{project_name}{hyphen_empty_ignore(lang)}.pdf"


def commonfiles_path(end_name: str = None):
    return leafing(cst.COMMONFILES, end_name)


def commonpy_path(end_name: str = None):
    return leafing(cst.COMMONPY, end_name)


def project_path(project_name, filename=None):
    return leafing(project_name, filename)


def out_path(project_name: str = None, filename: str = None):
    ans = "out"
    if project_name is not None:
        ans = project_name + os.sep + ans
    if filename is not None:
        ans = ans + os.sep + filename
    return ans


def flag_steps_name(fake: bool = False, question_id: int = 0):
    if fake:
        return cst.FLAG_STEPS_FILL_TXT.format("-fake", hyphen_zero_or_one_ignore(question_id))
    return cst.FLAG_STEPS_FILL_TXT.format("", hyphen_zero_ignore(question_id))


def flag_steps_path(project_name: str, fake: bool = False, question_id: int = 0):
    return out_path(project_name, flag_steps_name(fake, question_id))


def writeup_canevas_path():
    return commonfiles_path(cst.WRITEUP_CANEVAS)


def summary_solution_path(project_name: str, question_id=0):
    filename = cst.SUMMARY_SOLUTION_FILL.format(zero_ignore(question_id))
    return project_path(project_name, filename)


def tease_path(project_name: str, question_id=0):
    filename = cst.TEASE_FILL.format(zero_ignore(question_id))
    return project_path(project_name, filename)


def writeup_path(project_name: str, question_id: int = 0):
    filename = cst.WRITEUP_FILL.format(zero_ignore(question_id))
    return out_path(project_name, filename)


def challenge_yml_path(project_name: str, question_id: int = 0):
    filename = cst.CHALLENGE_YML_FILL.format(zero_ignore(question_id))
    return out_path(project_name, filename)


# Only used for empty projects
def answer_path(project_name: str, fake: bool = False, question_id: int = 0):
    fake_str = "-fake" if fake else ""
    return project_path(project_name, cst.EMPTY_ANSWER_FILL.format(fake_str, hyphen_zero_ignore(question_id)))
