import gensim
from gensim.models import LdaModel, Word2Vec
from gensim.corpora import Dictionary

# 示例文档
documents = [
    "apple banana fruit",
    "apple orange fruit",
    "car truck vehicle",
    "bike scooter motorcycle"
]

# 预处理文档
texts = [doc.split() for doc in documents]

# 创建词典
dictionary = Dictionary(texts)

# 转换文本数据为词袋表示
corpus = [dictionary.doc2bow(text) for text in texts]

# 训练LDA模型
lda = LdaModel(corpus, id2word=dictionary, num_topics=2)

# 训练Word2Vec模型
w2v = Word2Vec(sentences=texts, vector_size=100, window=5, min_count=1, workers=4)

# 为文档生成LDA向量
def get_lda_vector(text):
    bow = dictionary.doc2bow(text)
    lda_vec = [0] * lda.num_topics
    for topic_id, prob in lda.get_document_topics(bow):
        lda_vec[topic_id] = prob
    return lda_vec

# 示例: 获取某文档的LDA向量
doc_lda_vector = get_lda_vector(texts[0])

# 获取某单词的Word2Vec向量
word_vector = w2v.wv['apple']

print("LDA vector for first document:", doc_lda_vector)
print("Word2Vec vector for 'apple':", word_vector)