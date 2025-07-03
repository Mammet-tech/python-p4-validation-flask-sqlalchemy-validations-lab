from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name', 'phone_number')
    def validate_author(self, key,value):
        if key == 'name':
            if not value or not value.strip():
                raise ValueError('Name cannot be empty')
            existing = Author.query.filter_by(name=value.strip()).first()
            if existing and existing.id != self.id:
                raise ValueError('Author with this name already exists')
            return value.strip()
        elif key == 'phone_number':
            digit = ''.join(filter(str.isdigit, value)) if value else ''
            if len(digit) != 10:
                raise ValueError('Phone number must be 10 digits long')
            return digit

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

    # Add validators
    @validates('title', 'content', 'category', 'summary')
    def validate_post(self, key, value):
        if key == 'content':
            if value and len(value) < 250:
                raise ValueError('Content must be at least 250 characters long')
            return value
        elif key == 'summary':
            if value and len(value) > 250:
                raise ValueError('Summary must be at most 250 characters long')
            return value
        elif key == 'category':
            if value not in ['Fiction', 'Non-Fiction']:
                raise ValueError('Category must be either Fiction or Non-Fiction')
            return value
        elif key == 'title':
            clickbait_keywords = ["won't believe", "secret", "top", "guess"]
            lowercase_title = value.lower()
            if not any(keyword in lowercase_title for keyword in clickbait_keywords):
                raise ValueError("Title must be clickbait-y: include one of 'Won't Believe', 'Secret', 'Top', or 'Guess'")
            return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
