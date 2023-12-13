import json
import os

from functions import get_name

doc_path = r'c:\Users\stat\Documents'
from_file_en = os.path.join(doc_path, r'_english.txt')
from_file_ru = os.path.join(doc_path, r'orig_gpt_to_Russian.txt')
save_file = os.path.join(doc_path, r'orig_gpt_en_ru.txt')
with open(from_file_en, 'r', encoding='utf8') as f:
    all_lines_en = f.read().strip().split('\n')
print('all lines en: ' + str(len(all_lines_en)))
with open(from_file_ru, 'r', encoding='utf8') as f:
    all_lines_ru = f.read().strip().split('\n\n')
print('all lines ru: ' + str(len(all_lines_ru)))


out_list = []
ix = 0
for line_en in all_lines_en:
    ix += 1
    tmp = json.loads(line_en)
    crypto_name = tmp['crypto']
    about_en = tmp['about']
    out_dict = {
        "crypto": crypto_name,
        "about": {
            'en': about_en,
    }   }
    for line_ru in all_lines_ru:
        crypto_ru = json.loads(line_ru)['crypto']
        if crypto_name == crypto_ru:
            out_dict['about']['ru'] = json.loads(line_ru)['about']
            all_lines_ru.remove(line_ru)
            break

    output = json.dumps(out_dict, ensure_ascii=False)
    out_list.append(output)
print('all_lines_ru: ', len(all_lines_ru))
with open(save_file, 'w', encoding='utf8') as f:
    f.write('\n\n'.join(out_list))
