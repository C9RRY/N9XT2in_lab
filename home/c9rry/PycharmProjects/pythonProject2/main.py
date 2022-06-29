import json

import requests

WORD_CASE_API_URL = 'https://antebe.pythonanywhere.com'
CLERICALISM_DICT = {
    "на сьогоднішній день": "сьогодні", "проявляти бажання": "бажати",
    "в результаті ретельного розслідування": "розслідуючи", "переживати стан занепокоєння": "хвилюватися"
}


def emotionify(incorrect_sentence):
    incorrect_sentence_modified = incorrect_sentence.replace(',', ' ,')
    incorrect_sentence_modified = incorrect_sentence_modified.replace('.', ' *')
    incorrect_sentence_modified = list(incorrect_sentence_modified.split(' '))
    word_case_dict = {}
    incorrect_sentence_with_inf = ''

    for word in incorrect_sentence_modified:
        r = requests.get(f'{WORD_CASE_API_URL}/Noun/{word}/N')
        word_case = r.json()
        if word_case['inflection'] is None:
            r = requests.get(f'{WORD_CASE_API_URL}/Verb/{word}/Inf')
            word_case = r.json()
        print(word_case)
        word_case_dict[word_case['default/new_inflection']] = word_case['input']
        if word_case['inflection'] is not None:
            incorrect_sentence_with_inf += word_case['default/new_inflection'] + ' '
        else:
            incorrect_sentence_with_inf += word_case['input'] + ' '

    for key in CLERICALISM_DICT.keys():
        if key in incorrect_sentence_with_inf:
            incorrect_sentence_with_inf = incorrect_sentence_with_inf.replace(key, CLERICALISM_DICT[key])
        elif key in incorrect_sentence_with_inf.lower():
            incorrect_sentence_with_inf = incorrect_sentence_with_inf.replace(
                key.capitalize(), CLERICALISM_DICT[key].capitalize())
    for inf_word in word_case_dict.keys():
        incorrect_sentence_with_inf = incorrect_sentence_with_inf.replace(inf_word, word_case_dict[inf_word])

    correct_sentence = incorrect_sentence_with_inf
    correct_sentence = correct_sentence.replace(' ,', ',')
    correct_sentence = correct_sentence.replace(' *', '.')
    return correct_sentence


incorrect_sentence1 = "В результаті ретельного розслідування злочину детектив заявив," \
                      " що на сьогоднішній день неможливо знайти злодія. Світлана проявляє бажання вступити в КНУ."

print(emotionify(incorrect_sentence1))



# incorrect uppercase
# incorrect case
