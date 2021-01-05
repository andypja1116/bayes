import os
from sklearn.utils import Bunch
import pickle

def corpus2bunch(wordbag_path, seg_path):
    catelist = os.listdir(seg_path)
    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    bunch.target_name.extend(catelist)

    for cate in catelist:
        class_path = os.path.join(seg_path,cate)
        file_list = os.listdir(class_path)
        for file in file_list:
            fullname = os.path.join(class_path,file)
            bunch.label.append(cate)
            bunch.filenames.append(fullname)
            f = open(fullname,'r',encoding='UTF-8')
            bunch.contents.append(f.read())
    obj = open(wordbag_path, 'wb')
    pickle.dump(bunch,obj)

wordbag_path = 'C:\\Users\\BEIJING\\Desktop\\Bunch\\train_set.pickle'
seg_path = 'C:\\Users\\BEIJING\\Desktop\\DataSet_seg'

corpus2bunch(wordbag_path, seg_path)

wordbag_path = 'C:\\Users\\BEIJING\\Desktop\\Bunch\\test_set.pickle'
seg_path = 'C:\\Users\\BEIJING\\Desktop\\TestSet_seg'

corpus2bunch(wordbag_path, seg_path)
