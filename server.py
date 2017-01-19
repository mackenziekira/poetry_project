from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.contrib.cache import SimpleCache
from lda import perform_lda
import queries
import os
from model import connect_to_db, db 
from model import Poem, Author, Subject



cache = SimpleCache()
app = Flask(__name__)

# Raises an error if you use undefined Jinja variable.
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def index():
    """Homepage."""


    term = request.args.get('term')
    if not term:
        return render_template('homepage.html', poems=[], headlines=[], subjects=[], term='')

    isalpha = term.isalpha()
    if isalpha == False:
        flash('Word must be all alpha characters.')
        return redirect('/')

    poems = Poem.query.options(db.joinedload('subjects')).filter(Poem.tsv.match(term)).all()
    if not poems:
        flash('Word not found. Try another!')
        return redirect('/')


    headlines = queries.get_headlines(term)

    subjects = queries.get_subject_counts(poems)
    

    return render_template("homepage.html", headlines=headlines, poems=poems, subjects=subjects, term=term)


@app.route('/authors')
def authors():
    """displays a list of poets"""

    authors = cache.get('authors')

    if authors is None:
        authors = queries.get_authors()
        cache.set('authors', authors, timeout=60 * 60)

    return render_template('authors.html', authors=authors)



@app.route('/subjects')
def subjects():
    """explore by subjects"""

    subjects = Subject.query.order_by('subject_name').all()

    return render_template('subjects.html', subjects=subjects)


@app.route('/lda')
def explore_lda():
    """lda proof of concept page"""

    authors = Author.query.all()

    return render_template('lda.html', authors=authors)


@app.route('/kmeans')
def explore_kmeans():
    """kmeans proof of concept page"""

    return render_template('kmeans.html')


@app.route('/about')
def about():
    """returns about page"""

    return render_template('about.html')

##########################################################################################################

# unique id routes

@app.route('/author/<author_id>')
def specfic_author(author_id):
    """displays word stats for specific authors"""

    author = queries.author_top_words(author_id)

    return render_template('author.html', author=author)

@app.route('/poem/<poem_id>')
def specific_poem(poem_id):
    """displays a single poem"""

    poem = Poem.query.get(poem_id)

    db.session.commit()

    return render_template('poem.html', poem=poem)

##########################################################################################################

# json routes

@app.route('/subject_info/<subject_id>.json')
def subject_info(subject_id):
    """get most common words for a given subject"""

    top_words = queries.subject_top_words(subject_id)

    return jsonify(top_words)

@app.route('/author_lda/<author_id>.json')
def author_lda(author_id):
    """get topic breakdown for particular author"""

    lda = perform_lda(author_id)

    return jsonify(lda)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    # app.config['SQLALCHEMY_ECHO'] = True

    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "asdf9k$")

    # Required to use Flask sessions and the debug toolbar
    app.secret_key = SECRET_KEY


    app.jinja_env.auto_reload = True
    connect_to_db(app, os.environ.get("DATABASE_URL"))

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
    