<h1>The Poetry Project</h1>

<p>The Poetry Project allows people to explore how masters of language use words. The main page allows users to search for a particular word and see all instances of that term across the text corpus. This search is quick because it implements Postgres' full text search capability using a GIN index. Users can also explore by author and subject—the author page sorts authors by breadth of vocabulary, and the subject page lets users dynamically build a table to see the top terms used per subject. Lastly, users can see the results of a K-Means analysis of the corpus, plus compare Latent Dirichlet Allocation topic analyses on an author-by-author basis. These forms of unsupervised learning required transforming each poem into a multidimensional TF-IDF vector.</p>

<!-- <div>
<h2>Contents:</h2>
<ul>
<li>Features</li>
<li>Data Scraping</li>
<li>Creating an index</li>
<li>Creating an index</li>
</ul>
</div> -->

<div>
<h3>Features</h3>
<h4><i>Current</i></h4>
<ul>
<li>Full text search using GIN index</li>
<li>Dynamically generate table of top words used per subject using AJAX calls</li>
<li>See author list sorted by breadth of vocabulary</li>
<li>Caching of sorted author list</li>
<li>KMeans analysis of entire corpus</li>
<li>Dynamically generate LDA topic analysis of an author's poems</li>
<li>Compare LDA analyses of different authors side by side</li>
<li>Tests for many server routes and database queries</li>
</ul>

<h4><i>Future things I'd like to do</i></h4>
<ul>
<li>Play with graphs by using Network X to model subject relationships based on how often subjects are found on the same poem</li>
<li>Incorporate TF-IDF weighting into search results on homepage, author page, and subject page</li>
<li>Write more extensive tests</li>
</ul>
</div>