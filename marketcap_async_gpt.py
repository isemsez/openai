import json
import logging
import os.path
import time
from datetime import datetime
from functions import get_description, get_name
import asyncio
from openai import AsyncOpenAI



async def handle_crypto() -> None:
    question = ('I have a text which is a description of a cryptocurrency. Can you paraphrase this description? The '
                'description is below:\n' + about)
    for i in range(3):
        try:
            chat_completion = await client.chat.completions.create(
                messages=[{"role": "user", "content": question}],
                model="gpt-3.5-turbo",
            )
            modified_description = chat_completion.choices[0].message.content
            break
        except Exception as e:
            if i < 2:
                logging.warning( ' ' + type(e).__name__ + ': ' + str(e))
                time.sleep(20)
                continue
            raise Exception
    output = {"crypto": crypto_name, "about": modified_description}
    with open(save_file, 'a+', encoding='utf8') as f:
        f.write(json.dumps(output, ensure_ascii=False) + '\n\n')



client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

doc_path = r'c:\Users\stat\Documents'
from_file = os.path.join(doc_path, r'marketcap.txt')
save_file = os.path.join(doc_path, r'marketcap_modified.txt')

with open(from_file, 'r', encoding='utf8') as f:
    all_lines = f.read().strip().split('\n\n\n')
    print('all cryptos: ' + str(len(all_lines)))

with open(save_file, 'r', encoding='utf8') as f:
    already_downloaded1 = f.read().strip('\n').split('\n')
    already_downloaded2 = list(filter(lambda line: len(line) > 0, already_downloaded1))
    already_downloaded = list(map(lambda line: get_name(line), already_downloaded2))

ix = 0
for line in all_lines:
    ix += 1
    [crypto_name, about] = line.split('   ', 1)
    if crypto_name in already_downloaded or len(about.strip()) <= 15:
        continue
    print(datetime.now().strftime("%H:%M:%S") + '  >  ' + crypto_name + ' - ' + str(ix))

    asyncio.run( handle_crypto() )
    time.sleep(1)
