import gradio as gr
from read_from_raw import read_word_from_standard_text
from Word import Word, check_illeagal_word
from config import *
import re, os
# from pygame import mixer 

def prev_word():
    global WORD, index
    index -= 1
    word = WORD[ index % len(WORD) ]
    return word.English, word.to_repr()

def next_word():
    global WORD, index
    index += 1
    word = WORD[ index % len(WORD) ]
    return word.English, word.to_repr()

def tab1_modify_word(inputs):
    '''
        修改直接覆盖当前索引单词
        可以修改当前英语单词
    '''
    global WORD, index
    try:
        check_illeagal_word(inputs)
        word = Word().from_str(inputs)
        WORD[ index % len(WORD) ] = word
        # 判断是否有派生词
        derivative = getattr(word, config['派生词'])
        if derivative:
            derivative_words = re.split('[,，；;\s]+', derivative)
            for w in derivative_words:
                if w != '' and w not in WORD:
                    WORD.append(Word(English=w))
        result = WORD[ index % len(WORD) ].to_repr()
        return f'{result}\n\n{index % len(WORD)}'
    except AssertionError as e:
        return '\n\n'.join(['[Error]: 单词格式错误', str(e),inputs])

def tab3_modify_word(inputs):
    '''
        不可直接覆盖当前索引单词
        先搜索单词，找到该单词的索引再修改
        #TODO: 有bug
    '''
    global WORD, index
    try:
        check_illeagal_word(inputs)
        word = Word().from_str(inputs)
        idx = WORD.index(word.English)
        WORD[ idx % len(WORD) ] = word
        # 判断是否有派生词
        derivative = getattr(word, config['派生词'])
        if derivative:
            derivative_words = re.split('[,，；;\s]+', derivative)
            for w in derivative_words:
                if w != '' and w not in WORD:
                    WORD.append(Word(English=w))

        result = word.to_repr()
        return f'{result}\n\n{idx % len(WORD)}'
    except AssertionError as e:
        return '\n\n'.join(['[Error]: 单词格式错误', str(e),inputs])

def save_all_word_to_text():
    global WORD
    with open(dictionary_path, 'w', encoding='utf8') as f:
        for w in WORD:
            print(w.to_repr(), file=f)

def add_new_word(inputs):
    print("IIIIII AMAMMAMAMAM ININININI add_new_word")
    global WORD
    try:
        check_illeagal_word(inputs)
        word = Word().from_str(inputs)
        print(word.to_repr())
        search_ans = search_word(word.to_repr())
        # if not search_ans.startswith('[Error]'):   # 为什么会进入到这里
        #     return word.to_repr()
        if word not in WORD:
            WORD.append(word)
            result = f'已成功添加单词:\n{word.to_repr()}' 
        else:
            idx = WORD.index(word)
            word = WORD[idx]
            result = f'词库已存在该单词:\n{word.to_repr()}'
            print(result)
        return f'{result}\n\n当前词库数量为:{len(WORD)}'
    except AssertionError as e:
        return '\n\n'.join(['[Error]: 单词格式错误', str(e), inputs])
    
def search_word(inputs):
    global WORD
    try:
        word = Word().from_str(inputs)
        for w in WORD:
            if w.English == word.English:
                result = w.to_repr()
                return f'{result}'
        return f'[Error]: 没有找到单词 {word.English}'
    except AssertionError as e:
        return '\n\n'.join(['[Error]: 单词格式错误', str(e), inputs])
    except  AttributeError as e:
        return '\n\n'.join(['[Error]: 没有该单词', str(e), inputs])


def clear_new_word():
    return new_word

def tab1_modify_init():
    global WORD, index
    result = WORD[index % len(WORD)].modify_init()
    return result

def tab3_modify_init(inputs):
    global WORD
    try:
        check_illeagal_word(inputs)
    except AssertionError as e:
        return e

    word = Word().from_str(inputs)
    if word in WORD:
        idx = WORD.index(word)
        word = WORD[idx]
    result = word.modify_init()
    return result

def play_autio():
    global WORD, index
    English = WORD[index].English
    audio_path = os.path.join(AUDIO_DIR, English[0].lower(), f'{English}.mp3')
    # mixer.init()
    # mixer.music.load(audio_path)
    # mixer.music.play()
    return audio_path


if __name__ == '__main__':
    WORD = read_word_from_standard_text(dictionary_path)
    index = 0
    index = WORD.index('austere')
    new_word = r'''English  :  汉语
[前缀]:
[后缀]:
[词根]:
[词源]:
[助记]:
[派生词]:
[联想]:
[用法]:
[近]:
[反]:
[释义]:
[形近词]:
[知识点]:'''




    with gr.Blocks() as demo:
        with gr.Tab("整理词库"):    # Tab 1
            tab1_word_label = gr.Label(label='当前单词')
            tab1_Word_Show = gr.Textbox(lines=10, label='单词', value=WORD[index % len(WORD)].to_repr())
            with gr.Row():
                tab1_bt_prev = gr.Button("Prev Word")
                tab1_bt_next = gr.Button("Next Word")
            with gr.Column():
                with gr.Row():
                    tag1_bt_modify_init = gr.Button('Modify Init')
                    tab1_bt_modify = gr.Button("Modify")
                tab1_bt_save = gr.Button("Save to text")
            tab1_audio = gr.Audio(autoplay=True)
        

        with gr.Tab("添加单词"):   # Tab 2
            tb_new_word = gr.Textbox(lines=20, label='新单词', value=new_word, placeholder=new_word)
            with gr.Row():
                tab2_bt_clear = gr.Button('Clear')
                tab2_bt_add = gr.Button('Add a new word')
                tab2_bt_search = gr.Button('Search a word')

        with gr.Tab('搜索单词'):   # Tab 3
            tab3_tb_search_word = gr.Textbox(lines=20, label='搜索', placeholder='English:')
            with gr.Row():
                tab3_bt_modify_init = gr.Button('Modify Init')
                tab3_bt_modify = gr.Button('Modify')
                tab3_bt_search = gr.Button('Search a word')

        with gr.Tab("背单词"):      # Tab 4
            with gr.Row(equal_height=False):
                with gr.Column(min_width="2000px"):
                    tab4_word_english = gr.Label("English")
                    tab4_word_info = gr.Textbox("中文\naslf\n1232", lines=8)
                    with gr.Row(min_width="100px"):
                        tab4_prev = gr.Button(label="上一个", value='上一个')
                        tab4_next = gr.Button(label="下一个", value='下一个')

                        # tab4_playaudio = gr.Button(label="听音频", value='听音频')
            tab4_audio = gr.Audio(autoplay=True, visible=True, interactive=False)
        # Tab 4
        tab4_word_english.change(fn=play_autio, outputs=tab4_audio)
        tab4_next.click(fn=next_word, outputs=[tab4_word_english, tab4_word_info])
        tab4_prev.click(fn=prev_word, outputs=[tab4_word_english, tab4_word_info])
        # tab4_playaudio.click(fn=play_autio, outputs=audio)

            
        # Tab 1
        tab1_Word_Show.change(fn=play_autio, outputs=tab1_audio)
        tab1_bt_prev.click(fn=prev_word, outputs=[tab1_word_label, tab1_Word_Show])
        tab1_bt_next.click(fn=next_word, outputs=[tab1_word_label, tab1_Word_Show])
        
        tag1_bt_modify_init.click(fn=tab1_modify_init, outputs=tab1_Word_Show)
        tab1_bt_modify.click(fn=tab1_modify_word, inputs=tab1_Word_Show, outputs=tab1_Word_Show)
        tab1_bt_save.click(fn=save_all_word_to_text)

        # Tab 2
        tab2_bt_clear.click(fn=clear_new_word, outputs=tb_new_word)
        tab2_bt_add.click(fn=add_new_word, inputs=tb_new_word, outputs=tb_new_word)
        tab2_bt_search.click(fn=search_word, inputs=tb_new_word, outputs=tb_new_word)

        # Tab3 
        tab3_bt_modify_init.click(fn=tab3_modify_init, inputs=tab3_tb_search_word, outputs=tab3_tb_search_word)
        tab3_bt_modify.click(fn=tab3_modify_word, inputs=tab3_tb_search_word, outputs=tab3_tb_search_word)
        tab3_bt_search.click(fn=search_word, inputs=tab3_tb_search_word, outputs=tab3_tb_search_word)

    demo.launch(inbrowser=True)