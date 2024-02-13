import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.similarities import MatrixSimilarity

# Define the two passages to compare
passage1 = "The cat sat on the mat. The cat is happy."
passage2 = "The dog sat on the rug. The dog is happy."

# Preprocess the text
def preprocess(text):
    # Tokenize the text
    tokens = gensim.utils.simple_preprocess(text)
    return tokens

# Create a dictionary from the preprocessed text
texts = [preprocess(passage1), preprocess(passage2)]
dictionary = corpora.Dictionary(texts)
print(dictionary)

# Create a bag-of-words representation of the text
corpus = [dictionary.doc2bow(text) for text in texts]

# Train an LDA model on the corpus
lda = LdaModel(corpus, num_topics=2, id2word=dictionary)

# Compute the similarity between the two passages using the LDA model
index = MatrixSimilarity(lda[corpus])
sims = index[lda[corpus[0]]]
print("Similarity between passage 1 and passage 2:", sims[1])

# Get the topic vectors for each passage
topic_vector1 = lda.get_document_topics(corpus[0])
topic_vector2 = lda.get_document_topics(corpus[1])

print("Topic vector for passage 1:", topic_vector1)
print("Topic vector for passage 2:", topic_vector2)
print(lda.show_topic(topicid=0))
print(lda.show_topic(topicid=1))
