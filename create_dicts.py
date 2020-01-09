# -*- coding: utf-8 -*-
import pronouncing
import re
import os.path
import time

from tqdm import tqdm
from config import *
from en2vi import en2vi

cmuphone2vi_dict = load_dict(CMUPHONE2VI_DICT_PATH)
popular_en2vi_dict = load_dict(POPULAR_EN2VI_DICT_PATH)
popular_branch_dict = load_dict(BRANCH_DICT_PATH)
popular_person_dict = load_dict(PERSON_DICT_PATH)

popular_en2vi_dict.update(popular_branch_dict)
popular_en2vi_dict.update(popular_person_dict)

list_enwords = pronouncing.cmudict.words()
list_enwords.extend(popular_en2vi_dict.keys())


"""Tạo từ điển phiên âm tiếng Việt cho các từ tiếng Anh"""
t0 = time.time()

with open(EN2VI_DICT_PATH, 'w') as f:
    for enword in tqdm(list_enwords):
        viword = en2vi(enword)
        if viword:
            # khác None thì ghi vào file
            f.write("{}|{}\n".format(enword, viword))

print("Time: {} s".format(time.time()-t0))