import json
import os

from functions import get_name

doc_path = r'c:\Users\stat\Documents'
from_file_en = os.path.join(doc_path, r'marketcap_gpt_Russian.txt')
from_file = os.path.join(doc_path, r'marketcap_gpt_Russian.txt')
save_file = os.path.join(doc_path, r'marketcap_gpt_Russian_new.txt')
with open(from_file, 'r', encoding='utf8') as f:
    all_lines = f.read().strip().split('\n\n')
print('all lines: ' + str(len(all_lines)))

netto_list = list(set(map(lambda line: get_name(line), all_lines)))




already_added = []
out_list = []
ix = 0
for line in all_lines:
    ix += 1
    tmp = json.loads(line)
    crypto_name = tmp['crypto']
    about = tmp['about']
    if crypto_name in already_added:
        continue
    output = json.dumps( {"crypto": crypto_name, "about": about}, ensure_ascii=False )
    out_list.append(output)
    already_added.append(crypto_name)
print(len(out_list))
with open(save_file, 'w', encoding='utf8') as f:
    f.write('\n\n'.join(out_list))
