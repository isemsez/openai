import json
import logging
import os
import time
from datetime import datetime
from functions import get_name, get_description

doc_path = r'c:\Users\stat\Documents'
from_file_mcap = os.path.join(doc_path, r'orig_marketcap_en_ru.txt')
from_file_gpt = os.path.join(doc_path, r'orig_gpt_en_ru.txt')
save_file = os.path.join(doc_path, r'gpt_mcap_de.txt')
with open(from_file_mcap, 'r', encoding='utf8') as f:
    all_lines_mcap = f.read().strip().split('\n\n')
print('all lines mcap: ' + str(len(all_lines_mcap)))
with open(from_file_gpt, 'r', encoding='utf8') as f:
    all_lines_gpt = f.read().strip().split('\n\n')
print('all lines gpt: ' + str(len(all_lines_gpt)))
all_lines = all_lines_gpt + all_lines_mcap
print('all lines: ', len(all_lines))

already_downloaded = []
if os.path.exists(save_file):
    with open(save_file, 'r', encoding='utf8') as f:
        lines_de = f.read().strip('\n').split('\n\n')
        already_downloaded = list(map(lambda line: get_name(line), lines_de))

ix = 0
for line in all_lines:
    ix += 1
    tmp = json.loads(line)
    crypto_name = tmp['crypto']
    if crypto_name in already_downloaded:
        continue
    about_en = tmp['about']['en']
    print(datetime.now().strftime("%H:%M:%S") + '  >  ' + crypto_name + ' - ' + str(ix))

    question = ('I have a text which is a description of a cryptocurrency. Can you translate it to German? The '
                'description is below:\n' + about_en)
    for i in range(10):
        try:
            german_description = get_description(question)
            break
        except Exception as e:
            if i < 9:
                logging.warning( ' ' + type(e).__name__ + ': ' + str(e))
                time.sleep(20 if i < 5 else 60)
            else:
                raise e
    out_dict = {
        "crypto": crypto_name,
        "about": { 'de': german_description },
    }
    output = json.dumps(out_dict, ensure_ascii=False)
    with open(save_file, 'a+', encoding='utf8') as f:
        f.write(output + '\n\n')
