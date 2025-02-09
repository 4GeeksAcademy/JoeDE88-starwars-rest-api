import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String
from dataclasses import dataclass,field

db = SQLAlchemy()

@dataclass
class Users(db.Model):
    __tablename__ = 'users'
    user_id:int = db.Column(db.Integer, primary_key=True)
    email:str = db.Column(db.String(120), unique=True, nullable=False)
    username:str = db.Column(db.String(50), nullable=False,unique=True)
    firstname:str = db.Column(db.String(50),nullable=False)
    lastname:str = db.Column(db.String(50),nullable=False)
    password = db.Column(db.VARCHAR(60), unique=False, nullable=False)
    is_active:bool = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.username

    """def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }"""
    
class FavoritesType(str,enum.Enum):
    films = "films"
    planets = "planets"
    people = "people"

@dataclass
class Favorites(db.Model):
    __tablename__ = 'favorites'
    favorite_id:int = db.Column(db.Integer,unique=True, primary_key=True,index=True)
    user_id:int = db.Column(db.Integer, ForeignKey('users.user_id'),nullable=False)
    external_id:int = db.Column(db.Integer,nullable=False)
    name:str = db.Column(db.String(50), unique=True,nullable=False)
    type_enum: FavoritesType = db.Column(db.Enum(FavoritesType), nullable=False)

@dataclass
class Films(db.Model):
    __tablename__ = 'films'
    id:int = db.Column(db.Integer,primary_key=True,unique=True)
    name:str = db.Column(db.String(50),nullable=False,unique=True)
    episode:int = db.Column(db.Integer,nullable=False,unique=True)
    release_date:int = db.Column(db.Integer,nullable=False)
    opening_crawl:int = db.Column(db.String(500),nullable=False)
    director:str = db.Column(db.String(50),nullable=False)
    producer:str = db.Column(db.String(50),nullable=False)

@dataclass
class Planets(db.Model):
    __tablename__ = 'planets'
    id:int = db.Column(db.Integer,primary_key=True,unique=True)
    name:str = db.Column(db.String(50),nullable=False,unique=True)
    population:int = db.Column(db.Integer,nullable=False)
    climate:str = db.Column(db.String(50),nullable=False)
    diameter:str = db.Column(db.String(50),nullable=False)
    gravity:int = db.Column(db.Integer,nullable=False)

@dataclass
class People(db.Model):
    __tablename__ = 'people'
    id:int = db.Column(db.Integer,primary_key=True,unique=True)
    name:str = db.Column(db.String(50),unique=True,nullable=False)
    species:str = db.Column(db.String(50),nullable=False)
    skin_color:str = db.Column(db.String(50),nullable=False)
    hair_color:str = db.Column(db.String(50),nullable=False)
    height:int = db.Column(db.Integer,nullable=False)
    homeworld:int = db.Column(db.Integer,ForeignKey('planets.id'),nullable=False)