# -*- coding: utf-8 -*-

def load_dict(dict_path):
    """ Load dictionary \n 
    File dict: key|value\n
    Return dict
    """
    dict_ = {}
    with open(dict_path, 'r', encoding='utf-8') as file_:
        content = file_.read()
        rows = content.split('\n')
        for row in rows:
            if row == '':
                continue
            key = row.split('|')[0].strip()
            value = row.split('|')[1].strip()
            dict_[key] = value

    return dict_ 
