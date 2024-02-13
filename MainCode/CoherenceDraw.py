from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel
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
    input_path="./CleanAbstract"
    dict_patent=generateDict(input_path)
    dict_preprocess={}
    for key,values in dict_patent.items():
        dict_preprocess[key] = preprocess(values)
    
    texts = list(dict_preprocess.values())
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # Define the range of topic numbers
    start = 2
    limit = 60
    step = 1
    topic_numbers = range(start, limit, step)

    # Compute the coherence scores for each topic number
    coherence_scores = []
    for num_topics in topic_numbers:
        model = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)
        coherence_model = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence="c_v")
        coherence_score = coherence_model.get_coherence()
        coherence_scores.append(coherence_score)

    # Create a line plot with topic numbers on x-axis and coherence scores on y-axis
    plt.plot(topic_numbers, coherence_scores)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence Score")
    plt.title("Coherence Score vs Number of Topics")
    plt.show()

if __name__ == '__main__':
    input_path="./CleanAbstract"
    dict_patent=generateDict(input_path)
    dict_preprocess={}
    for key,values in dict_patent.items():
        dict_preprocess[key] = preprocess(values)
    curioucity_display(dict_preprocess)


