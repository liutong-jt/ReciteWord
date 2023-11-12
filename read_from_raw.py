from Word import Word
from config import config
import re

def read_word_from_origin_doc(file_path=r'word_doc.txt'):
    """
    读取word文档中的单词
    """
    line_list = []
    # read all lines from text file 
    with open(file_path, 'r', encoding='utf8') as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                line_list.append(line.strip())

    # extract word from lines
    Word_lists = []
    for line in line_list:
        if re.match(r'[a-z\*]', line):                           # 1. 当前行是一个新的单词
            if 'word' in locals():                               # 如果word已经存在，则添加到Word_lists中
                Word_lists.append(word)
            # 重新初始化word
            search_ans = re.search(r'[:：\s]+', line)
            if search_ans:
                word_start, word_end = search_ans.span()
                English_word, English_chinese = line[:word_start], line[word_end:] 
            else:
                raise Exception('单词格式错误:', line)
            word = Word(English_word, English_chinese)

        elif line.startswith('['):                                  # 2. 该单词的所有助记： [**]: **
            for key in config.keys():
                if re.match(f'\[{key}\]', line):
                    value = re.split(f'\[{key}\][:：\s]+', line)[-1]
                    if value :                                      # 如果value 不为空, 则添加到word中
                        current_value = getattr(word, config[key], value)
                        if current_value is None:
                            setattr(word, config[key], value)
                        else:
                            if isinstance(current_value, list):     # 2.1(如果有多个[前缀]等助记) 如果是列表，则添加到列表中
                                current_value.append(value)
                            else:                                   # 2.2(如果有多个[前缀]等助记) 如果不是列表，则转换成列表
                                setattr(word, config[key], [current_value, value])
        elif line.startswith('知'):
            pass
        else:
            print(line)
    if word != Word_lists[-1]:
        Word_lists.append(word)
    
    return Word_lists

def read_word_from_standard_text(file_path='word_origin.txt'):
    line_list = []
    # read all lines from text file 
    with open(file_path, 'r', encoding='utf8') as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                line_list.append(line.strip())
    # extract word from lines
    Word_lists = []
    for line in line_list:
        if re.match(r'[a-z\*]', line):                           # 1. 当前行是一个新的单词
            if 'word' in locals():                               # 如果word已经存在，则添加到Word_lists中
                Word_lists.append(word)
            if len(re.split(r'[:：;；\s]+', line)) == 2:                        # 如果是标准格式，则直接提取
                English_word, English_chinese = re.split(r'[:：;；\s]+', line)
            elif len(re.split(r'[:：;；\s]+', line)) > 2:                       # 如果不是标准格式，则需要重新提取
                English_word= re.split(r'[:：;；\s]+', line)[0]
                English_chinese = ';'.join(re.split(r'[:：;；\s]+', line)[1:])

            word = Word(English_word, English_chinese)
        elif line.startswith('['):                                  # 2. 该单词的所有助记： [**]: **
            key, value = line.split(']:')
            if not isinstance(value, str):
                value = eval(value)
            setattr(word, config[key[1:]], value)

    if word != Word_lists[-1]:
        Word_lists.append(word)

    return Word_lists

def check_two_word_list(Word_lists, Word_lists2):
    assert len(Word_lists) == len(Word_lists2), '两个单词列表长度不一致'
    config['单词'] = 'English'
    config['中文'] = 'chinese'
    for i in range(len(Word_lists)):
        word1, word2 = Word_lists[i], Word_lists2[i]
        for key,value in config.items():
            value1, value2 = getattr(word1, value), getattr(word2, value)
            if isinstance(value1, list) and isinstance(value2, list):
                if len(value1) != len(value2):
                    print(value1, value2)
                    raise('两个value不相同')
                for v1, v2 in zip(value1, value2):
                    if v1 != v2:
                        print(v1, v2)
                        raise('两个value不相同')
            elif value1 != value2:
                print(value1)
                print(value2)
                raise('两个value不相同')
    print('两个单词列表相同')        
    
if __name__ == '__main__':
    Word_lists = read_word_from_origin_doc(file_path=r'word_doc.txt')

    # save the standard format of word to txt file
    with open(r'word_origin.txt', 'w', encoding='utf8') as f:
        for word in Word_lists:
            print(word.to_repr(), file=f)

    Word_lists2 = read_word_from_standard_text(file_path='word_origin.txt')

    # check_two_word_list(Word_lists, Word_lists2)


    # save the standard format of word to txt file
    with open(r'word_origin2.txt', 'w', encoding='utf8') as f:
        for word in Word_lists2:
            print(word.to_repr(), file=f)