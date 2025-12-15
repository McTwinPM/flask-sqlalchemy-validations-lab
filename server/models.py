from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name', 'phone_number')
    def validate_name(self, key, value):
        if key == 'name':
            if not value:
                raise ValueError("Name cannot be empty")
            duplicate_author = db.session.query(Author).filter(Author.name == value).first()
            if duplicate_author is not None:
                raise ValueError("Author name must be unique")
        if key == 'phone_number':
            if len(value) != 10 or not value.isdigit():
                raise ValueError("Phone number must be exactly 10 digits")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content', 'summary', 'category', 'title') 
    def validate_post(self, key, value):
        if key == 'content':
            if len(value) < 250:
                raise ValueError("Content must be at least 250 characters long")
        if key == 'summary':
            if len(value) > 250:
                raise ValueError("Summary cannot exceed 250 characters")
        if key == 'category':
            if value not in ['Fiction', 'Non-Fiction']:
                raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'")
        if key == 'title':
            clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
            if not any(phrase in value for phrase in clickbait_phrases):
                raise ValueError("Title must contain at least one of the following phrases: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
