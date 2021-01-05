import os

def contruct_word(cate_file):
    cate_content = []
    file_list = os.listdir(cate_file)
    for file in file_list:
        if file == '.DS_Store':
            continue
        file_path = os.path.join(cate_file,file)
        f = open(file_path,'r',encoding='UTF-8')
        content = f.read()
        content_tuple = set(content.split())
        cate_content.append(content_tuple)
    return cate_content

def count_word_frequents(seg_path, wordtime_path):
    cate_list = os.listdir(seg_path)
    for cate in cate_list:
        word_frequents_dict = {}
        save_file = os.path.join(wordtime_path,cate)
        save_file = save_file + '_wordtimes.txt'
        cate_file = os.path.join(seg_path,cate)
        cate_content = contruct_word(cate_file)
        for each_content in cate_content:
            for word in each_content:
                if len(word) >= 2:
                    word_frequents_dict[word] = word_frequents_dict.get(word,0)+1
                    
        obj = open(save_file,'w',encoding='UTF-8')
        for key, value in word_frequents_dict.items():
            obj.write(key + ':' +str(value))
            obj.write('\n')
count_word_frequents('C:\\Users\\BEIJING\\Desktop\\DataSet_seg','C:\\Users\\BEIJING\\Desktop\\wordtimes')
