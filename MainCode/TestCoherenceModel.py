# Import the required modules
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
import matplotlib.pyplot as plt

# Load or create your LDA model, texts and dictionary
lda_model = LdaModel.load("my_lda_model")
texts = [["cat", "dog", "mouse"], ["car", "bike", "train"], ...]
dictionary = Dictionary.load("my_dictionary")

# Define the range of topic numbers
start = 2
limit = 40
step = 2
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
