import pronouncing
import re
import os.path
import time
from config import *
from tqdm import tqdm

def convert_by_rules(en_pronounce):
    """
        Chuyển theo luật phiên âm tiếng Anh từ CMU dictionary sang phiên âm tiếng Việt
    """
    list_en_phonemes = en_pronounce.split()
    list_vi_phonemes = []
    for i, en_phone in enumerate(list_en_phonemes):
        if i == 0:
            if en_phone in cmuphone2vi_dict.keys():
                list_vi_phonemes.append(cmuphone2vi_dict[en_phone].split(',')[0])
        elif i == len(list_en_phonemes) - 1:
            if en_phone in cmuphone2vi_dict.keys():
                list_vi_phonemes.append(cmuphone2vi_dict[en_phone].split(',')[2])
        else:
            if en_phone in cmuphone2vi_dict.keys():
                list_vi_phonemes.append(cmuphone2vi_dict[en_phone].split(',')[1])
    
    temp = ''.join(list_vi_phonemes)

    phones1 = 'au|ao|ai|ây|oi|âu'
    phones2 = 'b|p|ch|đ|d|ph|g|h|gi|k|c|l|m|n|ng|p|r|x|s|t|th|gu'
    phones3 = 'a|ă|â|ơ|o|ô|e|ê|i|y|u'
    phones4 = 'au|ao|ai|ây|oi|âu|a|ơ|ă|o|e|ê|ơ|i|ô|u|y'

    phones2_ = 'gi|gu'

    #tách mộ số âm không đọc được
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones2_, phones1),
                  lambda x: x.group('id') + ' ' + x.group('id1'), temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones2_, phones1),
                  lambda x: x.group('id') + ' ' + x.group('id1'), temp)

    #thêm ờ cho phụ âm đứng riêng
    if temp in phones2.split('|'):
        temp += 'ờ'
    
    #loại bỏ 1 số âm cuối không đọc được
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones1, phones2),
                  lambda x: x.group('id'), temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones1, phones2),
                  lambda x: x.group('id'), temp)
                  
    #chỉnh sửa 1 số âm cuối 
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format('e|ê', 'l'),
                  lambda x: 'eo', temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format('e|ê', 'l'),
                  lambda x: 'eo', temp)

    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format('a|ă|â|o|ô|ơ', 'l'),
                  lambda x: 'ồ', temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format('a|ă|â|o|ô|ơ', 'l'),
                  lambda x: 'ồ', temp)

    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format('i|y|u', 'l'),
                  lambda x: x.group('id'), temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format('i|y|u', 'l'),
                  lambda x: x.group('id'), temp)

    # thêm dấu
    add_prosodic_dict = {
        'at':'át', 'ăt':'ắt', 'ât':'ất', 'et':'ét', 'êt':'ết', 'it':'ít', 'ot':'ót', 'ôt':'ốt', 'ơt':'ớt', 'ut':'út', 'ưt':'ứt', 'yt':'ýt',
        'ac':'ác', 'ăc':'ắc', 'âc':'ấc', 'ec':'éc', 'êc':'ếc', 'ic':'íc', 'oc':'óc', 'ôc':'ốc', 'ơc':'ớc', 'uc':'úc', 'ưc':'ức', 'yc':'ýc',
        'ap':'áp', 'ăp':'ắp', 'âp':'ấp', 'ep':'ép', 'êp':'ếp', 'ip':'íp', 'op':'óp', 'ôp':'ốp', 'ơp':'ớp', 'up':'úp', 'ưp':'ứp', 'yp':'ýp',   
    }
    temp = re.sub(r'(?P<id>{})'.format('|'.join(add_prosodic_dict.keys())), lambda x: add_prosodic_dict[x.group('id')], temp)
    return temp

def convert_enword(en_pronounce):
    list_en_phonemes = en_pronounce.split()
    for i, en_phone in enumerate(list_en_phonemes):
        # loại bỏ trọng âm
        if en_phone[-1].isdigit():
            list_en_phonemes[i] = en_phone[:-1]
    
    #Tách nguyên âm, phụ âm
    cmu_vowel = 'AA|AE|AH|AO|AW|AY|EH|ER|IH|IY|Y|OW|OY|EY|UH|UW'
    cmu_vowel = cmu_vowel.split('|')
    cmu_consonant = 'B|CH|D|DH|F|G|HH|JH|K|L|M|N|NG|P|R|S|SH|T|TH|V|W|Z|ZH'
    cmu_consonant = cmu_consonant.split('|')
    cmu_con_ = 'B|CH|D|DH|G|HH|JH|K|L|P|R|S|SH|T|V|W|Z|ZH'
    cmu_con__ = 'F|M|N|TH|NG' 

    list_cmu_phonemes = []
    
    if 'abbrev' in list_en_phonemes:
        for i in range(len(list_en_phonemes)):
            if list_en_phonemes[i] in cmu_consonant:
                list_cmu_phonemes.append('|')
                list_cmu_phonemes.append(list_en_phonemes[i])
            else:
                list_cmu_phonemes.append(list_en_phonemes[i])
    else:
        for i in range(len(list_en_phonemes)):
            if i == 0:
                #1st phonemes
                list_cmu_phonemes.append(list_en_phonemes[i])
            elif i == len(list_en_phonemes) - 1:
                #last phonemes
                if list_en_phonemes[i] in cmu_consonant:
                    if list_en_phonemes[i-1] in cmu_consonant:
                        list_cmu_phonemes.append('|')
                        list_cmu_phonemes.append(list_en_phonemes[i])
                    else:
                        list_cmu_phonemes.append(list_en_phonemes[i])
                else:
                    list_cmu_phonemes.append(list_en_phonemes[i])
            else:
                #rest phonemes
                if list_en_phonemes[i] in cmu_consonant:
                    #con-con
                    if list_en_phonemes[i-1] in cmu_consonant:
                        if (list_en_phonemes[i] == 'R') and (list_en_phonemes[i-1] == 'T'):
                            list_cmu_phonemes.append(list_en_phonemes[i])
                        else:
                            list_cmu_phonemes.append('|')
                            list_cmu_phonemes.append(list_en_phonemes[i])
                    #vow-con-vow
                    elif (list_en_phonemes[i-1] in cmu_vowel) and (list_en_phonemes[i+1] in cmu_vowel):
                        if list_en_phonemes[i] in cmu_con__:
                            list_cmu_phonemes.append(list_en_phonemes[i])
                            list_cmu_phonemes.append('|')
                            list_cmu_phonemes.append(list_en_phonemes[i])
                        else:
                            list_cmu_phonemes.append('|')
                            list_cmu_phonemes.append(list_en_phonemes[i])
                    #vow-con-R
                    elif (list_en_phonemes[i-1] in cmu_vowel) and (list_en_phonemes[i+1] == 'R'):
                        list_cmu_phonemes.append('|')
                        list_cmu_phonemes.append(list_en_phonemes[i])
                    else:
                        list_cmu_phonemes.append(list_en_phonemes[i])
                else:
                    #vow-vow
                    if list_en_phonemes[i-1] in cmu_vowel:
                        list_cmu_phonemes.append('|')
                        list_cmu_phonemes.append(list_en_phonemes[i])
                    else:
                        list_cmu_phonemes.append(list_en_phonemes[i])

    cmu_phonemes = ' '.join(list_cmu_phonemes)
    #print(cmu_phonemes)
    cmu_phonemes = cmu_phonemes.split(' | ')

    for i in range(len(cmu_phonemes)):
        if cmu_phonemes[i] == '':
            continue
        else:
            cmu_phonemes[i] = convert_by_rules(cmu_phonemes[i])
    
    cmu_phonemes = ' '.join(cmu_phonemes)
    cmu_phonemes = ' '.join(cmu_phonemes.split())
        
    return cmu_phonemes

#latin2words
def latin2words(token):
    from time import time
    t0 = time()
    # sửa một số âm tiết sang tiếng việt
    phones1 = 'ai|ao|ây|oi|âu'
    phones2 = 'p|c|t|ch|n|ng|m|ph|b|d|đ|g|h|x|s|th|v|gu|l|r'
    phones3 = 'a|ă|e|i|o|ơ|ô|u|y'
    phones4 = 'ai|ao|ây|oi|âu|a|ă|e|i|o|ơ|ô|u'
    #token = re.sub('(?P<id>{})(?P<id1>({})(?P<id2>({})'.format(phones3, phones2, phones4),
    #               lambda x: x.group('id') + x.group('id1') + ' ' + x.group('id1') + x.group('id2'), token)
    #token = re.sub('(?P<id>{})(?P<id1>({})(?P<id2>({})'.format(phones3, phones2, phones4),
    #               lambda x: x.group('id') + x.group('id1') + ' ' + x.group('id1') + x.group('id2'), token)
    token = re.sub('yl', 'in', token)
    token = re.sub('(?P<id>da|di|de|du|do)',
                   lambda x: 'đ' + x.group('id')[1], token)
    token = re.sub('j|z', 'd', token)
    token = re.sub('f', 'ph', token)
    token = re.sub(r'd$', 't', token)
    token = re.sub('(?P<id>ya|ye|yo|yu)', lambda x: 'd' +
                   x.group('id')[1], token)
    token = re.sub('(?P<id>ka|ko|ku)', lambda x: 'c' + x.group('id')[1], token)
    token = re.sub('(?P<id>ci|ce)', lambda x: 'k' + x.group('id')[1], token)
    token = re.sub('al', 'an', token)
    token = re.sub('el', 'eo', token)
    token = re.sub('il', 'iu', token)
    token = re.sub('ol', 'on', token)
    token = re.sub('ul', 'un', token)
    token = re.sub('ue', 'oe', token)
    token = re.sub('et', 'ét', token)
    token = re.sub('ic', 'ích', token)
    token = re.sub('sh', 's', token)
    token = re.sub('ei', 'ây', token)
    token = re.sub('ee', 'i', token)
    token = re.sub('w', 'gu', token)
    token = re.sub('q','qu', token)

    i = 0
    newtoken = ''
    while i < len(token):
        # so khớp từ dài đến ngắn  xem có từ nào không
        # nếu có thì thay thế bởi phiên âm
        for j in [5, 4, 3, 2, 1]:
            if i+j <= len(token):
                if j == 1 and token[i] not in ['a', 'e', 'i', 'o', 'u']:
                    # nếu chỉ có 1 chữ cái không phải nguyên âm thì bỏ qua
                    i += 1
                elif token[i:i+j] in vn_words_dict:
                    newtoken += token[i:i+j] + ' '
                    i = i+j
                    break
    return newtoken

def read_en2vi(en_word):
    """ 
        Chuyển 1 từ tiếng Anh sang cách đọc tiếng Việt
    """
    result = ""
    try:
        if en_word in popular_en2vi_dict:
            result = popular_en2vi_dict[en_word]
        else:
            en_pronounce = pronouncing.phones_for_word(en_word)
            # 1 từ tiếng anh có thể có >= 1 cách phát âm
            # ta dùng cách phát âm đầu tiên
            en_pronounce = en_pronounce[0]
            result = convert_enword(en_pronounce)
    except:
        return None
    return result

def en2vi(en_word):
    result = ""
    result = read_en2vi(en_word)
    if result != None:
        return result
    else:
        result = ""
        phones1 = 'b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z'
        phones2 = 'a|e|o|u|i|y'
        
        en_word = re.sub('(?P<id>{})(?P<id1>({})({}))'.format(phones2, phones1, phones2),
                      lambda x: x.group('id') + ' ' + x.group('id1'), en_word)
        en_word = re.sub('(?P<id>{})(?P<id1>({})({}))'.format(phones2, phones1, phones2),
                      lambda x: x.group('id') + ' ' + x.group('id1'), en_word)
        
        en_word = re.sub('(?P<id>{})(?P<id1>({})({}))'.format(phones1, phones1, phones1),
                      lambda x: x.group('id') + ' ' + x.group('id1'), en_word)
        en_word = re.sub('(?P<id>{})(?P<id1>({})({}))'.format(phones1, phones1, phones1),
                      lambda x: x.group('id') + ' ' + x.group('id1'), en_word)
        
        en_word = re.sub('(?P<id>({})({}))(?P<id1>({})({}))'.format(phones2, phones1, phones1, phones2),
                      lambda x: x.group('id') + ' ' + x.group('id1'), en_word)
        en_word = re.sub('(?P<id>({})({}))(?P<id1>({})({}))'.format(phones2, phones1, phones1, phones2),
                      lambda x: x.group('id') + ' ' + x.group('id1'), en_word)
        #popular_en2word_dict
        en_arr = en_word.split()
        if len(en_arr) > 1:
            for i in range(len(en_arr)):
                result = read_en2vi(en_arr[i])
                #khác none thì đọc
                if result != None:
                    en_arr[i] = result
                else:
                    try:
                        en_arr[i] = latin2words(en_arr[i])
                    except:
                        for char in en_arr[i]:
                            if char.upper() in (LSEQ_DICT.keys()):
                                result += LSEQ_DICT[char.upper()] + ' '
            result = ' '.join(en_arr)
        else:    
            result = ""
            en_word = en_word.upper()
            for char in en_word:
              if char.upper() in (LSEQ_DICT.keys()):
                  result += LSEQ_DICT[char.upper()] + ' '
    result = ' '.join(result.split())   
    return result