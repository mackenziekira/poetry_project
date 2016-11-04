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

    def __repr__(self):
        """repr for a more readable poem object"""
        return "{}".format(self.title.encode('unicode-escape'))


class Author(db.Model):
    """class for author objects"""

    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'))
    affiliation_id = db.Column(db.Integer, db.ForeignKey('affiliations.affiliation_id'))
    
    birthdate = db.Column(db.Date)
    deathdate = db.Column(db.Date)
    bio = db.Column(db.Text)

    region = db.relationship('Region', backref='authors')
    affiliation = db.relationship('Affiliation', backref='authors')

    def __repr__(self):
        """repr for a more readable author object"""
        return "{}".format(self.name.encode('unicode-escape'))



class Region(db.Model):
    """class for region objects"""

    __tablename__ = 'regions'

    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region_name = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """repr for a more readable region object"""
        return "{}".format(self.region_name)



class Affiliation(db.Model):
    """class for affiliation objects"""

    __tablename__ = 'affiliations'

    affiliation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    affiliation_name = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """repr for a more readable region object"""
        return "{}".format(self.affiliation_name)


class Subject(db.Model):
    """class for subjects"""

    __tablename__ = 'subjects'

    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """repr for a more readable subject object"""
        return "{}".format(self.subject_name)




#################################################################################
#An association tables


class PoemSubject(db.Model):
    """association table connecting poems with subjects"""

    __tablename__ = 'poems_subjects'

    poems_subjects_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
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

