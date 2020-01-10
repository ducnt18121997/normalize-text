# -*- coding: utf-8 -*-

import os
import re
import unicodedata
from config import *

def classify_text(list_token):
    list_label = []
    for i, NSWs in enumerate(list_token):
        label = []
        #Rules
        token = NSWs[0]
        env = NSWs[1].split()
        if token.lower() not in list_vietnamese_words:
            #URLE
            if re.match(email_regex, token) or re.match(url_regex, token):
                label.append('OTHERS')
                label.append('URLE')
            #Number
            elif re.match(r'([0-9])', token):
                for j in range(len(env)):
                    env[j] = env[j].lower()
                label.append('NUMBERS')
                #Token chứa :
                if ':' in token:
                    if token.count('-') == 1:
                        label.append('NTIM')
                    elif token.count('-') == 0:
                        if token.count(':') == 2:
                            label.append('NTIM')
                        elif token.count(':') == 1:
                            if ('.' in token) or (',' in token):
                                label.append('NTIM')
                            else:
                                token_ = token.split(':')
                                try:
                                    if int(token_[0]) > 59 or int(token_[1]) > 60:
                                        label.append('NSCR')
                                    else:
                                        label.append('NTIM')
                                except:
                                    label.append('NTIM')
                        else:
                            label[0] = 'OTHERS'
                            label.append('CSEQ')
                    else:
                        label[0] = 'OTHERS'
                        label.append('CSEQ')
                #Token chứa %
                elif '%' in token:
                    label.append('NPER')
                #Token chứa /
                elif '/' in token:
                    #Token chứa / và .
                    if '.' in token:
                        label.append('NFRC')
                    #Token chứa / và ,
                    elif ',' in token:
                        try:
                            if token.count('/') == 2:
                                label.append('NDAT')
                            elif token.count('/') == 1:
                                token_ = token.split('/')
                                if int(token_[-1]) > 12:
                                    label.append('NMON')
                                else:
                                    label.append('NDAY')
                        except:
                            label[0] = 'OTHERS'
                            label.append('CSEQ')
                    #Token chứa / và -
                    if '-' in token:
                        if token.count('-') == 1:
                            token = token.split('-')
                            token_ = token[0]
                            token__ = token[1]
                            token = '-'.join(token)
                            try:
                                if token.count('/') == 1:
                                    token__ = token__.split('/')
                                    if int(token__[-1]) > 12:
                                        label.append('NMON')
                                    else:
                                        label.append('NDAY')
                                elif token.count('/') == 2:
                                    if '/' not in token_:
                                        label.append('NDAT')
                                    else:
                                        token__ = token__.split('/')
                                        if int(token__[-1]) > 12:
                                            label.append('NMON')
                                        else:
                                            label.append('NDAY')
                                elif (token.count('/') == 3) or (token.count('/') == 4):
                                    label.append('NDAT')
                                else:
                                    label[0] = 'OTHERS'
                                    label.append('CSEQ')
                            except: 
                                label[0] = 'OTHERS'
                                label.append('CSEQ')
                        else:
                            label[0] = 'OTHERS'
                            label.append('CSEQ')
                    #Token chỉ chứa /
                    else:
                        if token.count('/') == 2:
                            for j in range(len(env)):
                                if env[j] in N_Space:
                                    label.append('NADD')
                                    break
                            if len(label) < 2:
                                label.append('NDAT')
                        elif token.count('/') == 1:
                            token_ = token.split('/') 
                            for j in range(len(env)):
                                if env[j] in N_Space:
                                    label.append('NADD')
                                    break
                                elif env[j] in N_Frc:
                                    label.append('NFRC')
                                    break
                                elif env[j] in N_Time:
                                    if int (token_[0]) > 12:
                                        label.append('NMON')
                                    else:
                                        label.append('NDAY')
                            if len(label) < 2:
                                try:
                                    if token == '24/7' or token == '24/24':
                                        label.append('NFRC')
                                    elif token in N_T_Spec:
                                        label.append('NDAY')
                                    elif int(token_[-1]) > 12 and (int(token_[-1]) > 0):
                                        label.append('NMON')
                                    else:
                                        label.append('NFRC')
                                except:
                                    label[0] = 'OTHERS'
                                    label.append('CSEQ')
                        else:
                            label.append('NFRC')
                #Token chứa -
                elif '-' in token:
                    if ('.' in token) or (',' in token):
                        label.append('NRNG')
                    else:
                        if token.count('-') == 1:
                            for j in range(len(env)):
                                if env[j] in N_Rng:
                                    label.append('NRNG')
                                    break
                                elif env[j] in N_Scr:
                                    label.append('NSCR')
                                    break
                                elif env[j] in N_Time:
                                    try:
                                        token_ = token.split('-')
                                        if int(token_[-1]) > 12:
                                            label.append('NMON')
                                        else:
                                            label.append('NDAY')
                                        break
                                    except:
                                        label.append('NSCR')
                            if len(label) < 2:
                                label.append('NSCR')
                        elif token.count('-') == 2:
                            token_ = token.split('-')
                            for j in range(len(token_)):
                                if int(token_[j]) == 0:
                                    label[0] = 'OTHERS'
                                    label.append('CSEQ')
                                    break
                            if label[0] == 'NUMBERS':
                                for j in range(len(env)):
                                    if env[j] in N_Time:
                                        label.append('NDAT')
                                    else:
                                        try:
                                            if int(token_[-1]) > 9:
                                                if (int(token_[0]) <= 31) and (int(token_[1]) <= 12):
                                                    label.append('NDAT')
                                                else:
                                                    label[0] = 'OTHERS'
                                                    label.append('CSEQ')
                                            else:
                                                label[0] = 'OTHERS'
                                                label.append('CSEQ')
                                        except:
                                            label[0] = 'OTHERS'
                                            label.append('CSEQ')    
                        else:
                            label[0] = 'OTHERS'
                            label.append('CSEQ')
                #Token chứa .
                elif '.' in token:
                    if ',' in token:
                        label[0] = 'OTHERS'
                        label.append('CSEQ')
                    else:
                        for j in range(len(Money)):
                            if Money[j] in token.upper():
                                label.append('MONY')
                                break
                        if len(label) < 2:
                            if token.count('.') == 1:
                                token_ = token.split('.')
                                if len(token_[1]) == 3:
                                    label.append('NNUM')
                                else:
                                    label[0] = 'OTHERS'
                                    label.append('CSEQ')
                            elif token.count('.') == 2 or token.count('.') == 3:
                                token_ = token.split('.')
                                if token.count('.') == 3:
                                    tel_check = token_[0] + token_[1]
                                else:
                                    tel_check = token_[0]
                                if tel_check in N_1st_Tel:
                                    label.append('NTEL')
                                else:
                                    for j in range(len(env)):
                                        if env[j] in N_Dig:
                                            label.append('NDIG')
                                            break
                                        elif env[j] in N_Tel:
                                            label.append('NTEL')
                                            break
                                    if len(label) < 2:
                                        label.append('NNUM')
                            else:
                                if token[0] == '0':
                                    label.append('NDIG')
                                else:
                                    label.append('NNUM')
                #Token chứa ,
                elif ',' in token:
                    for j in range(len(Money)):
                        if Money[j] in token.upper():
                            label.append('MONY')
                            break
                    if len(label) < 2:
                        token_ = token.split(',')
                        if token.count(',') >= 2:
                            for j in range(len(token_)):
                                if j == 0:
                                    continue
                                else:
                                    if len(token_[j]) != 3:
                                        label[0] = 'OTHERS'
                                        label.append('CSEQ')
                            if len(label) < 2:
                                label.append('NNUM')
                        else:
                            label.append('NNUM')
                    
                #Token còn lại
                else:
                    if token[0] == '+':
                        label.append('NTEL')
                    else:
                        for j in range(len(Money)):
                            if Money[j] in token.upper():
                                label.append('MONY')
                                break
                        if len(label) < 2:
                            for j in range(len(env)):
                                if env[j] in N_Dig:
                                    label.append('NDIG')
                                elif env[j] in N_Tel:
                                    label.append('NTEL')
                            if (token[0:3] in N_1st_Tel) or (token[0:4] in N_1st_Tel):
                                label.append('NTEL')
                        if len(label) < 2:
                            if len(token) < 3:
                                label.append('NNUM')
                            else:
                                if token[0] == '0':
                                    label.append('NDIG')
                                else:
                                    label.append('NNUM')

            #Letters
            elif re.match(r'[a-zA-Z]', token):
                label.append('LETTERS')
                if len(token) == 1:
                    if (token in MONY)  or (token in UNIT):
                        label.append('LABB')
                    else:
                        label.append('LSEQ')
                else:
                    if (token.upper() in LABB) or (token.upper() in MONY)  or (token.lower() in UNIT):
                        label.append('LABB')
                    elif token == token.upper():
                        label.append('LSEQ')
                    else:
                        label.append('LWRD')
            #Others
            else:
                label.append('OTHERS')
                if token in punc_read:
                    label.append('PUNC')
                elif token in punc_dura:
                    label.append('DURA')
                elif token.upper() in LABB:
                    label[0] = 'LETTERS'
                    label.append('LABB')
                elif token[0] == '+':
                    if (len(token) >= 9) and (len(token) <= 12):
                        label[0] = 'NUMBERS'
                        label.append('NTEL')
                    else:
                        label.append('CSEQ')
                else:
                    if re.match('[a-zA-Z0-9_]', token):
                        label.append('CSEQ')
                    else:
                        label.append('NONE')
            list_label.append(label[0:2])
        else:
            label = []
            label.append('NOT_NSWs')
            label.append('SKIP')
            list_label.append(label)
    return list_label
