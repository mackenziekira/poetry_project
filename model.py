"""Models and database functions for Poetry project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



############################################################################
# Model definitions

class Poem(db.Model):
    """class for poem objects"""

    __tablename__ = 'poems'

    poem_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    poem_url = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)

    author = db.relationship('Author', backref='poems')
    subjects = db.relationship('Subject', secondary='poems_subjects', backref='poems')
    poetic_terms = db.relationship('PoeticTerm', secondary='poems_poetic_terms', backref='poems')

    @staticmethod
    def parse_poem(soup):
        selector = soup.find('div', class_="poem")

        if selector:
            return selector.text

    @staticmethod
    def parse_title(soup):
        selector = soup.find('title')

        if selector:
            return selector.string


class Author(db.Model):
    """class for author objects"""

    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    region_code = db.Column(db.String(100), db.ForeignKey('regions.region_code'))
    affiliation_code = db.Column(db.String(100), db.ForeignKey('affiliations.affiliation_code'))
    
    birthdate = db.Column(db.Date)
    deathdate = db.Column(db.Date)
    bio = db.Column(db.Text)

    region = db.relationship('Region', backref='authors')
    affiliation = db.relationship('Affiliation', backref='authors')

    @staticmethod
    def parse_name(soup):
        selector = soup.find(property="article:author")

        if selector:
            return selector['content']



class Region(db.Model):
    """class for region objects"""

    __tablename__ = 'regions'

    region_code = db.Column(db.String(100), primary_key=True)
    region_name = db.Column(db.String(300), nullable=False)



class Affiliation(db.Model):
    """class for affiliation objects"""

    __tablename__ = 'affiliations'

    affiliation_code = db.Column(db.String(100), primary_key=True)
    affiliation_name = db.Column(db.String(300), nullable=False)


class PoeticTerm(db.Model):
    """class for poetic terms associated with a poem"""

    __tablename__ = 'poetic_terms'

    term_code = db.Column(db.String(100), primary_key=True)
    term_name = db.Column(db.String(300), nullable=False)



class Subject(db.Model):
    """class for subjects"""

    __tablename__ = 'subjects'

    subject_code = db.Column(db.String(100), primary_key=True)
    subject_name = db.Column(db.String(300), nullable=False)



#################################################################################
#A couple association tables

class PoemPoeticTerm(db.Model):
    """association table connecting poems with poetic terms"""

    __tablename__ = 'poems_poetic_terms'

    poems_poetic_terms_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    term_code = db.Column(db.String(100), db.ForeignKey('poetic_terms.term_code'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.poem_id'), nullable=False)



class PoemSubject(db.Model):
    """association table connecting poems with subjects"""

    __tablename__ = 'poems_subjects'

    poems_subjects_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject_code = db.Column(db.String(100), db.ForeignKey('subjects.subject_code'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.poem_id'), nullable=False)




#############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask application"""

    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql:///poetry'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print 'connected to db'