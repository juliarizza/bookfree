from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Info
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False) # create an specific table
    publisher = db.Column(db.String, nullable=False) # create an specific table
    gender = db.Column(db.String, nullable=False) # create an specific table
    isbn = db.Column(db.String)

    def __repr__(self):
        return "%s - %s" % (self.author,self.title)