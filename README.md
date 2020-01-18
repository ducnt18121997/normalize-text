# Normalize-text for TTS


| Features          | Tutorials               |
| ----------------- |:----------------------- |
| GitHub Sync       | [:link:][GitHub-Sync] https://github.com/ducnt18121997/normalize-text|

[GitHub-Sync]: https://github.com/ducnt18121997/normalize-text

- chạy create_dict để tạo bộ từ điển đọc từ tiếng anh
- normalize_text là hàm chính

## 1. Requirements

- num2words
- beautifulsoup4
- lxml
- pronouncing
- tqdm
- unicodedata

## 2. Function
- config: chứa các dict và rule để phân loại và đọc các từ dạng NSW
- create_dict: tạo thư viện đọc từ tiếng anh
- en2vi: hàm xây dựng âm tiết với các từ tiếng anh (hiện đang sử dụng en2vi_old)
- spit_token: tách riêng các NSW và các từ đọc được
- expand_NSWs: hàm đọc các loại NSW đã phân loại
- classify_token: hàm phân loại các NSW
- replace: thay thế các NSW sang dạng đọc được
- normalize-text: main

## 3. Maintain
- config: thêm dict, rule
- split_token: tách các token là NSW và các từ đọc được bằng regrex
- expand_NSWs: diễn giải các NSWs theo từng dạng được phân loại
- classify_token: phân loại các NSW vào 3 group và 21 category
- folder dicts: chứa các thư viện sử dụng khi diễn giải NSWs và được đặt tên theo các dạng NSW từ file normalize_text.doc

## 4. Update
- update(2/1/2020): thêm bộ phân loại NSWs
- update(9/1/2020): chỉnh sửa bộ đọc các NSWs
