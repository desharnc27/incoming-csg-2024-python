from commonpy.project import Project

# ---------- You can modify --------


DYNAMIC_PROGRAMMING_USE = True
# ROOT = ""  # Modify if it does not work, but it should already work

# ---------- Do Not touch ---------
"""
PROJECT_NAME = "iaccuse"
PROJECT_PATH = PROJECT_NAME if ROOT == "" else ROOT + os.sep + PROJECT_NAME

TITLE = "I accuse!, part {}"
TAGS = ["mathematics", "probability"]

"""

PROJECT = Project(name="iaccuse",
                  titles=[f"I accuse!, part {i}" for i in (1, 2)],
                  tags=["mathematics", "probability"])


def get_question_params(question: int):
    if question == 1:
        return 6, 2, 20
    elif question == 2:
        return 12, 3, 50
    else:
        return 4, 2, 20
