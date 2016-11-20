from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from model import Author
from model import connect_to_db, db 
from server import app
from scipy.spatial.distance import cdist, pdist
import numpy as np
import matplotlib.pyplot as plt


connect_to_db(app)

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

# true_k = 5
# km = KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=1)
# km.fit(S)
# print("Top terms per cluster:")
# order_centroids = km.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# for i in range(true_k):
#     print "Cluster %d:" % i,
#     for ind in order_centroids[i, :10]:
#         print ' %s' % terms[ind],
#     print


# determine k range
k_range = range(1, 20)

# fit kmeans model for each cluster number in k_range
k_means_var = [KMeans(n_clusters=k).fit(S) for k in k_range]

# get cluster centers for each model
centroids = [X.cluster_centers_ for X in k_means_var]

# euclidean distance from each point to each cluster center
k_euclid = [cdist(S.toarray(), cent, 'euclidean') for cent in centroids]
dist = [np.min(ke,axis=1) for ke in k_euclid]

# total within cluster sum of squares
wcss = [sum(d**2) for d in dist]

# Total  sum of square
tss = sum(pdist(S.toarray())**2)/S.shape[0]

# between cluster sum of squares
bss = tss-wcss


# elbow curve
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(K, avgWithinSS, 'b*-')
ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
plt.grid(True)
plt.xlabel('Number of clusters')
plt.ylabel('Average within-cluster sum of squares')
plt.title('Elbow for KMeans clustering')
plt.show()
