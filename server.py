from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db 
from model import Poem, Author, Region, Affiliation, Subject, PoemSubject
from sqlalchemy import func
from werkzeug.contrib.cache import SimpleCache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation


cache = SimpleCache()
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def index():
    """Homepage."""


    term = request.args.get('term')
    # term = '\'' + term +  '\''

    if not term:
        return render_template('homepage.html', poems=[], headlines=[], subjects=[])

    poems = Poem.query.filter(Poem.tsv.match(term)).all()

    if not poems:
        flash('Word not found. Try another!')
        return redirect('/')


    qry = 'SELECT *, ts_headline(body, q) AS headline FROM poems, to_tsquery(\'{}\') q WHERE q @@ tsv'.format(term)
    cursor = db.session.execute(qry)
    headlines = cursor.fetchall()
    db.session.commit()

    poem_ids = [0]

    for poem in headlines:
        poem_ids.append(poem[0])

    poem_ids = tuple(poem_ids)

    qry = "select s.subject_name, count(s.subject_name) from poems_subjects as ps join subjects as s on ps.subject_id = s.subject_id where ps.poem_id in {} group by s.subject_name order by count(s.subject_name) desc limit 5".format(poem_ids)

    cursor = db.session.execute(qry)

    subjects = cursor.fetchall()

    db.session.commit()
    

    return render_template("homepage.html", headlines=headlines, poems=poems, subjects=subjects)

def get_authors():
    """retrieve list of author objects (sorted by word stats) from the cache. else calculate list and return"""

    authors = cache.get('authors')
    if authors is None:
        authors = Author.query.all()

        for author in authors:
            qry = 'SELECT count(*) FROM ts_stat(\'SELECT tsv FROM poems WHERE author_id = {}\');'.format(author.author_id)

            cursor = db.session.execute(qry)

            word_count = cursor.fetchone()

            # divide by /len(author.poems) to attenuate mismatch in sample size?
            author.word_count = int(word_count[0])
            db.session.expunge(author)

            db.session.commit()

        authors = sorted(authors, key=lambda author: author.word_count, reverse=True)
        cache.set('authors', authors, timeout=60 * 60)
    return authors

@app.route('/authors')
def authors():
    """displays a list of poets"""

    authors = get_authors()

    return render_template('authors.html', authors=authors)

@app.route('/author/<author_id>')
def specfic_author(author_id):
    """displays word stats for specific authors"""

    qry = 'SELECT * FROM ts_stat(\'SELECT tsv FROM poems WHERE author_id = {}\') ORDER BY nentry DESC, ndoc DESC, word;'.format(author_id)

    author = Author.query.options(db.joinedload('poems')).get(author_id)

    cursor = db.session.execute(qry)

    words = cursor.fetchall()

    db.session.commit()

    return render_template('author.html', author=author, words=words)

@app.route('/poem/<poem_id>')
def specific_poem(poem_id):
    """displays a single poem"""

    poem = Poem.query.get(poem_id)

    db.session.commit()

    return render_template('poem.html', poem=poem)


@app.route('/subjects')
def subjects():
    """explore by subjects"""

    subjects = Subject.query.order_by('subject_name').all()

    return render_template('subjects.html', subjects=subjects)

@app.route('/subject_info/<subject_id>.json')
def subject_info(subject_id):
    """get most common words for a given subject"""

    # better way to fix this? need tuple to have at least two values, so this ensures no errors are thrown by psycopg2 
    poem_ids = [0, 0]

    relevant_poems = PoemSubject.query.filter_by(subject_id=subject_id).all()

    for poem in relevant_poems:
        poem_ids.append(poem.poem_id) 
    print poem_ids   

    poem_ids = tuple(poem_ids)


    qry = 'SELECT * FROM ts_stat(\'SELECT tsv FROM poems WHERE poem_id IN {}\') ORDER BY nentry DESC, ndoc DESC, word LIMIT 10;'.format(poem_ids)


    cursor = db.session.execute(qry)

    words = cursor.fetchall()

    db.session.commit()

    word_dict = []

    for row in words:
        word_dict.append({'word': row[0], 'count': row[2]})

    return jsonify(word_dict)

@app.route('/lda')
def lda():
    """lda proof of concept page"""

    authors = Author.query.all()

    return render_template('lda.html', authors=authors)

@app.route('/author_lda/<author_id>.json')
def author_lda(author_id):
    """get topic breakdown for particular author"""

    v = vectorize_poems(author_id)

    lda = perform_lda(v[0], v[1])

    return jsonify(lda)

@app.route('/kmeans')
def kmeans():
    """kmeans proof of concept page"""

    return render_template('kmeans.html')

def vectorize_poems(author_id):
    """returns vectorized version of an author's corpus"""
    
    author = Author.query.get(author_id)

    text = []
    for poem in author.poems:
        text.append(poem.body)


    vectorizer = TfidfVectorizer(stop_words='english')

    S = vectorizer.fit_transform(text)

    feature_names = vectorizer.get_feature_names()

    return [S, feature_names]

def perform_lda(S, feature_names):
    """given a tf_idf vectorized document(s) and feature names, returns lda analysis"""


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

    top_topics = []
    for k in xrange(3):
        top_topics.append(top_words[sorted_keys[k]])
        
    return top_topics


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['SQLALCHEMY_ECHO'] = True


    app.jinja_env.auto_reload = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run('0.0.0.0')
    