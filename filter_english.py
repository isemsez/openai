import os
import re
import subprocess
from datetime import datetime
from functions import *

doc_path = r'c:\Users\stat\Documents'
with open(os.path.join(doc_path, 'crypto_descriptions.txt'), 'r', encoding='utf8') as f:
    raw_content = f.read().strip('\n').split('\n')

all_crypto_lines = list(filter(lambda line: len(line) > 0, raw_content))
print('all cryptos: ' + str(len(all_crypto_lines)))


eng_file = os.path.join(doc_path, '_english.txt')
try:
    os.remove(eng_file)
except FileNotFoundError:
    pass

eng_descriptions = filter_english(all_crypto_lines)

if len(eng_descriptions) > 0:
    with open(eng_file, 'w', encoding='utf8') as f:
        f.write('\n'.join(eng_descriptions))
    subprocess.run(r'C:\Program Files\Notepad++\notepad++.exe ' + eng_file)
print(f'{len(eng_descriptions)} lines written.')
