from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from model import Author
from model import connect_to_db, db 
from server import app


shake = Author.query.get(169)
text = []

for poem in shake.poems:
    text.append(poem.body)

vectorizer = TfidfVectorizer(stop_words='english')

S = vectorizer.fit_transform(text)


n_topics = 10
n_top_words = 20

lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
    
lda.fit(S)

tf_feature_names = vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

true_k = 5
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=1)
km.fit(S)
print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print "Cluster %d:" % i,
    for ind in order_centroids[i, :10]:
        print ' %s' % terms[ind],
    print
