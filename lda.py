from sklearn.decomposition import LatentDirichletAllocation
from vectorizer import S, feature_names

# code based off of sci-kit learn lda example: http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-topics-extraction-with-nmf-lda-py
n_topics = 20
n_top_words = 10

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

top_words = group_top_words(lda, feature_names, n_top_words)

sorted_keys = sorted(top_words.keys(), reverse=True)

for k in xrange(n_topics):
    print sorted_keys[k], top_words[sorted_keys[k]]
    print