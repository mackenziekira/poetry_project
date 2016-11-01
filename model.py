"""Models and database functions for Poetry project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Poem(db.Model):
    """class for poem objects"""

    __tablename__ = 'poems'

    poem_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200))
    author_id = db.Column(db.ForeignKey)