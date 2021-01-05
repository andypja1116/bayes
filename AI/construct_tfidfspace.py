import os
from sklearn.utils import Bunch
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def _readbunchobj(path):
    with open(path, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


def _writebunchobj(path, bunchobj):
    with open(path, "wb") as file_obj:
        pickle.dump(bunchobj, file_obj)



def vector_space(bunch_path, space_path, train_tfidf_path=None):
    bunch = _readbunchobj(bunch_path)
    tfidf_space = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[], vocabulary={})

    if train_tfidf_path is None:
        train_vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
        train_tdm = train_vectorizer.fit_transform(bunch.contents)
        tfidf_space.tdm = train_tdm
        tfidf_space.vocabulary = train_vectorizer.vocabulary_

    else:
        trainbunch = _readbunchobj(train_tfidf_path)
        test_vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, vocabulary=trainbunch.vocabulary)
        test_tdm = test_vectorizer.fit_transform(bunch.contents)
        tfidf_space.tdm = test_tdm
        tfidf_space.vocabulary = trainbunch.vocabulary

    _writebunchobj(space_path, tfidf_space)

bunch_path = 'C:\\Users\\BEIJING\\Desktop\\Bunch\\train_set.pickle'
space_path = 'C:\\Users\\BEIJING\\Desktop\\Bunch\\train_tfidf_space.pickle'

vector_space(bunch_path, space_path)

bunch_path = 'C:\\Users\\BEIJING\\Desktop\\Bunch\\test_set.pickle'
space_path = 'C:\\Users\\BEIJING\\Desktop\\Bunch\\test_tfidf_space.pickle'
train_tfidf_path = 'C:\\Users\\BEIJING\\Desktop\\Bunch\\train_tfidf_space.pickle'
vector_space(bunch_path, space_path, train_tfidf_path)
