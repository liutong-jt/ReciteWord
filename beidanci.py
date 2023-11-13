from main import *
import pandas as pd
import random, time
# from pygame import mixer 
from pydub import AudioSegment
import numpy as np
from Word import Index

class Recite(Word):
    '''
        1. 选择单词到背诵列表里；
        2. 为该单词建立对应的背诵参数：
            - 得分（认识，不认识） 正确+3分，错误-3分
            - 满分 10 分 完成该单词  
            - 第几次背诵该单词
            - 开始时间，完成时间
            - 错误次数
            - 是否完成该单词
        3. 正在学习的单词最大数量为 10个/ *分
    '''
    def __init__(self, word):
        self.word = word           # 单词
        self.score = 0             # 得分
        self.done = False          # 是否完成该单词
        self.start_time = []       # 背诵时间
        self.level = 0             # 第几次背诵该单词, 和背诵开始时间对应
        self.error_times = 0       # 错误次数

def init_status(word_list):
    #TODO: index 的最大长度可以修改全局变量

    value =[{'word':word.English,'status':0, 'score': 0, 'error':0, 'No':i} for i, word in enumerate(word_list)]
    word_status = pd.DataFrame(value)
    word_status = word_status.set_index('word')
    
    if os.path.exists('recite_status.csv'):
        init_status = pd.read_csv(r'recite_status.csv', index_col=0)
        for i in range(len(init_status)):
            w = init_status.iloc[i]
            if pd.isna(w.name):
                w.name = 'null'
            word_status.loc[w.name].status = w.status
            word_status.loc[w.name].score = w.score
            word_status.loc[w.name].error = w.error
            word_status.loc[w.name].No = w.No
            # word_status.loc[str(w.word)].status = w.status
            # word_status.loc[str(w.word)].score = w.score
            # word_status.loc[str(w.word)].error = w.error
            # word_status.loc[str(w.word)].No = w.No

    return word_status

def next_word():
    ...

def prev_word():
    ...

def know_word():
    global recite_word_list, index

    recite = recite_word_list[index.current_index]

    index.word_status.loc[recite.English].score += 4        # SETTING: 正确加分

    if index.word_status.loc[recite.English].score >= 10:   # SETTING: 完成该单词
        index.word_status.loc[recite.English].score = 10
        index.word_status.loc[recite.English].status = 2

    index.update()
    next_recite = recite_word_list[index.get_next_index()]
    audio_path = os.path.join(AUDIO_DIR, next_recite.English[0].lower(), f'{next_recite.English}.mp3')

    if index.word_status.loc[recite.English].score >= 10:   # SETTING: 完成该单词
        Finish = AudioSegment.from_file(FINISH_MUSIC)
        Wordwav = AudioSegment.from_file(audio_path)
        Finish = Finish.set_frame_rate(Wordwav.frame_rate)
        Answer = Finish + Wordwav
        Answer = np.array(Answer.get_array_of_samples(), dtype=np.float16)
        audio_path = (Wordwav.frame_rate, Answer)

    print(index.prev, index.current_index)
    return next_recite.English, next_recite.to_repr(), audio_path

def not_know_word():
    global recite_word_list, index
    recite = recite_word_list[index.current_index]
    index.word_status.loc[recite.English].score -= 2     # SETTING: 错误扣分
    index.word_status.loc[recite.English].error += 1

    index.update()
    next_recite = recite_word_list[index.get_next_index()]

    print(index.prev, index.current_index)

    audio_path = os.path.join(AUDIO_DIR, next_recite.English[0].lower(), f'{next_recite.English}.mp3')

    return next_recite.English, next_recite.to_repr(), audio_path

def update_status(word_status, index):
    need_update = []
    for idx in index:
        if word_status.iloc[idx].status == 2:  # 已完成该单词
            need_update.append(idx)

    # 更新状态，删除已完成的单词
    index = [idx for idx in index if idx not in need_update]
    # 添加未学习的单词
    for i in range(len(word_status)):
        if word_status.iloc[i].status != 2:
            index.append(i)
            word_status.iloc[i].status = 1
        if len(index) >= 20 :
            break
    return word_status, index

def save_status():
    global index, WORD, recite_word_list
    index.word_status.to_csv('recite_status.csv')

    with open(dictionary_path, 'w', encoding='utf8') as f:
        for w in WORD:
            if w in recite_word_list:
                w = recite_word_list[recite_word_list.index(w)]
            print(w.to_repr(), file=f)

def modify_init(inputs):
    global recite_word_list, WORD, index
    print(time.ctime(), 'modify_init', index.current_index)
    return recite_word_list[index.current_index].modify_init()

def modify_word(inputs):
    '''
        修改直接覆盖当前索引单词
        可以修改当前英语单词
    '''
    global recite_word_list, WORD, index

    print(time.ctime(), 'modify_word', index.current_index)

    try:
        check_illeagal_word(inputs)
        word = Word().from_str(inputs)
        if word not in recite_word_list:
            raise ValueError(f'没有该单词 {word.English}, 清查看单词信息的English是否正确。')
            
        # 判断是否有派生词
        derivative = getattr(word, config['派生词'])
        if derivative:
            derivative_words = re.split('[,，；;\s]+', derivative)
            for w in derivative_words:
                if w != '' and w not in WORD:
                    WORD.append(Word(English=w))
        
        
        recite_word_list[index.current_index] = word
        result = recite_word_list[index.current_index].to_repr()
        return result
    except AssertionError as e:
        return '\n\n'.join(['[Error]: 单词格式错误', str(e),inputs])
    
if __name__ == '__main__':
    # global recite_word_list, word_status

    WORD = read_word_from_standard_text(dictionary_path)
    start_index = WORD.index('regress')
    end_index = WORD.index('evoke')
    recite_word_list = [WORD[i] for i in range(start_index, end_index+1)]
    word_status = init_status(recite_word_list)
    # word_status.to_csv('a.csv')
    index = Index(word_status, RECITE_LENGTH=20)
    index.get_next_index()


    #TODO: 可修改内容
    #TODO: 保存时，同时保存修改后的单词文件
    #TODO: 添加动词/形容词， 添加音标
    with gr.Blocks() as demo:
        with gr.Row(equal_height=False):
            with gr.Column(min_width="2000px"):
                word_english = gr.Label(recite_word_list[index.current_index].English)
                word_info = gr.Textbox(recite_word_list[index.current_index].to_repr(), lines=6)
                with gr.Row():
                    bt_notknow = gr.Button(value='不认识')
                    bt_know = gr.Button(value='认识')
                with gr.Row():
                    bt_modify_init = gr.Button(value='Modify_Init')
                    bt_modify = gr.Button(value='Modify')
        audio = gr.Audio(autoplay=True)
        bt_save = gr.Button(value='背诵状态')

        bt_know.click(fn=know_word, outputs=[word_english, word_info, audio])
        bt_notknow.click(fn=not_know_word, outputs=[word_english, word_info, audio])
        bt_save.click(fn=save_status)

        bt_modify_init.click(fn=modify_init, inputs=word_info, outputs=word_info)
        bt_modify.click(fn=modify_word, inputs=word_info, outputs=word_info)

    demo.launch(server_name='0.0.0.0', server_port=7860)
    # demo.launch(share=True)
    # demo.launch()