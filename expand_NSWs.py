# encoding : utf-8
import re
import pronouncing
import os.path
from num2words import num2words
from unicodedata import normalize
from datetime import date

from utils import load_dict
from config import *
from en2vi import *

# hàm bignumread để xử lý số lớn mà thu viện num2words không xử lý được
def bignumread(numberstring, index=0):
    '''đọc số tự nhiên lớn (>10^9), index: độ lớn hàng tỷ cần xét'''
    if len(numberstring) <= 9:
        return smallnumread(numberstring)
    else:
        index += 1
        big = numberstring[:-9]
        small = numberstring[-9:]
        return bignumread(big, index+1) + ' ' + 'tỷ '*index + ' ' + smallnumread(small)

def smallnumread(numberstring):
    '''đọc số tự nhiên nhỏ có chỉnh sửa từ thư viện num2words'''
    result = ""
    number = int(numberstring)
    if number <= 1000 or number % 100 == 0:
        result = num2words(number, lang='vi')
    else:
        result = num2words(number//100*100, lang='vi')
        if ((number//100) % 10 == 0):
            result += " không trăm"
        if number % 100 < 10:
            result += " lẻ " + num2words(number % 100, lang='vi')
        else:
            result += " " + num2words(number % 100, lang='vi')
    return result

def decimal2words(numberstring):
    """đọc số tự nhiên"""
    if len(numberstring) <= 9:
        return smallnumread(numberstring)
    else:
        return bignumread(numberstring)

"""NUMBERS Start"""
#NNUM class
def NNUM2words(nnum_string):
    """đọc số tự nhiên, có thể có phân tách . và số thập phân"""
    result = ""
    try:
        if ',' in nnum_string:
            if nnum_string.count(',') == 1:
                nnum_arr = nnum_string.split(',')
                result = decimal2words(nnum_arr[0]) + ' phẩy ' + decimal2words(nnum_arr[1])
            else:
                nnum_string = re.sub(r'\,', '', nnum_string)
                result = decimal2words(nnum_string)
        else:
            nnum_string = re.sub(r'\.', '', str(nnum_string))
            result = decimal2words(nnum_string)
        return result
    except:
        return result

#NTIM class
def TIM2words(time_string):
    result = ""
    if '.' in time_string:
        time_string = re.sub(r'\.',',',time_string)
    time_arr = time_string.split(':')
    if ',' in time_string:
        m = time_arr[0]
        s = time_arr[1]
        result = NNUM2words(m) + " phút " + NNUM2words(s) + " giây"
    else:
        if len(time_arr) == 2:
            if int(time_arr[1]) > 60:
                m = time_arr[0]
                s = time_arr[1]
                result = NNUM2words(m) + " phút " + NNUM2words(s) + " giây"
            else:
                h = time_arr[0]
                m = time_arr[1]
                result = NNUM2words(h) + " giờ " + NNUM2words(m) + " phút"
        else:
            h = time_arr[0]
            m = time_arr[1]
            s = time_arr[2]
            result = NNUM2words(h) + " giờ " + NNUM2words(m) + " phút " + NNUM2words(s) + " giây" 
    return result

def NTIM2words(ntim_string):
    result = ""
    if '-' in ntim_string: 
        ntim_arr = ntim_string.split('-')
        result = TIM2words(ntim_arr[0]) + " đến " + TIM2words(ntim_arr[1])
    else:
        result = TIM2words(ntim_string)
    return result

"""ngày/tháng"""
def DAY2words(day_string):
    separator = '/'
    day_arr = day_string.split(separator)
    d, m = day_arr[0], day_arr[1]

    # đọc ngày
    dstring = ""
    if int(d) <= 10:
        dstring = "mồng " + NNUM2words(d)
    else:
        dstring = NNUM2words(d)
    
    return dstring + " tháng " + NNUM2words(m)

"""tháng/năm"""
def MON2words(mon_string):    
    separator = '/'
    mont_arr = mon_string.split(separator)
    m, y = mont_arr[0], mont_arr[1]

    return NNUM2words(m) + " năm " + NNUM2words(y)

"""ngày/tháng/năm"""
def DAT2words(date_string):
    separator = '/'
    date_arr = date_string.split(separator)
    d, m, y = date_arr[0], date_arr[1], date_arr[2]

    # đọc ngày
    dstring = ""
    if int(d) <= 10:
        dstring = "mồng " + NNUM2words(d)
    else:
        dstring = NNUM2words(d)

    return dstring + " tháng " + NNUM2words(m) + " năm " + NNUM2words(y)

#NDAT class
def NDAT2words(ndat_string):
    result = ""
    if '-' in ndat_string:
        ndat_arr = ndat_string.split('-')
        if ndat_string.count('/') == 4:
            result = DAT2words(ndat_arr[0]) + " đến " + DAT2words(ndat_arr[1])
        elif ndat_string.count('/') == 3:
            result = DAY2words(ndat_arr[0]) + " đến " + DAT2words(ndat_arr[1])
        elif ndat_string.count('/') == 2:
            # đọc ngày
            dstring = ""
            if int(ndat_arr[0]) <= 10:
                dstring = "mồng " + NNUM2words(ndat_arr[0])
            else:
                dstring = NNUM2words(ndat_arr[0])
            result = dstring + " đến " + DAT2words(ndat_arr[1])
    else:
        result = DAT2words(ndat_string)
    return result

#NMON class
def NMON2words(nmon_string):
    result = ""
    if '-' in nmon_string:
        nmon_arr = nmon_string.split('-')
        if nmon_string.count('/') == 2:
            result = MON2words(nmon_arr[0]) + " đến " + MON2words(nmon_arr[1])
        elif nmon_string.count('/') == 1:
            result = NNUM2words(nmon_arr[0]) + " đến " + MON2words(nmon_arr[1])
    else:
        result = MON2words(nmon_string)
    return result

#NDAY class
def NDAY2words(nday_string):
    result = ""
    if '-' in nday_string:
        nday_arr = nday_string.split('-')
        if nday_string.count('/') == 2:
            result = DAY2words(nday_arr[0]) + " đến " + DAY2words(nday_arr[1])
        elif nday_string.count('/') == 1:
            dstring = ""
            if int(nday_arr[0]) <= 10:
                dstring = "mồng " + NNUM2words(nday_arr[0])
            else:
                dstring = NNUM2words(nday_arr[0])
            result = dstring + " đến " + DAY2words(nday_arr[1])
    else:
        result = DAY2words(nday_string)
    return result

#NDIG class
def NDIG2words(ndig_string):
    "3925"
    result = ""
    for digit in ndig_string:
        if digit.isdigit():
            result += num2words(int(digit), lang='vi') + " "
    return result

#NTEL class
def NTEL2words(ntel_string):
    "093.156.2565, +84357121314"
    ntel_string = ''.join(ntel_string.split('.'))
    result = ""
    if '+' in ntel_string:
        ntel_string = re.sub(r'\+','',ntel_string)
        result = 'cộng ' + NDIG2words(ntel_string)
    else:
        result = NDIG2words(ntel_string)
    return result

#NSCR class
def NSCR2words(nscr_string):
    """tỷ số `2-3`"""
    result = ""
    nscr_string = re.sub(':','-',nscr_string)
    arr = nscr_string.split('-')
    if nscr_string.count('-') == 1:
        result = NNUM2words(arr[0]) + ' ' + NNUM2words(arr[1])
    return result

#NRNG class
def NRNG2words(nrng_string):
    """từ `2-3`"""
    nrng_string_arr = nrng_string.split('-')
    result = NNUM2words(nrng_string_arr[0]) + ' đến ' + NNUM2words(nrng_string_arr[1])
    return result

#NPER class
def NPER2words(nper_string):
    """30% hoặc 30-40%"""
    result = ""
    nper_string = re.sub('\.',',', nper_string)
    if '-' in nper_string:
        if nper_string.count('-') == 1:
            nper_string = re.sub('\%', '', nper_string)
            result = NRNG2words(nper_string) + " phần trăm "
    else:
        nper_string = re.sub('\%', '', nper_string)
        result = NNUM2words(nper_string) + " phần trăm "
    return result

#NFRC class
def NFRC2words(nfrc_string):
    result = ""
    nfrc_arr = nfrc_string.split('/')
    if '.' in nfrc_string:
        result = NNUM2words(nfrc_arr[0]) + ' trên ' + NNUM2words(nfrc_arr[1])
    if nfrc_string.count('/') == 1:
        if int(nfrc_arr[0]) >= int(nfrc_arr[1]):
            result = NNUM2words(nfrc_arr[0]) + ' trên ' + NNUM2words(nfrc_arr[1])
        else:
            if (int(nfrc_arr[0]) < 10) and (int(nfrc_arr[1]) < 10):
                result = NNUM2words(nfrc_arr[0]) + ' phần ' + NNUM2words(nfrc_arr[1])
            else:
                result = NNUM2words(nfrc_arr[0]) + ' trên ' + NNUM2words(nfrc_arr[1])
    else:
        for i in range(len(nfrc_arr)):
            if i == 0:
                result = NNUM2words(nfrc_arr[i])
            else:
                result = ' trên ' + NNUM2words(nfrc_arr[i])
    return result

#NADD class
def NADD2words(nadd_string):
    result = ""
    """Số 14/3/2 phố Huế"""
    separator = '/'
    nadd_arr = nadd_string.split(separator)
    if nadd_string.count('/') == 3:
        result = 'ngõ ' + NNUM2words(nadd_arr[0]) + ' ngách ' + NNUM2words(nadd_arr[1]) + ' hẻm ' + NNUM2words(nadd_arr[2])  + ' số ' + NNUM2words(nadd_arr[3])
    elif nadd_string.count('/') == 2:
        result = 'ngõ ' + NNUM2words(nadd_arr[0]) + ' ngách ' + NNUM2words(nadd_arr[1])  + ' số ' + NNUM2words(nadd_arr[2])
    elif nadd_string.count('/') == 1:
        result = 'ngõ ' + NNUM2words(nadd_arr[0])  + ' số ' + NNUM2words(nadd_arr[1])
    else:
        for i in range(len(nfrc_arr)):
            if i == 0:
                result = 'ngõ ' + NNUM2words(nfrc_arr[i])
            else:
                result = ' trên ' + NNUM2words(nfrc_arr[i])
    return result
"""NUMBERS End"""

"""LETTERS Start"""
#LWRD class
def LWRD2words(lwrd_string):
    result = ""
    lwrd_string = lwrd_string.lower()
    if lwrd_string in EN2VI_DICT.keys():
        result = EN2VI_DICT[lwrd_string]
    elif lwrd_string in EN2VI_DICT.keys():
        result = PERSON_DICT[lwrd_string]
    elif lwrd_string in EN2VI_DICT.keys():
        result = BRANCH_DICT[lwrd_string]
    else:
        if '-' in lwrd_string:
            lwrd_arr = lwrd_string.split('-')
            for i in range(len(lwrd_arr)):
                if lwrd_arr[i].lower() in list_vietnamese_words:
                    result += lwrd_arr[i] + ' '
                else:
                    result += LWRD2words(lwrd_arr[i]) + ' '
        else:
            result = en2vi(lwrd_string)
    return result

#LSEQ class
def LSEQ2words(lseq_string):
    result = ""
    lseq_string = lseq_string.upper()
    for char in lseq_string:
        if char.upper() in (LSEQ_DICT.keys()):
            result += LSEQ_DICT[char.upper()] + ' '
    return result

#LABB class
def LABB2words(labb_string):
    """ĐHBKHN"""
    result = ""
    labb_string = labb_string.upper()
    try:
        if labb_string in (ABB_DICT.keys()):
            result = ABB_DICT[labb_string].split(',')[0]
        elif labb_string in (UNIT_DICT.key()):
            result = UNIT_DICT[labb_string].split(',')[0]
        else:
            result = CURRENCY_DICT[labb_string].split(',')[0]
    except:
        result = CSEQ2words(labb_string)
    return result
"""LETTERS End"""

"""OTHERS Start"""
#PUNC class
def PUNC2words(punc_string):
    result = ''
    if punc_string in list(PUNC_DICT.keys()):
        result = PUNC_DICT[punc_string]
    return result

#DURA class
def DURA2words(dura_string):
    result = dura_string
    return result

#MONY class
def MONY2words(money_string):
    money_string = money_string.upper()
    result = ""
    # tách đơn vị và số
    money_string = re.sub(r'(?P<id>\d)(?P<id1>{})'.format(''.join(currency_list.split(
    ))), lambda x: x.group('id') + ' ' + CURRENCY_DICT[x.group('id1')], money_string)
    money_arr = money_string.split()
    for i in range(len(money_arr)):
        if i == 0:
            result += NNUM2words(money_arr[i])
        else:
            result += ' ' + money_arr[i]
    return result

#URLE class
def URLE2words(urle_string):
    """đọc đường link và email"""
    urle_string = urle_string.lower()
    urle_string = re.sub(r'\.$', '', urle_string)
    urle_string = re.sub(r'^http', 'hát tê tê pê ', urle_string)
    urle_string = re.sub(r'.com', ' chấm com ', urle_string)
    urle_string = re.sub(r'.edu', ' chấm e đu ', urle_string)
    urle_string = re.sub(r'gmail', ' gờ meo ', urle_string)
    urle_string = re.sub(r'outlook', ' ao lúc ', urle_string)
    urle_string = re.sub(r'@', ' a còng ', urle_string)
    urle_string = re.sub(r'(?P<id>{})'.format("\\" + '|\\'.join(PUNC_DICT.keys())),
                         lambda x: ' ' + PUNC2words(x.group('id')) + ' ', urle_string)
    urle_string = re.sub(r'(?P<id>\d)', lambda x: ' ' +
                         NNUM2words(x.group('id')) + ' ', urle_string)
    arr = urle_string.split()
    for i, word in enumerate(arr):
        if word not in list_vietnamese_words:
            # nếu đọc được theo tiếng Anh
            if LWRD2words(word):
                arr[i] = LWRD2words(word)
            else:
                k = 0
                newtoken = ''
                while k < len(word):
                    # so khớp từ dài đến ngắn  xem có từ nào đọc được tiếng Việt không
                    for j in [5, 4, 3, 2, 1]:
                        if k+j <= len(word):
                            if word[k:k+j] in vn_words_dict:
                                newtoken += word[k:k+j] + ' '
                                k = k+j
                                break
                            elif j > 2 and LWRD2words(word[k:k+j]):
                                # nếu có trong tiếng anh thì đọc kiểu tiếng anh
                                newtoken += LWRD2words(word[k:k+j]) + ' '
                                k = k+j
                                break
                            elif j == 1 and word[k] != ' ':
                                # nếu có 1 chữ cái thì đọc từng chữ
                                newtoken += LSEQ2words(word[k]) + ' '
                                k += 1
                                break
                            elif j == 1 and word[k] == ' ':
                                # kí tự cách
                                newtoken += ' '
                                k += 1
                arr[i] = newtoken

    result = ' '.join(arr)
    return result

#CSEQ class
def CSEQ2words(cseq_string):
    result = ""
    for char in cseq_string:
        if char.upper() in list(LSEQ_DICT.keys()):
            result += LSEQ_DICT[char.upper()] + ' '
        elif char in list(PUNC_DICT.keys()):
            result += PUNC_DICT[char] + ' '
        elif re.match(r'([0-9])', char):
            number = int(char)
            result += num2words(number, lang='vi') + ' '
    return result

#NONE class
def NONE2words(none_string):
    result = ''
    return result