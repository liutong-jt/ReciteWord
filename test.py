import re

line = 'asfslfjl ：;:舒服:啦'
matched = re.match(r'[a-zA-Z]+', line)
English_start, English_end = matched.start(), matched.end()
English = line[English_start:English_end]
chinese = re.sub(r'^[\s:：；;]+', '', line[English_end:])
print(English, chinese)

from read_from_raw import read_word_from_standard_text
from Word import Word

Word_lists = read_word_from_standard_text('save_text.txt')
other_words = read_word_from_standard_text('other_word.txt')

word_dict = {}
new_word_list = []
for i, word in enumerate(Word_lists + other_words):
    English = word.English
    if English in word_dict:
        print('      WORD:  ', word.to_repr(), end='')
        print('DICT[WORD]:  ', word_dict[English].to_repr())
    else:
        word_dict[English] = word
        new_word_list.append(word)

print('debug')



with open('save_text2.txt', 'w', encoding='utf8') as f:
    for w in new_word_list:
        print(w.to_repr(), file=f)

print(new_word_list[0].to_repr())



# word = Word('ingress')
# if word in Word_lists:
#     print('ol')

#     idx = Word_lists.index(word)
#     print(idx, Word_lists[idx].to_repr())


