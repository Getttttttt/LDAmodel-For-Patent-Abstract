from gensim import corpora, models
import matplotlib.pyplot as plt
import os
import jieba
from gensim.parsing.preprocessing import STOPWORDS
import string
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
import matplotlib.pyplot as plt
import nltk

stop_words = list(STOPWORDS)
punctuations = string.punctuation
# 获取所有数字
digits = string.digits
# 获取所有空字符
whitespace = string.whitespace

def generateDict(input_path):
    dict_patent={}
    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            for root, dirs, files in os.walk(input_path+'/'+dir):
                for file in files:
                    with open(input_path+'/'+dir+'/'+file,'r',encoding='utf-8') as f_input:
                        for line in f_input:
                            line=line.strip()
                            each_patent = line.split('    ',1)
                            id_number = each_patent[0]
                            abstract = each_patent[1]
                            id_number = id_number.split('-',1)[1]
                            abstract = abstract.split('-',1)[1]
                            if id_number in dict_patent :pass
                            else : dict_patent[id_number]=abstract
    return dict_patent

def preprocess(text):
    words = jieba.lcut(text)
    # 去除停用词
    words = [word for word in words if word not in stop_words  and word not in punctuations and word not in digits and word not in whitespace]
    words = [word.lower() for word in words]
    tagged_words = nltk.pos_tag(words)
    nouns_and_verbs = [word for word, pos in tagged_words if pos.startswith('N') or pos.startswith('V')]
    return nouns_and_verbs

def curioucity_display(dict_in):
    # 将字典转换为语料库
    corpus = [value for value in dict_in.values()]
    dictionary = Dictionary(corpus)
    corpus = [dictionary.doc2bow(text) for text in corpus]
    # 定义主题数量范围
    min_topics = 1
    max_topics = 30
    step_size = 1
    # 计算困惑度
    perplexity_scores = []
    for num_topics in range(min_topics, max_topics+1, step_size):
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
        perplexity_score = pow(2,-lda_model.log_perplexity(corpus))
        perplexity_scores.append(perplexity_score)
    # 绘制困惑度曲线
    x = range(min_topics, max_topics+1, step_size)
    plt.plot(x, perplexity_scores)
    plt.xlabel('Number of Topics')
    plt.ylabel('Perplexity Score')
    plt.title('LDA Perplexity Scores')
    plt.show()

if __name__ == '__main__':
    input_path="./CleanAbstract"
    dict_patent=generateDict(input_path)
    dict_preprocess={}
    for key,values in dict_patent.items():
        dict_preprocess[key] = preprocess(values)
    curioucity_display(dict_preprocess)


