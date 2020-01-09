# -*- coding: utf-8 -*-

import os
import re
import unicodedata
from expand_NSWs import *
from config import *

def replace(list_token, list_label):
    new_token = []
    for i in range(len(list_token)):
        token = list_token[i][0]
        env = list_token[i][1]
        category = list_label[i][1]
        #NUMBERS
        if category == 'NTIM':
            token = NTIM2words(token)
        elif category == 'NDAT':
            token = NDAT2words(token)
        elif category == 'NDAY':
            token = NDAY2words(token)
        elif category == 'NMON':
            token = NMON2words(token)
        elif category == 'NNUM':
            token = NNUM2words(token)
        elif category == 'NTEL':
            token = NTEL2words(token)
        elif category == 'NDIG':
            token = NDIG2words(token)
        elif category == 'NSCR':
            token = NSCR2words(token)
        elif category == 'NRNG':
            token = NRNG2words(token)
        elif category == 'NPER':
            token = NPER2words(token)
        elif category == 'NFRC':
            token = NFRC2words(token)
        elif category == 'NADD':
            token = NADD2words(token)
        #LETTERS
        elif category == 'LWRD':
            token = LWRD2words(token)
        elif category == 'LSEQ':
            token = LSEQ2words(token)
        elif category == 'LABB':
            token = LABB2words(token)
        #OTHERS
        elif category == 'PUNC':
            token = PUNC2words(token)
        elif category == 'URLE':
            token = URLE2words(token)
        elif category == 'MONY':
            token = MONY2words(token)
        elif category == 'CSEQ':
            token = CSEQ2words(token)
        elif category == 'DURA':
            token = DURA2words(token)
        elif category == 'NONE':
            token = NONE2words(token)
        token = str(token)
        new_token.append(token)
    text = ' '.join(new_token)
    return text, new_token