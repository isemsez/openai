import json
import re
from openai import OpenAI


def get_description(question: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    return completion.choices[0].message.content


def get_name(line):
    return json.loads(line)['crypto']


def filter_bad(all_lines: list) -> list:
    good_results = []
    bad_results = []
    bad_about = []
    bad_i = []
    bad_please = []
    bad_gertr = []
    bad_note = []
    bad_know_ru = []
    bad_know_gr = []
    ix = ig = 0
    for line in all_lines:
        ix += 1
        if '"about": "-"' in line:
            bad_about.append(line)
            continue
        if 'please'.casefold() in line.casefold():
            bad_please.append(line)
            continue
        if re.search(r'\bне знаю\b', line):
            bad_know_ru.append(line)
            continue
        if re.search(r'weiß (es )?nicht', line):
            bad_know_gr.append(line)
            continue
        if re.search(r'\bI\b', line):
            bad_i.append(line)
            continue
        if re.search(r'Note: ', line):
            bad_note.append(line)
            continue
        if re.search(r'German[^:( Translation)]', line):
            bad_gertr.append(line)
            continue
        good_results.append(line)
        ig += 1
    pie = round(ig / ix * 100)
    bad_results = bad_about + ['\n'] + bad_gertr + ['\n'] + bad_note + ['\n'] + bad_i + ['\n'] + bad_know_ru + ['\n'] \
                  + bad_know_gr + ['\n'] + bad_please
    return [good_results, bad_results, pie]


def find_ru(translations):
    string_s = r'^(- )?(Translation to Russian:|Russian [Tt]ranslation:|In Russian:)'
    translations2 = re.subn('^Translation')


def filter_english(all_crypto_lines):
    eng_descriptions = []
    for crypto in all_crypto_lines:
        name = get_name(crypto)
        description = json.loads(crypto)['about']
        if description == '-':
            continue
        all_lines = description.split('\n')
        eng_description = ''
        for line in all_lines:
            if len(line) == 0:
                continue
            if (
                    re.search(r'[а-я]', line)
                    or re.search(r'\bRussian\b|\bGerman\b|\byou\b|\bmy\b|Note: |\bplease\b|\bno info|\bit\'s\b|'
                                 r'\bas of\b|\bto note\b|\bit is important to\b|\bto conduct [^\.]*?research\b|'
                                 r'it is [^\.]*?research|consider\b|Translation:', line, re.IGNORECASE)
                    or re.search(r'\bI\b', line)
            ):
                break
            eng_description += line + '\n\n'
        eng_description = eng_description.rstrip('\n')

        if eng_description != 'No info.' and eng_description != 'No info' and eng_description != '':
            crypto_in_json = json.dumps({'crypto': name, 'about': eng_description})
            eng_descriptions.append(crypto_in_json)
    return eng_descriptions






