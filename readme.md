<h1>The Poetry Project</h1>

<p>The Poetry Project allows people to explore how masters of language use words. The main page allows users to search for a particular word and see all instances of that term across the text corpus. This search is quick because it implements Postgres' full text search capability using a GIN index. Users can also explore by author and subject—the author page sorts authors by breadth of vocabulary, and the subject page lets users dynamically build a table to see the top terms used per subject. Lastly, users can see the results of a K-Means analysis of the corpus, plus compare Latent Dirichlet Allocation topic analyses on an author-by-author basis. These forms of unsupervised learning required transforming each poem into a multidimensional TF-IDF vector.</p>

<div>
<h2>Features:</h2>
<ul>
<li>Full text search using GIN index</li>
<li>Dynamically generate table of top words used per subject</li>
<li>See author list sorted by breadth of vocabulary</li>
<li>Caching of sorted author list</li>
<li>KMeans analysis of entire corpus</li>
<li>Dynamically generate LDA topic analysis of an author's poems</li>
<li>Compare LDA analyses of different authors side by side</li>
</ul>
</div>