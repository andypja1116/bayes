from __future__ import division
import os

def count_cate_page(category):
    cate_page_num = {}
    for cate in category:
        path = os.path.join('C:\\Users\\BEIJING\\Desktop\\DataSet_seg',cate)
        cate_page_num[cate] = len(os.listdir(path))
    return cate_page_num

def get_word_times(category):
    cate_word_times = dict()
    for cate in category:
        cate_word_times['dict_'+cate] = dict()
        word_path = os.path.join('C:\\Users\\BEIJING\\Desktop\\wordtimes',cate+'_wordtimes.txt')
        df = open(word_path,'r',encoding='UTF-8')
        for ele in [d.strip().split(':') for d in df]:
            cate_word_times['dict_'+cate][ele[0]] = ele[1]
            
    return cate_word_times

def caculate_chi_write(category, cate_page_num, cate_word_times):
    for cate in category:
        dictname = cate_word_times['dict_'+cate]  # 将此类的词频词典赋予dictname
        chi_dic = {}  # 记录这个class中每个词的卡方检验值
        for kv in dictname:  # 遍历这个类别下的每个词，比较这个类别下每个词的CHI值
            kv_out_class = 0  # 统计一个新词时，初始化本类别外有这个词的文档数目为0  相当于b
            # not_kv_out_class = 0  # 统计一个新词时，初始化本类别外没有这个词的文档数目为0  相当于d
            kv_in_class = int(dictname[kv])   # 记录在这个分类下包含这个词的文档的数量  相当于a
            not_kv_in_class = (cate_page_num[cate]) - kv_in_class   # 记录在这个分类下不包含这个词的文档的数量  相当于c
            all_page_out_class = 0  # 初始化本类别外所有的文档数
            for cate_compare in category:
                if cate_compare != cate:
                    compare_name = cate_word_times['dict_'+cate_compare]
                    all_page_out_class += cate_page_num[cate_compare]
                    if kv in compare_name:
                        kv_out_class += int(compare_name[kv])

            not_kv_out_class = all_page_out_class - kv_out_class  # 本类所有别外没有用到这个词的文档数目  相当于d

            chi_dic[kv] = ((kv_in_class*not_kv_out_class - kv_out_class*not_kv_in_class) ** 2) / \
                          ((kv_in_class + kv_out_class) * (not_kv_in_class + not_kv_out_class))
        f = open('C:\\Users\\BEIJING\\Desktop\\train_chi_order\\class_'+cate+'_chi_order.txt','w',encoding='UTF-8')
        f.write('\n'.join(sorted(chi_dic, key=chi_dic.get, reverse=True)))

        obj = open('C:\\Users\\BEIJING\\Desktop\\train_chi_order\\class_'+cate+'_chi_order.txt','r',encoding='UTF-8')
        chi_order = obj.read()
        chi_order = chi_order.split('\n')
        k = open('C:\\Users\\BEIJING\\Desktop\\train_chi_order\\class_'+cate+'_chi_order_select.txt','w',encoding='UTF-8')
        N = 10000
        k.write('\n'.join(chi_order[0:N]))

category = os.listdir('C:\\Users\\BEIJING\\Desktop\\DataSet')
cate_page_num = count_cate_page(category)
cate_word_times = get_word_times(category)
caculate_chi_write(category, cate_page_num, cate_word_times)
