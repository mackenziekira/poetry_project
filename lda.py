from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from model import Author, Poem
from model import connect_to_db, db 
from server import app

connect_to_db(app)

poems = Poem.query.all()

# author = Author.query.get(1)
text = []

for poem in poems:
    text.append(poem.body)

vectorizer = TfidfVectorizer(stop_words='english')

S = vectorizer.fit_transform(text)


n_topics = 10
n_top_words = 20

lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

def group_top_words(model, feature_names, n_top_words):
    top_words = {}
    for topic in model.components_:
        top_words[sum(topic)] = [feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]
    return top_words

lda.fit(S)

tf_feature_names = vectorizer.get_feature_names()

top_words = group_top_words(lda, tf_feature_names, n_top_words)

sorted_keys = sorted(top_words.keys(), reverse=True)

for k in xrange(10):
    print sorted_keys[k], top_words[sorted_keys[k]]
    print