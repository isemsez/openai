import time
from datetime import datetime

import openai

from functions import *
import json


with open(r'c:\Users\stat\Documents\logos.txt', 'r', encoding='utf8') as f:
    cryptos = f.read().strip('\n').split('\n')
print('cryptos length: ' + str(len(cryptos)))

saved_file = r'c:\Users\stat\Documents\crypto_descriptions.txt'
with open(saved_file, 'r', encoding='utf8') as f:
    already_downloaded1 = f.read().strip('\n').split('\n')
    already_downloaded2 = list(filter(lambda line: len(line) > 0, already_downloaded1))
    already_downloaded3 = list(map(lambda line: get_name(line), already_downloaded2))

to_download = [x for x in cryptos if x not in already_downloaded3]
print('to download length: ' + str(len(to_download)))

ix = 0
for crypto in to_download:
    ix += 1
    print(datetime.now().strftime("%H:%M:%S") + '  >  ' + crypto + ' - ' + str(ix))
    question = 'Tell me about ' + crypto + ' cryptocurrency. If you don\'t have specific information on the cryptocurrency don\'t write anything just "No info".'

    for i in range(3):
        try:
            about = get_description(question)
        except openai.APIConnectionError:
            if i < 2:
                print('Was "openai.APIConnectionError"')
                time.sleep(20)
                continue
            raise openai.APIConnectionError
        except Exception:
            if i < 2:
                print('Was some exception.')
                time.sleep(60)
                continue
            raise openai.APIConnectionError

    output = {"crypto": crypto, "about": about}
    with open(saved_file, 'a+', encoding='utf8') as f:
        f.write(json.dumps(output, ensure_ascii=False) + '\n\n')
