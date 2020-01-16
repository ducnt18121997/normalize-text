# -*- coding: utf-8 -*-

from time import time
import re
import unicodedata
from config import *

def fix_punc(text, punc):
    list_token = text.split()
    text = []
    for i, NSWs in enumerate(list_token):
        if re.match(r'([0-9])', NSWs):
            if punc in NSWs:
                if NSWs.count(punc) > 1:
                    NSWs_ = NSWs.split(punc)
                    for j in range(len(NSWs_)):
                        if j == 0:
                            continue
                        else:
                            if len(NSWs_[j]) % 3 != 0:
                                if punc == '.':
                                    NSWs = re.sub(r'\.', ' _',NSWs)
                                    break
                                else:
                                    NSWs = re.sub(punc, ' '+punc+' ',NSWs)
                                    break
        text.append(NSWs)
    return ' '.join(text)

def split_token(text):
    '''convert_form'''
    # tách token
    list_tokens = text.split()
    for i, token in enumerate(list_tokens):
        # nếu là email hoặc url thì bỏ qua
        if re.match(email_regex, token) or re.match(url_regex, token):
            #print(token)
            continue
        
        # tách các từ bị dính các dấu ;/()'"
        # "đã xong.Viện" => "đã xong . Viện", "HN(Số 36)" => "HN ( Số 36)"
        
        #split_punc = '\.|\,|\;|\/|\(|\)|\!|\?|\…|\:|\%|\-|\+'
        split_punc = '\.|\,|\…|\;|\/|\(|\)|\!|\?|\'|\"|\“|\”|\:|\+|\*|\\|\_|\&|\%|\^|\[|\]|\{|\}|\=|\#|\@|\`|\~'
        # tách kí tự
        token = re.sub(r'(?P<id>[{}])(?P<id1>{})(?P<id2>[{}])'.format(charset, split_punc, charset),
                       lambda x: x.group('id') + ' ' + x.group('id1') + ' ' + x.group('id2'), token)
        
        token = re.sub(r'(?P<id>[{}])(?P<id1>{})(?P<id2>[{}]|\d+)'.format(charset, split_punc, charset),
                       lambda x: x.group('id') + ' ' + x.group('id1') + ' ' + x.group('id2'), token)
        token = re.sub(r'(?P<id>[{}]|\d+)(?P<id1>{})(?P<id2>[{}])'.format(charset, split_punc, charset),
                       lambda x: x.group('id') + ' ' + x.group('id1') + ' ' + x.group('id2'), token)

        #tách số
        token = re.sub(r'(?P<id>[{}]|\d+)(?P<id1>{})'.format(charset, split_punc),
                       lambda x: x.group('id') + ' ' + x.group('id1'), token)
        token = re.sub(r'(?P<id>{})(?P<id1>[{}]|\d+)'.format(split_punc, charset),
                       lambda x: x.group('id') + ' ' + x.group('id1'), token)
        
        # tách các punctuation liền nhau
        token = re.sub(r'(?P<id>{})(?P<id1>{})'.format(punc, punc),
                       lambda x: x.group('id') + ' ' + x.group('id1'), token)
        token = re.sub(r'(?P<id>{})(?P<id1>{})'.format(punc, punc),
                       lambda x: x.group('id') + ' ' + x.group('id1'), token)

        list_tokens[i] = token
    
    text = ' '.join(list_tokens)
    
    '''tranform_text'''
    # chuyển tiền tệ và dạng đơn vị ở cuối: $ 1000, $1000, 1000 $ => 1000$
    #pre_currency_list = '\$|S\$|SGD|VNĐ'
    text = re.sub(r'(?P<id>{})\s*(?P<id1>(\d+ \. )*\d+( \, \d+)?)'.format(currency_list),
                  lambda x: ''.join((x.group('id1') + x.group('id')).split()), text)
    text = re.sub(r'(?P<id>(\d+ \. )*\d+(\,\d+| \, \d+)*?)\s*(?P<id1>{})'.format(currency_list),
                  lambda x: ''.join((x.group('id') +  x.group('id1')).split()), text)
                  
    # chuyển số  về dạng chuẩn: 1 .000.000, 1. 000.000, 1  . 000. 000 => 1.000.000
    text = re.sub(r'(?P<id>\d+)(\s+\.|\.\s+|\s+\.\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+'.'+x.group('id1'), text)
    text = re.sub(r'(?P<id>\d+)(\s+\.|\.\s+|\s+\.\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+'.'+x.group('id1'), text)
    
    # chuyển các dạng lỗi 2018.2.121 thành 2018 _2 _12
    text = fix_punc(text, '.')
    
    # 2/ 3, 2 /3, 2 / 3 => 2/3
    text = re.sub(r'(?P<id>\d+)(\s+\/|\/\s+|\s+\/\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+'/'+x.group('id1'), text)
    text = re.sub(r'(?P<id>\d+)(\s+\/|\/\s+|\s+\/\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+'/'+x.group('id1'), text)
    
    # 09 15 33 45 77 => 09.15.33.45.77, 035 164 4565 => 035.164.4565
    text = re.sub(r'(?P<id>( |^|\,)\d+)\s+(?P<id1>\d+)( |$)',
              lambda x: x.group('id')+'.'+x.group('id1')+' ', text)
    text = re.sub(r'(?P<id>( |^|\,)\d+)\s+(?P<id1>\d+)( |$)',
              lambda x: x.group('id')+'.'+x.group('id1') + ' ', text)
    
    # 2, 3 => 2,3
    text = re.sub(r'(?P<id>( |^|\,)\d+)(\s+\,|\,s+|\s+\,\s+)(?P<id1>\d+( |^|\,))',
              lambda x: x.group('id')+','+x.group('id1'), text)
    text = re.sub(r'(?P<id>( |^|\,)\d+)(\s+\,|\,\s+|\s+\,\s+)(?P<id1>\d+( |^|\,))',
              lambda x: x.group('id')+','+x.group('id1'), text)
    text = fix_punc(text, ',')
    
    # 30- 40, 30 -40, 30 - 40 => 30-40
    text = re.sub(r'(?P<id>\d+)(\s+\-|\-\s+|\s+\-\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+'-'+x.group('id1'), text)
    text = re.sub(r'(?P<id>\d+)(\s+\-|\-\s+|\s+\-\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+'-'+x.group('id1'), text)
    
    # 30 % => 30%
    text = re.sub(r'(?P<id>\d+)(\s+\%)',
                  lambda x: x.group('id')+'%', text)
    text = re.sub(r'(?P<id>\d+)(\s+\%)',
                  lambda x: x.group('id')+'%', text)
    
    # 2 : 30 => 2:30, 12 : 30 : 59 => 12:30:59
    text = re.sub(r'(?P<id>\d+)(\s+\:|\:\s+|\s+\:\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+':'+x.group('id1'), text)
    text = re.sub(r'(?P<id>\d+)(\s+\:|\:\s+|\s+\:\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+':'+x.group('id1'), text)
    
    # + 84 => +84
    text = re.sub(r'(\+\s+)(?P<id>\d+)',
                  lambda x: '+'+x.group('id'), text)
    text = re.sub(r'(\+\s+)(?P<id>\d+)',
                  lambda x: '+'+x.group('id'), text)
        
    # chuyển tiền tệ và dạng đơn vị ở cuối: $ 1000, $1000, 1000 $ => 1000 $
    text = re.sub(r'(?P<id>{})\s*(?P<id1>(\d+ \. )*\d+( \, \d+)?)'.format('\$|S\$|USD|NDT|€|£|¥|Fr'),
                  lambda x: ''.join((x.group('id1') + x.group('id')).split()), text)
    text = re.sub(r'(?P<id>(\d+ \. )*\d+(\,\d+| \, \d+)?)\s*(?P<id1>{})'.format('\$|S\$|USD|NDT|€|£|¥|Fr'),
                  lambda x:  ''.join((x.group('id') +  x.group('id1')).split()), text)
    
    # loại bỏ tag punc
    text = re.sub(r'(\s+\_)(?P<id>\d+)',
              lambda x: ' '+x.group('id'), text)
    text = re.sub(r'(\s+\_)(?P<id>\d+)',
              lambda x: ' '+x.group('id'), text)

    # chỉnh sửa một số âm , ví dụ òa thành oà
    change_phone_dict = {'òa': 'oà', 'óa': 'oá', 'ọa': 'oạ', 'õa': 'oã', 'ỏa': 'oả',
                         'òe': 'oè', 'óe': 'oé', 'ọe': 'oẹ', 'õe': 'oẽ', 'ỏe': 'oẻ',
                         'ùy': 'uỳ', 'úy': 'uý', 'ụy': 'uỵ', 'ũy': 'uỹ', 'ủy': 'uỷ'}
    text = re.sub(r'(?P<id>{})'.format('|'.join(change_phone_dict.keys())),
                  lambda x: change_phone_dict[x.group('id')], text)

    return text
    
def split_compound_NSWs(text):
    list_tokens = text.split()
    for i, token in enumerate(list_tokens):
        # nếu token là NSW
        if token.lower() not in list_vietnamese_words:
            if re.match(email_regex, token) or re.match(url_regex, token):
                #print(token)
                continue
            # nếu không phải punctuation, word riêng lẻ hoặc lớp số thì phân tách
            if not re.match(r'^({}|[{}]+|\d+|((\d+({}))+\d+))$'.format(punc, charset, punc), token):
                token = re.sub(r'(?P<id>{})'.format(punc),
                               lambda x: ' ' + x.group('id') + ' ', token)
                token = re.sub(r'(?P<id>(\D\d)|(\d\D))',
                               lambda x: x.group('id')[0]+' '+x.group('id')[1], token)
                token = re.sub(r'(?P<id>(\D\d)|(\d\D))',
                               lambda x: x.group('id')[0]+' '+x.group('id')[1], token)
                token = re.sub(r'(?P<id>(\d[{}]))'.format(charset),
                               lambda x: x.group('id')[0]+' '+x.group('id')[1], token)

                token = ' '.join(token.split())
                list_tokens[i] = token
    
    text = ' '.join(list_tokens)
    return text

def edit_token(text):
    list_tokens = text.split()
    for i, token in enumerate(list_tokens):
        if re.match(r'([0-9])', token):
            if ('/' in token) and (',' in token):
                list_tokens[i] = re.sub(r'\,',' , ',token)
            elif ('/' in token) and (':' in token):
                list_tokens[i] = re.sub(r'\:', ' : ', token)
            elif ('/' in token) and ('-' in token) and (('.' in token) or (',' in token)):
                list_tokens[i] = re.sub(r'\-', ' đến ', token)
            elif ('.' in token) and (',' in token):
                list_tokens[i] = re.sub(r'\,', ' , ', token)
            elif ('-' in token):
                token_ = token.split('-')
                for j in range(len(token_)):
                    if re.match(r'[a-zA-Z]', token_[j]):
                        list_tokens[i] = re.sub(r'\-', ' - ', token)
                    elif token_[j] == '':
                        list_tokens[i] = re.sub(r'\-', ' - ', token)
        else:
            if '-' in token:
                token_ = token.split('-')
                for j in range(len(token_)):
                    if re.match(r'([0-9])', token_[j]):
                        list_tokens[i] = re.sub(r'\-', ' - ', token)
                    elif token_[j] == '':
                        list_tokens[i] = re.sub(r'\-', ' - ', token)
    text = ' '.join(list_tokens)
    return text

def get_token(text):
    list_token = []
    text = text.split()
    for i, token in enumerate(text):
        NSWs_word = []
        token_ = token.lower()
        if token_ not in list_vietnamese_words:
            if i == 0:
                env = ' '.join(text[i:i+3])
            elif i == 1:
                env = ' '.join(text[i-1:i+3])
            elif i >= len(text) - 2: 
                env = ' '.join(text[i-2:])
            else:
                env = ' '.join(text[i-2:i+3])
            NSWs_word.append(token)
            NSWs_word.append(env)
            list_token.append(NSWs_word)
        else:
            env = ''
            NSWs_word.append(token)
            NSWs_word.append(env)
            list_token.append(NSWs_word)
    return list_token

def convert_text(text):
    text = re.sub('–','-',text)
    text = re.sub('\r',' gachcheor ',text)
    text = re.sub('\t',' gachcheot ',text)
    
    text = split_compound_NSWs(text)
    text = split_token(text)
    
    text = re.sub('gachcheor', ' , ', text)
    text = re.sub('gachcheot', ' , ', text)
    
    text = edit_token(text)
    list_token = get_token(text)
    return list_token