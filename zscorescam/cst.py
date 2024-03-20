from commonpy.project import Project

PROJECT = Project(name="zscorescam",
                  titles="Lily Bernard at Learngame-HC College",
                  tags=["mathematics", "statistics"])

INPUT_RAW_NAME = "data"
OUTPUT_RAW_NAME = "answer"
EXT = ".txt"

INPUT_FILENAME = INPUT_RAW_NAME + EXT
OUTPUT_FILENAME = OUTPUT_RAW_NAME + EXT
INPUT_PATH = PROJECT.path(INPUT_FILENAME)
OUTPUT_PATH = PROJECT.path(OUTPUT_FILENAME)

LBERNARD = "Lily Bernard"

MINI_STEP_ALGO = False
