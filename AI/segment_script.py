import os
import re
import jieba.posseg as pseg
import sys

# 保存至文件
def _savefile(savepath, content):
    with open(savepath, "wb") as fp:
        fp.write(content)

# 读取文件
def _readfile(path):
    with open(path, "rb") as fp:
        content = fp.read()
    return content

# 处理停用词
def process_stop_word(file_path):
    stop_words = _readfile(file_path).decode('gb18030')
    stop_words = stop_words.replace("\n", " ")
    stop_list = stop_words.split(" ")
    return stop_list

def corpus_segment(corpus_path, seg_path):

    # def判断该分词对是否符合内容
    def judeg_word(seg_pair):
        if seg_pair.flag == 'n':
            if len(seg_pair.word) > 1:
                if seg_pair.word not in stop_words_list:
                    return True
        return False

    cate_list = os.listdir(corpus_path)  # 获取corpus_path下的所有子目录(即所有的类)

    try:
        for cate in cate_list:
            catagory_path = os.path.join(corpus_path, cate)
            seg_cate_path = os.path.join(seg_path, cate)
            file_list = os.listdir(catagory_path)

            for file_name in file_list:
                word_list = []
                fullname = os.path.join(catagory_path, file_name)
                seg_filename = os.path.join(seg_cate_path, file_name)
                f = open(fullname,'r',encoding='UTF-8')
                content = f.read()

                content = content.replace("\r\n", "")  # 删除换行
                content = content.replace(" ", "")  # 删除空行、多余的空格
                regular = u'[^\u4E00-\u9FA5]'  # 非汉字
                content = re.sub(regular, '', content)
                seg_pairs = pseg.cut(content)  # 为文件内容分词
                for seg_pair in seg_pairs:
                    if judeg_word(seg_pair):
                        word_list.append(seg_pair.word)

                if len(word_list) >= 5:
                    obj = open(seg_filename,'w',encoding='UTF-8')
                    obj.write(" ".join(word_list))
    except UnicodeError:
        print("出现编码异常")
        print(document_path)

stop_words_list = process_stop_word('C:\\Users\\BEIJING\\Desktop\\stop_words_ch.txt')
corpus_segment('C:\\Users\\BEIJING\\Desktop\\DataSet','C:\\Users\\BEIJING\\Desktop\\DataSet_seg')
                    
            
        
        
