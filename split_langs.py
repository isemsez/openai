import os
import subprocess
from datetime import datetime
from functions import *

doc_path = r'c:\Users\stat\Documents'
with open(os.path.join(doc_path, '_good.txt'), 'r', encoding='utf8') as f:
    raw_content = f.read().strip('\n').split('\n')

good_cryptos = list(filter(lambda line: len(line) > 0, raw_content))
print('good_cryptos: ' + str(len(good_cryptos)))

output = ''
for line in good_cryptos:
    translations = json.loads(line)['about']
    output += translations + '\n\n\n\n\n\n'

file = os.path.join(doc_path, 'temp.txt')
with open(file, 'w', encoding='utf8') as f:
    f.write(output)
subprocess.run(r'C:\Program Files\Notepad++\notepad++.exe ' + file)
