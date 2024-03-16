import os

PUBLIC_GIT = "https://github.com/desharnc27/incoming-csg-{0}-{1}"
PUBLIC_GIT_PYTHON = PUBLIC_GIT.format("{0}", "python")

DEFAULT_AUTHOR = "desharnc27"

# SEE_IN_PDF = "Full description is in pdf. "
# SEE_IN_PREVIOUS_PDF = "See pdf of first challenge, it also contains this challenge's description. "

TOUGH_MATHS = "That's a hard mathematic challenge, but if you are the only one to solve it, that's a lot of points $$$."

TRUE_STORY = "Closely related to a true story."

BARE_REQUIREMENT_FILE = "bare-requirement{}.txt"
DESC_IN_PDF = "Full description is in pdf. "

COMMONFILES = "commonfiles"
COMMONPY = "commonpy"

FLAG_STEPS_FILL_TXT = "flag-steps{0}{1}.txt"
WRITEUP_CANEVAS = "writeup-canevas.md"
WRITEUP_CANEVAS_PATH = COMMONFILES + os.sep + WRITEUP_CANEVAS
SUMMARY_SOLUTION_FILL = "summary-solution{}.txt"
TEASE_FILL = "tease{}.txt"
EMPTY_ANSWER_FILL = "answer{}{}.txt"

WRITEUP_FILL = "writeup{}.md"
CHALLENGE_YML_FILL = "challenge{}.yml"

PDF_NAME_FILL = "{0}{1}.pdf"


def __read_file__(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()


def __read_common_file__(filename: str):
    with open(COMMONFILES + os.sep + filename, 'r') as file:
        return file.read()


PDF_TEXTS = [DESC_IN_PDF] + \
            [__read_common_file__(BARE_REQUIREMENT_FILE.format(i)) for i in (1, 2)]

QUICKTEX = __read_common_file__("quicktex.txt")
