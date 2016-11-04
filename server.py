from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Poem, Author, Region
import spacy


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

    nlp = spacy.load('en')

    poems = Poem.query.all()

    docs = [nlp(body) for body in [poem.body for poem in poems]]

    t = nlp.vocab[u'kiss']

    sents = []
    objects = []

    for doc in docs:
        for sent in doc.sents:
            for token in sent:
                if token.orth == t.orth:
                    sents.append(sent.text)
                    objects.append(poems[docs.index(doc)])


    return render_template("homepage.html", sents=sents, objects=objects)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    app.jinja_env.auto_reload = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000)