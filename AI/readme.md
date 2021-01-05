# 新闻文本分类 -- 自实现朴素贝叶斯分类器

## 项目文件包括：

- `segment_script.py`：数据预处理，用来将原新闻预料分词，其中主要利用了[jieba](https://github.com/fxsjy/jieba)分词，分词的要求为：
    - 只取汉字
    - 去掉停用词
    - 只取名词
    - 去掉单个字
-'segment_script_test.py'
- `class_word_frequents.py`：统计每个词在其类别下被包含的文档数，用以卡方检验计算；
- `chisquare_test.py`：卡方检验，筛选出每个类下卡方值高的特征词，卡方检验的原理与理解推荐此文---[特征选择算法之开方检验](http://www.blogjava.net/zhenandaci/archive/2008/08/31/225966.html)；
- `file2bunch.py`：分别将所有训练文件与测试文件的文件名、内容与对应类读入`Bunch`数据结构，并将其序列化存储到一个文件，方便后面程序的读写与计算；
- `bim_bayes.py`：自编二项式朴素贝叶斯分类器，其中利用`laplas`平滑算法进行零概率处理，利用`pandas`与`numpy`加速50万数据的训练与测试，经过多次测试，平均训练时间为10min，平均测试时间为23min，平均总体正确率、召回率和F测度都为`84%`；

