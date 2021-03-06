<h1>The Poetry Project</h1>

Deployed on Heroku! Check it out: <a href="https://poetryproject.herokuapp.com" target="_blank">https://poetryproject.herokuapp.com</a>

![](http://g.recordit.co/0ro9r6KQ2X.gif)

<p>The Poetry Project allows people to explore how poets use words. The main page allows users to search for a particular word and see all instances of that term across the text corpus. This search is quick because it implements Postgres' full text search capability using a GIN index. Users can also explore by author and subject—the author page sorts authors by breadth of vocabulary, and the subject page lets users dynamically build a table to see the top terms used per subject. Lastly, users can explore the results of common topic extraction methods to see how a computer models topics: a K-Means analysis of the entire poem corpus, and a Latent Dirichlet Allocation topic analyses on an author-by-author basis. These forms of unsupervised learning required transforming each poem into a multidimensional TF-IDF vector.</p>
<p>The project uses Python, PostgreSQL, SQLAlchemy, Flask, scikit-learn, Jinja, JavaScript, jQuery, AJAX, unittest, requests, Beautiful Soup, and Bootstrap.</p>
<div>
<h2>Contents:</h2>
<ul>
<li><a href="#features">Features</a></li>
<li><a href="#setup">Setup</a></li>
<li><a href="#build-process">Build Process</a></li>
</ul>
</div>

<div>
<h2>Features</h2>
<h4><i>Current</i></h4>
<ul>
<li>Full text search using GIN index</li>
<li>Dynamically generate table of top words used per subject using AJAX calls and jQuery</li>
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
<h2>Setup</h2>
<ol>
<li><h4><i>Clone the repository</i></h4></li>
<li><h4><i>Create a virtual environment and install all required libraries</i></h4>
<p>Inside the repo that you just cloned, create a virtual environment:<br/><br/><code>virtualenv env</code><br/><br/>enter the virtual env:<br/><br/><code>source env/bin/activate</code><br/><br/>and install all required libraries:<br/><br/><code>pip install -r requirements.txt</code><br/><br/> Note best practices and make sure you add your env folder to your .gitignore file (<code>echo '/env' >> .gitignore</code>).</p></li>
<li><h4><i>Create the database</i></h4>
<p>At the command line, type <br/><br/><code>createdb poetry</code><br/><code>psql poetry < poetry.sql</code><br/><br/> to create and restore the database. This requires you to have PostgreSQL on your machine.</p></li>
<li><h4><i>Run the server</i></h4>
<p>Run <br/><br/><code>python server.py</code><br/><br/>and you should be up and running! Go to localhost in your browser and check it out.</p></li>
</ol>

</div>

<div>
<h2>Build Process</h2>
<ul>
<li><h4><i>Scraping Poems</i></h4>
</li>
<li><h4><i>Seeding the Database</i></h4>
</li>
<li><h4><i>Creating a Full Text Search</i></h4>
</li>

</div>