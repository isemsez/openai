import os
import subprocess
from datetime import datetime
from functions import *

doc_path = r'c:\Users\stat\Documents'
with open(os.path.join(doc_path, 'crypto_descriptions.txt'), 'r', encoding='utf8') as f:
    raw_content = f.read().strip('\n').split('\n')

all_crypto_lines = list(filter(lambda line: len(line) > 0, raw_content))
print('all_cryptos: ' + str(len(all_crypto_lines)))

[good, suspicious, pie] = filter_bad(all_crypto_lines)
print('pie %s' % pie)

try:
    os.remove(os.path.join(doc_path, '_good.txt'))
    os.remove(os.path.join(doc_path, '_suspicious.txt'))
    os.remove(os.path.join(doc_path, '_bad.txt'))
except FileNotFoundError:
    pass

with open(os.path.join(doc_path, '_good.txt'), 'w', encoding='utf8') as f:
    f.write('\n\n'.join(good))

bad_file = os.path.join(doc_path, '_suspicious.txt')
with open(bad_file, 'w', encoding='utf8') as f:
    f.write('\n\n'.join(suspicious))

subprocess.run(r'C:\Program Files\Notepad++\notepad++.exe ' + bad_file)
