import gensim
from gensim import corpora
from gensim.models import TfidfModel, LdaModel, Lda2Vec
from gensim.models.ldamodel import LdaModel
from gensim.models.ldaseqmodel import LdaSeqModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

# 读取专利摘要数据
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()
    return data

# 数据预处理
def preprocess_data(data):
    stop_words = set(stopwords.words('english'))  # 英文停用词表
    processed_data = []
    
    for document in data:
        words = word_tokenize(document.lower())  # 分词并转换为小写
        words = [word for word in words if word.isalnum()]  # 移除非字母数字字符
        words = [word for word in words if word not in stop_words]  # 移除停用词
        processed_data.append(words)
    
    return processed_data

# 创建TF-IDF向量化模型
def create_tfidf_model(processed_data):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([" ".join(doc) for doc in processed_data])
    return tfidf_matrix, tfidf_vectorizer

# 创建LDA模型
def create_lda_model(tfidf_matrix, num_topics):
    corpus = gensim.matutils.Sparse2Corpus(tfidf_matrix, documents_columns=False)
    id2word = corpora.Dictionary.from_corpus(corpus, id2word=dict((id, word) for word, id in tfidf_vectorizer.vocabulary_.items()))
    
    lda_model = LdaModel(corpus=corpus, num_topics=num_topics, id2word=id2word)
    return lda_model

# 创建LDA-2Vec模型
def create_lda2vec_model(lda_model, processed_data, num_topics):
    lda2vec = Lda2Vec(corpus=processed_data, num_topics=num_topics, lda_model=lda_model)
    return lda2vec

# 主程序
if __name__ == "__main__":
    file_path = "patent_abstracts.txt"  # 专利摘要文件路径
    num_topics = 10  # 主题数量

    # 加载数据并进行预处理
    data = load_data(file_path)
    processed_data = preprocess_data(data)

    # 创建TF-IDF向量化模型
    tfidf_matrix, tfidf_vectorizer = create_tfidf_model(processed_data)

    # 创建LDA模型
    lda_model = create_lda_model(tfidf_matrix, num_topics)

    # 创建LDA-2Vec模型
    lda2vec_model = create_lda2vec_model(lda_model, processed_data, num_topics)

    # 进行主题分析或其他分析任务
    # 可以使用lda_model和lda2vec_model来获取主题分布或进行相似性分析等任务
