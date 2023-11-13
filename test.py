# 测试播放WsFinish.wav和单词
import gradio as gr
import random 
import os
from pydub import AudioSegment
import numpy as np
gr.close_all()

def f():
    if random.randint(0,10) % 2 == 0:
        Finish = AudioSegment.from_file('/mnt/e/Projects/ReciteWord/Sounds/avaricious.mp3')
        Wordwav = AudioSegment.from_file('/mnt/e/Projects/ReciteWord/Sounds/WsFinish.wav')
        Finish = Finish.set_frame_rate(Wordwav.frame_rate)
        Answer = Finish + Wordwav
        Answer = np.array(Answer.get_array_of_samples(), dtype=np.float16)
        return '偶数', (Wordwav.frame_rate, Answer)
    else:
        return '奇数', '/mnt/e/Projects/ReciteWord/Sounds/avaricious.mp3'

with gr.Blocks() as demo:
    tx = gr.TextArea(value='0')
    audio = gr.Audio(autoplay=True)

    bt = gr.Button(value='button')

    bt.click(fn=f, outputs=[tx, audio])
    
demo.launch(server_port=7860, inbrowser=True)

os._exit(0)


# 测试从文本读入单词
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


