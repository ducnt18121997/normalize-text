#last_fix: 15:00 5/1/2020
# encoding: utf-8
import re
from config import *
from split_token import convert_text
from classify_token import classify_text
from replace_token import replace

def normalize_para(text):
    list_token = convert_text(text)
    list_label = classify_text(list_token)
    normalized_text, list_normalized_text = replace(list_token, list_label)
    for i in range(len(list_token)):
        if list_label[i][0] != 'NOT_NSWs':
            print(list_token[i][0] + '|' + list_label[i][1] + '|' + list_normalized_text[i])
    normalized_text = ' '.join(normalized_text.split())
    return normalized_text

def normalize(text):
    separator = '\n'
    text = text.split(separator)
    #print(text)
    for i in range(len(text)):
        text[i] =  normalize_para(text[i])
    #giữ lại \n
    text = '\n'.join(text)
    
    # chuyển \n thành chấm nếu cuối câu không chấm
    text = re.sub(r'\n', ' . ', text)
    text = re.sub(r'(\s*)(\.|\,|\…|\;)(\s*)\.', ' .', text)
    text = re.sub(r'(\s*)(\.|\,|\…|\;)(\s*)\.', ' .', text)

    text = ' '.join(text.split())
    return text

text = open('./vidu_1.txt').read()
text = normalize(text)
print(text)