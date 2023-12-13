import json
import logging
import os.path
import time
from datetime import datetime
from functions import get_description, get_name

doc_path = r'c:\Users\stat\Documents'
from_file = os.path.join(doc_path, r'_english.txt')
save_file = os.path.join(doc_path, r'orig_gpt_to_Russian.txt')
with open(from_file, 'r', encoding='utf8') as f:
    all_lines = f.read().strip().split('\n')
    print('all cryptos en: ' + str(len(all_lines)))

already_downloaded = []
if os.path.exists(save_file):
    with open(save_file, 'r', encoding='utf8') as f:
        lines = f.read().strip('\n').split('\n\n')
        already_downloaded = list(map(lambda line: get_name(line), lines))

ix = 0
for line in all_lines:
    ix += 1
    tmp = json.loads(line)
    crypto_name = tmp['crypto']
    about = tmp['about']
    if crypto_name in already_downloaded:
        continue
    print(datetime.now().strftime("%H:%M:%S") + '  >  ' + crypto_name + ' - ' + str(ix))

    question = ('I have a text which is a description of a cryptocurrency. Can you translate it to Russian? The '
                'description is below:\n' + about)
    for i in range(10):
        try:
            russified_description = get_description(question)
            break
        except Exception as e:
            if i < 2:
                logging.warning( ' ' + type(e).__name__ + ': ' + str(e))
                time.sleep(20)
                continue
            raise e

    output = {"crypto": crypto_name, "about": russified_description}
    with open(save_file, 'a+', encoding='utf8') as f:
        f.write(json.dumps(output, ensure_ascii=False) + '\n\n')
