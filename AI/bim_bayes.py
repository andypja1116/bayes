import os
import pandas
import pickle
from chisquare_test import count_cate_page
from math import log
import datetime

def readbunchobj(path):
    with open(path, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


def readfile(path):
    with open(path, 'r', encoding='UTF-8') as fp:
        content = fp.read()
    return content

# 构建特征词向量
def contrust_vect(words_path):
    words_vect = []
    file_list = os.listdir(words_path)
    for file_name in file_list:
        if file_name == '.DS_Store':
            continue
        if file_name[-11:] == '_select.txt':
            tmp = readfile(words_path + '\\' + file_name).split('\n')
            for word in tmp[:1000]:
                words_vect.append(word)
    return words_vect

def get_class_wordtimes(category, words_vect, word_times_path, cate_page_num):
    df = pandas.DataFrame(index=category, columns=words_vect)
    file_list = os.listdir(word_times_path)
    for cate_file in file_list:
        if cate_file == '.DS_Store':
            continue
        cate = cate_file.split('_')[0]
        word_fequents_dict = dict()
        wordtimes = readfile(word_times_path + '\\' + cate_file).split('\n')
        for word in wordtimes:
            word = word.split(':')
            if word[0] in words_vect:
                word_fequents_dict[word[0]] = log(int(word[1]) + 1) - log(cate_page_num[cate] + 2)
        df.loc[cate] = word_fequents_dict
    df = df.fillna(-10)
    return df

def classify(content=None, wordtimes_ndarray=None):

    per_page_words = set(content.split())
    columns = set(wordtimes_ndarray.columns)
    col = per_page_words & columns  # 将文章里的词与特征词集合‘与’运算
    p_ndarray = wordtimes_ndarray[list(col)].values
    line_sum = list(map(sum, p_ndarray))  # numpy在行方向上求和
    prediction = wordtimes_ndarray.index[line_sum.index(max(line_sum))]

    return prediction

# 二项式朴素贝叶斯分类
def predict(test_set, wordtimes_ndarray):
    TP, FP, FN = 0, 0, 0
    average_accuracy, average_recall, average_f = 0.0, 0.0, 0.0
    cate_TP = {}
    cate_FP = {}
    cate_FN = {}
    cate_accuracy = {}
    cate_recall = {}
    cate_F_measure = {}
    clock = 0

    category = test_set.target_name
    labels = test_set.label
    for cate in category:
        cate_TP[cate] = 0
        cate_FP[cate] = 0
        cate_FN[cate] = 0
        cate_accuracy[cate] = 0
        cate_recall[cate] = 0
        cate_F_measure[cate] = 0

    index = len(test_set.contents)
    for i in range(index):     # 对test_set.contents[i] 文档进行分类
        prediction = classify(
            content=test_set.contents[i],
            wordtimes_ndarray=wordtimes_ndarray
        )
        if prediction == labels[i]:
            cate_TP[prediction] += 1
        else:
            cate_FP[prediction] += 1
            cate_FN[labels[i]] += 1
        clock += 1
        print(clock)

    for cate in category:
        cate_accuracy[cate] = float(cate_TP.get(cate, 1)) / (cate_TP.get(cate, 1) + cate_FP.get(cate, 1))
        cate_recall[cate] = float(cate_TP.get(cate, 1)) / (cate_TP.get(cate, 1) + cate_FN.get(cate, 1))
        cate_F_measure[cate] = float(2*cate_TP.get(cate, 1)) / (2*cate_TP.get(cate, 1) + cate_FN.get(cate, 1) + cate_FP.get(cate, 1))
        TP += cate_TP[cate]
        FP += cate_FP[cate]
        FN += cate_FN[cate]
        average_accuracy += cate_accuracy[cate]
        average_recall += cate_recall[cate]
        average_f += cate_F_measure[cate]

    average_accuracy = average_accuracy / 10
    average_recall = average_recall / 10
    average_f = average_f / 10

    return average_accuracy, average_recall, average_f, cate_accuracy, cate_recall, cate_F_measure
begintime_test = datetime.datetime.now()
category = os.listdir('C:\\Users\\BEIJING\\Desktop\\TestSet_seg')
words_path = 'C:\\Users\\BEIJING\\Desktop\\train_chi_order'
words_vect = set(contrust_vect(words_path))

word_times_path = 'C:\\Users\\BEIJING\\Desktop\\wordtimes'
cate_page_num = count_cate_page(category)
word_fequents_ndarray = get_class_wordtimes(category, words_vect, word_times_path, cate_page_num)
    
test_set = readbunchobj('C:\\Users\\BEIJING\\Desktop\\Bunch\\test_set.pickle')
accuracy_rate, recall_rate, f_score, cate_accuracy, cate_recall, cate_F_measure \
        = predict(test_set, word_fequents_ndarray)
endtime_test = datetime.datetime.now()
print("预测完毕，预测时长为：" + str((endtime_test - begintime_test).seconds)+ "秒")
print('--' * 40)
print('features_number = ' + repr(len(words_vect)))
print('--' * 40)
for cate in category:
    print(cate + '_accuracy_rate = ' + repr(cate_accuracy[cate]))
    print(cate + '_recall_rate = ' + repr(cate_recall[cate]))
    print(cate + '_f_score = ' + repr(cate_F_measure[cate]))
    print('--' * 40)

print('accuracy_rate = ' + repr(accuracy_rate))
print('recall_rate = ' + repr(accuracy_rate))
print('f_score = ' + repr(accuracy_rate))
print('--' * 40)
