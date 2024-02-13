from gensim import corpora, models
import nltk
import os
import jieba
from gensim.parsing.preprocessing import STOPWORDS
import string
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
import matplotlib.pyplot as plt

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


if __name__ == '__main__':
    input_path="./CleanAbstract"
    dict_patent=generateDict(input_path)
    dict_preprocess={}
    for key,values in dict_patent.items():
        dict_preprocess[key] = preprocess(values)
    
    texts = list(dict_preprocess.values())
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    for i in range(24,25):
        # 训练LDA模型
        num_topics = i
        lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary,minimum_probability=0)

        # 将主题词存储到TopicImplication.txt文件中
        with open(str(i).zfill(2)+'TopicImplication.txt', 'w',encoding='utf-8') as f:
            for topic_id in range(20):
                topic_words = lda_model.show_topic(topic_id)
                f.write(f'{topic_words}\n')

        # 将文章主题向量存储到OutcomeAbstract.txt文件中
        with open('OutcomeAbstract.txt', 'w') as f:
            for doc_id, text in dict_preprocess.items():
                bow = dictionary.doc2bow(text)
                doc_topics = lda_model.get_document_topics(bow)
                f.write(f'id-{doc_id} vector-{doc_topics}\n')