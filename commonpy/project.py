from typing import List

from commonpy import my_utils, csg_file_making, path_making

import commonpy.common_cst as cst


class Project:
    def __init__(self, name: str,
                 titles: str | list[str],
                 tags: str | list[str],
                 prerequisting: bool = False,
                 hand_flagging: bool = False):
        self._name = name
        self._titles = my_utils.listify(titles)
        self._tags = my_utils.listify(tags)
        self._prerequisting = prerequisting  # Not used yet always assumed false now
        self._hand_flagging = hand_flagging  # TODO might delete

    def title(self, question_id=0) -> str:
        if question_id == 0:
            return self._titles[0]
        return self._titles[question_id - 1]

    # Akward that path() and name() are 2 fcts.
    # Does the same because paths are designed to be the name itself

    def path(self, end_name: str = None) -> str:
        return path_making.leafing(self._name, end_name)

    def name(self):
        return self._name

    def make_challenge_yml(self, complete_flag: str, extra_fnames: List[str], bilingual_pdfs=True,
                           question_id: int = 0):
        fnames = []
        if question_id < 2:
            langs = [""] if not bilingual_pdfs else ["en", "fr"]
            for lang in langs:
                fnames.append(path_making.pdf_name(self._name, lang))

            fnames.append(path_making.flag_steps_name(True, question_id))
        fnames = fnames + extra_fnames
        return csg_file_making.make_challenge_yml(path_making.challenge_yml_path(self._name, question_id),
                                                  path_making.tease_path(self._name, question_id),
                                                  self.title(question_id),
                                                  complete_flag,
                                                  self._tags,
                                                  fnames,
                                                  cst.PDF_TEXTS[question_id])

    def make_writeup(self, complete_flag: str, year: int, question_id: int = 0, code_language="python"):

        csg_file_making.make_writeup(path_making.summary_solution_path(self._name, question_id),
                                     path_making.flag_steps_path(self._name, False, question_id),
                                     path_making.writeup_path(self._name, question_id),
                                     self.title(question_id),
                                     complete_flag,
                                     year,
                                     code_language)

    def put_flag_steps_in_file(self,
                               answer: int | str,
                               real_answer: bool,
                               use_sha1: bool = False,
                               question_detail: int = 0) -> None:
        csg_file_making.put_flag_steps_in_file(path_making.flag_steps_path(self._name,
                                                                           not real_answer,
                                                                           question_detail),
                                               answer,
                                               real_answer,
                                               use_sha1)
