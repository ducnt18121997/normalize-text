# -*- coding: utf-8 -*-
import os
import pronouncing

from utils import load_dict

CURDIR = os.path.dirname(__file__)

LSEQ_DICT_PATH = os.path.join(CURDIR, 'dicts/LSEQ_DICT.txt')
EN2VI_DICT_PATH = os.path.join(CURDIR, 'dicts/EN2VI_DICT.txt')
EN2WORD_DICT_PATH = os.path.join(CURDIR, 'dicts/EN2WORD_DICT.txt')
ABB_DICT_PATH = os.path.join(CURDIR, 'dicts/ABB_DICT.txt')
PUNC_DICT_PATH = os.path.join(CURDIR, 'dicts/PUNC_DICT.txt')
CURRENCY_DICT_PATH = os.path.join(CURDIR, 'dicts/CURRENCY_DICT.txt')
UNIT_DICT_PATH = os.path.join(CURDIR, 'dicts/UNIT_DICT.txt')
PERSON_DICT_PATH = os.path.join(CURDIR, 'dicts/proper_name/PERSON_DICT.txt')
BRANCH_DICT_PATH = os.path.join(CURDIR, 'dicts/proper_name/BRANCH_DICT.txt')

VI_WORDS_PATH = os.path.join(CURDIR, 'dicts/vietnamese_words.txt')

LSEQ_DICT = load_dict(LSEQ_DICT_PATH)
EN2VI_DICT = load_dict(EN2VI_DICT_PATH)
ABB_DICT = load_dict(ABB_DICT_PATH)
PUNC_DICT = load_dict(PUNC_DICT_PATH)
CURRENCY_DICT = load_dict(CURRENCY_DICT_PATH)
UNIT_DICT = load_dict(UNIT_DICT_PATH)
PERSON_DICT = load_dict(PERSON_DICT_PATH)
BRANCH_DICT = load_dict(BRANCH_DICT_PATH)

LSEQ = list(LSEQ_DICT.keys())
LWRD = list(EN2VI_DICT.keys())
LABB = list(ABB_DICT.keys())
PUNC = list(PUNC_DICT.keys())
MONY = list(CURRENCY_DICT.keys())
UNIT = list(UNIT_DICT.keys())
PERSON = list(PERSON_DICT.keys())
BRANCH = list(PERSON_DICT.keys())

POPULAR_EN2VI_DICT_PATH = os.path.join(CURDIR,  'dicts/popular_english_words.txt')
CMUPHONE2VI_DICT_PATH = os.path.join(CURDIR,  'dicts/cmu_phones.txt')

cmuphone2vi_dict = load_dict(CMUPHONE2VI_DICT_PATH)
popular_en2vi_dict = load_dict(POPULAR_EN2VI_DICT_PATH)
popular_en2word_dict = load_dict(EN2WORD_DICT_PATH)
popular_branch_dict = load_dict(BRANCH_DICT_PATH)
popular_person_dict = load_dict(PERSON_DICT_PATH)


popular_en2vi_dict.update(popular_branch_dict)
popular_en2vi_dict.update(popular_person_dict)
popular_en2vi_dict.update(EN2VI_DICT)

list_enwords = pronouncing.cmudict.words()
list_enwords.extend(popular_en2vi_dict.keys())

charset = 'aáảàãạâấẩầẫậăắẳằẵặbcdđeéẻèẽẹêếểềễệfghiíỉìĩịjklmnoóỏòõọôốổồỗộơớởờỡợpqrstuúủùũụưứửừữựvwxyýỷỳỹỵzAÁẢÀÃẠÂẤẨẦẪẬĂẮẲẰẴẶBCDĐEÉẺÈẼẸÊẾỂỀỄỆFGHIÍỈÌĨỊJKLMNOÓỎÒÕỌÔỐỔỒỖỘƠỚỞỜỠỢPQRSTUÚỦÙŨỤƯỨỬỪỮỰVWXYÝỶỲỸỴZ'
email_regex = r'[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4})+'
url_regex = r'((?:http(s)?:\/\/)|(www))[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+'
short_url = r'([\w.-]+(?:\.[\w\.-]+)+)?[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+(\.(com|gov|vn|com|org|info|io|net|edu))+'
url_regex += '|' + short_url
punc = r'\.|\,|\…|\;|\/|\(|\)|\!|\?|\'|\"|\“|\”|\:|\-|\+|\*|\\|\_|\&|\%|\^|\[|\]|\{|\}|\=|\#|\@|\`|\~|\$'
unitlist = '|'.join(UNIT)
lseq_charset = '|'.join(LSEQ)

f = open(VI_WORDS_PATH, 'r', encoding='utf-8')
list_vietnamese_words = f.read().split('\n')
vn_words_dict = dict.fromkeys(list_vietnamese_words, 0)
f.close()

currency_list = '\$|S\$|SGD|VND|USD|VNĐ|USĐ|€|£|¥|Fr'

punc_dura = ['.', ',', ';', '!', '-', '?', ':', "'", '"', '“', '”', '*', '…', '(', ')', '[', ']', '{', '}', '~', '`', '_']
punc_read = [ '/', '+', '&', '%', '^', '$', '#', '@', '<', '>', '=', '\\']

classes = ['NTIM', 'NDAT', 'NDAY', 'NMON', 'NNUM', 'NTEL', 'NDIG', 'NSCR', 'NRNG', 'NPER', 'NFRC', 'NADD', 
           'LWRD', 'LSEQ', 'LABB',
           'PUNC', 'URLE', 'MONY', 'CSEQ', 'DURA', 'NONE']

#Token xung quanh NSWs
#NSWs chứa /
N_Space = ['ở', 'địa', 'điểm', 'nhà', 'nằm', 'chỗ', 'tại', 'nơi', 'ngõ', 'đường', 'phố', 'huyện', 'tỉnh', 'thành', 'phố'] 
N_Time = ['nhân', 'dịp', 'vào', 'tới', 'ngày', 'tháng', 'năm', 'khoảng', 'lúc', 'từ', 'đến', 'hôm', 'nay', 'mai' , 'kia', 'qua', 'sáng', 'trưa', 'chiều', 'tối', 'đêm', 'khuya', 'hai', 'ba', 'tư', 'năm', 'sáu', 'bảy', 'chủ', 'nhật', 'tuần']
N_Frc = ['vượt', 'của','bằng', 'tỷ' , 'tỉ', 'lệ', 'trung', 'bình', 'cập', 'nhật', 'số', 'kết', 'quả', 'khoảng', 'chiếm', 'đạt', 'được', 'có', 'nghị', 'định', 'quyết']
N_T_Spec = ['1/1', '14/2', '8/3', '30/4', '1/5', '1/6', '27/7', '2/9', '20/10', '20/11', '22/12']
#NSWs là số
N_Dig = ['mã', 'id']
N_Tel = ['sđt', 'điện', 'thoại', 'phone', 'tele', 'telephone']
N_1st_Tel = ['0162', '0163', '0164', '0165', '0166', '0167', '0168', '0169', '032', '033', '034', '035', '036', '037', '038', '039', '0120', '0121', '0122', '0126', '0128', '070', '079', '077', '076', '078', '0123', '0124', '0125', '0127', '0129', '083', '084', '085', '081', '082']
#NSWs chứa - 
N_Scr = ['trận', 'tranh', 'tỉ', 'kết', 'quả', 'thắng', 'thua', 'trước']
N_Rng = ['cấp', 'kì', 'kỳ' , 'có', 'từ', 'mức', 'giây', 'giờ', 'phút', 'ngày', 'tháng', 'năm', '(', ')', 'trong', 'vòng', 'thập', 'niên', 'giai', 'đoạn', 'gấp', 'lần', 'tuổi', 'lệ', 'khoảng', 'ở', 'km', 'm', 'g', 'kg', 'từ', 'mm', 'cm']
#NSWs dạng tiền
Money = ['$', 'S$', 'D', 'VND', 'USD', 'VNĐ', 'USĐ', '€', '£', '¥', 'Fr']
#NSWs của dạng lwrd
L_Person = ['ông', 'bà', 'anh', 'chị']