from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist, pdist
# import numpy as np
# import matplotlib.pyplot as plt
from vectorizer import S, feature_names



true_k = 5
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=1)
km.fit(S)
print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]

for i in range(true_k):
    print "Cluster {}:".format(i),
    for ind in order_centroids[i, :10]:
        print '{}'.format(feature_names[ind]),
    print

# elbow method test to choose optimal k value. huge thanks to sarah guide (http://www.slideshare.net/SarahGuido/kmeans-clustering-with-scikitlearn) and marco dena (http://datascience.stackexchange.com/questions/6508/k-means-incoherent-behaviour-choosing-k-with-elbow-method-bic-variance-explain) for code guideline
"""
# determine k range
K = range(1,20)

# fit kmeans model for each number of clusters in k range
KM = [KMeans(n_clusters=k).fit(S) for k in K]

# pull out cluster centers for each kmeans model
centroids = [k.cluster_centers_ for k in KM]

# calculate euclidean distance from each document point to each cluster center
D_k = [cdist(S.toarray(), cent, 'euclidean') for cent in centroids]
cIdx = [np.argmin(D,axis=1) for D in D_k]
dist = [np.min(D,axis=1) for D in D_k]
avgWithinSS = [sum(d)/S.shape[0] for d in dist]

# Total within cluster sum of squares
wcss = [sum(d**2) for d in dist]

# total of sum of squares
tss = sum(pdist(S.toarray())**2)/S.shape[0]

# between-cluster sum of squares
bss = tss - wcss

kIdx = 10-1

# elbow curves
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(K, avgWithinSS, 'b*-')
ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
plt.grid(True)
plt.xlabel('Number of clusters')
plt.ylabel('Average within-cluster sum of squares')
plt.title('Elbow for KMeans clustering')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(K, bss/tss*100, 'b*-')
plt.grid(True)
plt.xlabel('Number of clusters')
plt.ylabel('Percentage of variance explained')
plt.title('Elbow for KMeans clustering')

"""