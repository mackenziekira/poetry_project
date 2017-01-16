<h1>The Poetry Project</h1>

![](http://g.recordit.co/0ro9r6KQ2X.gif)

<p>The Poetry Project allows people to explore how masters of language use words. The main page allows users to search for a particular word and see all instances of that term across the text corpus. This search is quick because it implements Postgres' full text search capability using a GIN index. Users can also explore by author and subject—the author page sorts authors by breadth of vocabulary, and the subject page lets users dynamically build a table to see the top terms used per subject. Lastly, users can see the results of a K-Means analysis of the corpus, plus compare Latent Dirichlet Allocation topic analyses on an author-by-author basis. These forms of unsupervised learning required transforming each poem into a multidimensional TF-IDF vector.</p>

<div>
<h2>Contents:</h2>
<ul>
<li>Features</li>
<li>Setup</li>
</ul>
</div>

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

<div>
<h3>Setup</h3>
<h4><i>Clone the repository</i></h4>
<h4><i>Create a virtual environment and install all required libraries</i></h4>
<p>Inside the repo that you just cloned, create a virtual environment:```virtualenv env```enter the virtual env:<br/><code>source env/bin/activate</code><br/>and install all required libraries:<br/><code>pip install -r requirements.txt</code><br/> Note best practices and make sure you add your env folder to your .gitignore file (<code>echo '/env' >> .gitignore</code>).</p>
<h4><i>Create the database</i></h4>
<p>At the command line, type <code>createdb poetry</code> to create an empty database.</p>

</div>