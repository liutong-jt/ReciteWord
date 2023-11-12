import re, os, random
from config import config

class Word():
    def __init__(self, English='', 
                 chinese='',
                 prefix=None,
                 suffix=None,
                 root=None,
                 helpful=None,
                 derivative=None,
                 etymology=None,
                 levovo=None,
                 usage=None,
                 near=None,
                 anti=None,
                 paraphrase=None,
                 form_similar=None,
                 learning_point=None,
            ):
        self.English = English
        self.chinese = chinese
        self.prefix = prefix
        self.suffix = suffix
        self.root = root
        self.helpful = helpful
        self.derivative = derivative
        self.etymology = etymology
        self.levovo = levovo
        self.usage = usage
        self.near = near
        self.anti = anti
        self.paraphrase = paraphrase
        self.form_similar = form_similar
        self.learning_point = learning_point

    def to_repr(self) -> str:
        '''
            只显示有值的属性,
            如果某一属性有多个值,则单条罗列。
                例如：[词根]: root, tree
                    -> [词根]: root
                       [词根]: tree
        '''
        info = f'{self.English}:{self.chinese}\n'
        for key, value in config.items():
            value = getattr(self, value)
            if value:  # 如果有值
                if isinstance(value, list):
                    for item in value:
                        info += f'[{key}]:{item}\n'
                else:
                    info += f'[{key}]:{value}\n'
        return info
    
    def modify_init(self):
        '''
            即使没有值也要显示
        '''
        info = f'{self.English}:{self.chinese}\n'
        for key, value in config.items():
            value = getattr(self, value)
            if isinstance(value, list):
                for item in value:
                    info += f'[{key}]:{item}\n'
            else:
                if value:   # 如果有值
                    info += f'[{key}]:{value}\n'
                else:        # 如果没有值 或者是None, 则显示空字符串
                    info += f'[{key}]:\n'
        return info

    def to_json(self) -> dict:
        info = {}
        for key, value in config.items():
            if getattr(self, value):
                info[key] = str(getattr(self, value))
        info['单词'] = self.English
        info['中文'] = self.chinese
        return info

    def from_str(self, inputs):
        lines = inputs.strip().split('\n')

        for i, line in enumerate(lines):
            if i == 0:
                # self.English, self.chinese = line.split(':')     # 加入没有:， 而是只有英语单词（或者英语汉语之间是其他符号）
                matched = re.match(r'[a-zA-Z]+', line)
                English_start, English_end = matched.start(), matched.end()
                self.English = line[English_start:English_end]
                self.chinese = re.sub(r'^[\s:：；;]+', '', line[English_end:])
                self.English, self.chinese = self.English.strip(), self.chinese.strip()
            elif line.strip():
                try:
                    key, input_value = line.split(']:')
                    key, input_value = key.strip(), input_value.strip()
                    if input_value:
                        # 如果有多个[助记]，[前缀]，将其放到列表里
                        current_value = getattr(self, config[key[1:]])

                        if current_value is None:
                            setattr(self, config[key[1:]], input_value)
                        elif isinstance(current_value, list): # 如果该值是列表形式，则直接append
                            current_value.append(input_value)
                            setattr(self, config[key[1:]], current_value)
                        else:                                # 如果不是列表，则将其包装成列表
                            setattr(self, config[key[1:]], [current_value, input_value])
                        # print('Print: add a new word:\n', self.to_repr())
                except ValueError as e:
                    self.English = f' [Error]:单词格式错误, {e}'
        return self
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Word):
            return self.English == other.English
        elif isinstance(other, str):
            return self.English == other

class Index:
    def __init__(self, word_status, RECITE_LENGTH=20):
        self.RECITE_LENGTH = RECITE_LENGTH
        self.indexs = []
        self.current_index = None
        self.prev = None
        self.word_status = word_status
        self.word_status = self.update()
        # self.current_index = self.get_next_index()

    def get_next_index(self):
        self.prev = self.current_index

        self.current_index = random.choice(self.indexs)
        if self.current_index == self.prev:
            self.current_index = random.choice(self.indexs)
            
        return self.current_index

    def update(self):
        need_update = []
        for idx in self.indexs:
            if self.word_status.iloc[idx].status == 2:  # 已完成该单词
                need_update.append(idx)

        # 更新状态，删除已完成的单词
        self.indexs = [idx for idx in self.indexs if idx not in need_update]
        # 添加未学习的单词
        for i in range(len(self.word_status)):
            if self.word_status.iloc[i].status != 2 and i not in self.indexs:
                self.indexs.append(i)
                self.word_status.iloc[i].status = 1      # 设置单词的状态位: 正在学习
            if len(self.indexs) >= self.RECITE_LENGTH :
                break

        return self.word_status

def check_illeagal_word(inputs):
    # 使用正则表达式进行断言
    word_pattern = r'^[a-zA-Z]+'                        # 只要是字母开头就行
    feature_pattern = r'^\[.{1,3}\]\s*[:-:：]\s*.*$'    # [abc]   :-：   asldfjl
    
    assert inputs is not None, '输入不能为空'
    lines = inputs.strip().split('\n')

    for i,line in enumerate(lines):
        if i == 0:
            assert re.match(word_pattern, line), f'line "{line}" is not a word format'
        elif line.strip():
            assert re.match(feature_pattern, line), f'line "{line}" is not a feature format'
            key = line.split(']:')[0]
            assert key[1:] in config, f'key {key} is not in config'

def create_word():
    English = input('请输入单词：')
    chinese = input('请输入中文：')
    word = Word(English=English, chinese=chinese)
    return word


if __name__ == '__main__':
    from read_from_raw import read_word_from_standard_text
    Word_lists = read_word_from_standard_text('save_text.txt')


    word = Word('ingress')
    if word in Word_lists:
        print('ol')

    word_dict = {}
    for word in Word_lists:
        word_dict[word.English] = word

    length = len(Word_lists)
    for i in range(length):
        word = Word_lists[i]
        derivative = getattr(word, config['派生词'])
        if derivative:
            print(derivative)
            word.derivative = []
            try:
                while True:
                    new_word = create_word()
                    if new_word.English in word_dict:
                        new_word = word_dict[new_word.English]
                    else:
                        Word_lists.append(new_word)
                        word_dict[new_word.English] = new_word
                    
                    print(new_word.to_repr())
                    if input('是否插入(y/n):') == 'n':
                        pass
                    else:
                        word.derivative.append(new_word)
                        print('添加成功')
                    if input('是否继续添加派生词(y/n):') == 'n':
                        break
                    print(derivative)
            except KeyboardInterrupt:
                print('中断')
            finally:
                with open('word_origin.txt', 'w', encoding='utf8') as f:
                    for word in Word_lists:
                        f.write(word.to_repr())
                os._exit(0)





    