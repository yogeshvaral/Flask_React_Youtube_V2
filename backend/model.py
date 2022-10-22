from exts import db

"""
class Recipe:
    id: int Primary key
    title: str
    description: str
"""

class Recipe(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"< Recipe {self.title}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, description):
        self.title = title
        self.description = description
        db.session.commit()
    

"""
class User:
    id:Integer
    username:String
    email:String
    password:String
"""
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(255),nullable=False)

    def __repr__(self):
        return f"< User {self.username} >"

    def save(self):
        db.session.add(self)
        db.session.commit()