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
    @validates("name")
    def validate_author(self, key, name):
        if not name:
            raise ValueError("Author name required")
        
        elif Author.query.filter_by(name=name).first():
            raise ValueError("Author already exists")
        
        return name
    
    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if phone_number and not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number MUST be 10 digits long")
        return phone_number

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
    @validates("title")
    def validate_post(self, key, title):
        if not title:
            raise ValueError("Post title required")
        elif "Won't Believe" not in title and "Secret" not in title and "Top [number]" not in title:
            raise ValueError("Title must contain Won't Believe, Secret, Top, or Guess")
        return title
    
    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content too short. Less than 250 chars.")
        return content
    
    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary too long. More than 250 chars.")
        return summary
    
    @validates("category")
    def validate_category(self, key, category):
        if category and category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction") 
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
