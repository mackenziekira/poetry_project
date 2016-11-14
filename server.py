from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db 
from model import Poem, Author, Region, Affiliation, Subject, PoemSubject
from sqlalchemy import func



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


    # poems = Poem.query.filter(Poem.tsv.match(term)).all()

    if term:
        qry = 'SELECT *, ts_headline(body, q) AS headline FROM poems, to_tsquery(\'{}\') q WHERE q @@ tsv'.format(term)
        cursor = db.session.execute(qry)
        poems = cursor.fetchall()
        db.session.commit()
    else:
        poems = []
    

    return render_template("homepage.html", poems=poems)

@app.route('/authors')
def authors():
    """displays a list of poets"""

    authors = Author.query.all()

    return render_template('authors.html', authors=authors)

@app.route('/author/<author_id>')
def specfic_author(author_id):
    """displays word stats for specific authors"""

    qry = 'SELECT * FROM ts_stat(\'SELECT tsv FROM poems WHERE author_id = {}\') ORDER BY nentry DESC, ndoc DESC, word;'.format(author_id)

    author = Author.query.get(author_id)

    cursor = db.session.execute(qry)

    words = cursor.fetchall()

    db.session.commit()

    return render_template('author.html', author=author, words=words)

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
        word_dict.append({row[0]: row[2]})

    return jsonify(word_dict)


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