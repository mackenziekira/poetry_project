from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from model import Author
from model import connect_to_db, db 
from server import app
# from scipy.spatial.distance import cdist, pdist
# import numpy as np
# import matplotlib.pyplot as plt


connect_to_db(app)

patti = Author.query.get(267)
text = []

for poem in patti.poems:
    text.append(poem.body)

vectorizer = TfidfVectorizer(stop_words='english')

S = vectorizer.fit_transform(text)


n_topics = 4
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


# K = range(1,20)
# KM = [KMeans(n_clusters=k).fit(S) for k in K]
# centroids = [k.cluster_centers_ for k in KM]

# D_k = [cdist(S.toarray(), cent, 'euclidean') for cent in centroids]
# cIdx = [np.argmin(D,axis=1) for D in D_k]
# dist = [np.min(D,axis=1) for D in D_k]
# avgWithinSS = [sum(d)/S.shape[0] for d in dist]

# # Total with-in sum of square
# wcss = [sum(d**2) for d in dist]
# tss = sum(pdist(S.toarray())**2)/S.shape[0]
# bss = tss-wcss

# kIdx = 10-1

# # elbow curve
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(K, avgWithinSS, 'b*-')
# ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
# markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
# plt.grid(True)
# plt.xlabel('Number of clusters')
# plt.ylabel('Average within-cluster sum of squares')
# plt.title('Elbow for KMeans clustering')

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(K, bss/tss*100, 'b*-')
# plt.grid(True)
# plt.xlabel('Number of clusters')
# plt.ylabel('Percentage of variance explained')
# plt.title('Elbow for KMeans clustering')
