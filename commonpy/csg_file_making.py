from fractions import Fraction
from typing import List

from commonpy import my_utils
from commonpy.common_cst import DEFAULT_AUTHOR, WRITEUP_CANEVAS_PATH, PUBLIC_GIT, QUICKTEX


def make_challenge_yml(filename: str,
                       tease_fn: str,
                       title: str,
                       complete_flag: str, tags: List[str],
                       fnames: List[str], pdf_text: str = ""):
    with open(filename, 'w') as file:
        line = "name: \"{}\"\n".format(title)
        file.write(line)
        line = "author: \"{}\"\n".format(DEFAULT_AUTHOR)
        file.write(line)
        file.write("description: |\n")
        four_spaces = "   "
        description: str

        with open(tease_fn, 'r') as tease_file:
            description = tease_file.read()

        val_str_list = ["pdf"]
        val_list = [pdf_text]
        description = my_utils.double_exclaim_replacement(val_str_list, val_list, description)
        description = description.replace("\n", "\n" + four_spaces)

        file.write(four_spaces + description + "\n")
        bulletor = four_spaces + "- {}\n"
        file.write("flags:\n")
        file.write(bulletor.format(complete_flag))
        file.write("tags:\n")
        for tag in tags:
            file.write(bulletor.format(tag))
        lines = []

        for fname in fnames:
            lines.append(bulletor.format(fname))
        if len(lines) > 0:
            file.write("files:\n")
            for line in lines:
                file.write(line)


def make_writeup(summary_path: str,
                 flag_steps_path: str,
                 writeup_path: str,
                 title: str,
                 complete_flag: str,
                 year: int,
                 code_language: str = "python"):
    with open(WRITEUP_CANEVAS_PATH, 'r') as file:
        content = file.read()
    url = PUBLIC_GIT.format(year, code_language)
    url_md = "[{0}]({0})".format(url)

    ss: str
    try:
        with open(summary_path, 'r') as summary_file:
            ss = summary_file.read()
    except FileNotFoundError as e:
        # If there is no such file we just don't add
        print("Might ot might not be ok: " + str(e))
        ss = ""
    with open(flag_steps_path, 'r') as file:
        flag_steps_content = "```\n" + file.read() + "\n```\n"

    val_str_list = ["title", "flag", "url", "summary", "quicktex", "flagsteps"]
    val_list = [title, complete_flag, url_md, ss, QUICKTEX, flag_steps_content]
    content = my_utils.double_exclaim_replacement(val_str_list, val_list, content)

    with open(writeup_path, 'w') as file:
        file.write(content)


def put_flag_steps_in_file(flag_steps_path: str,
                           answer: int | str,
                           real_answer: bool,
                           use_sha1: bool = False) -> None:
    attributes: List[str] = []
    values: List[str] = []
    answer = str(answer)
    ans_str = "answer" if real_answer else "fake_answer"
    fract = my_utils.detect_fraction(answer)
    if fract is not None:
        simplified_frac = Fraction(fract[0], fract[1])  # Should automatically simplify
        if simplified_frac.numerator != fract[0]:
            unsimp_str = "unsimplified_" + ans_str
            value = f"{fract[0]}/{fract[1]}"
            attributes.append(unsimp_str)
            values.append(value)
        answer = str(simplified_frac)

    attributes.append(ans_str)
    values.append(answer)

    if use_sha1:
        answer = my_utils.get_sha1(answer)
        sha1_str = f"sha1({ans_str})"
        attributes.append(sha1_str)
        values.append(answer)
    flag_str = "Flag"
    flag = f"FLAG{{{answer}}}"
    attributes.append(flag_str)
    values.append(flag)
    arrowed_list = my_utils.arrow_intuitive_format(attributes, values)
    my_utils.string_array_to_file(arrowed_list, flag_steps_path)
