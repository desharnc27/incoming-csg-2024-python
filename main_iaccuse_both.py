import os
from commonpy import my_utils

from iaccuse.cst import PROJECT as PJ
from iaccuse import i_accuse_prob_win, i_accuse_prob_length

print(os.getcwd())

PJ.put_flag_steps_in_file("175/375", real_answer=False, use_sha1=False)
mains = i_accuse_prob_win.main, i_accuse_prob_length.main
for ques in (1, 2):
    print(f"---- Question {ques} -------")
    answer = str(mains[ques - 1](ques))
    PJ.put_flag_steps_in_file(answer, real_answer=True, use_sha1=False, question_detail=ques)
    complete_flag = my_utils.my_flag(answer)
    PJ.make_writeup(complete_flag, 2024, ques)
    PJ.make_challenge_yml(complete_flag, [], bilingual_pdfs=True, question_id=ques)