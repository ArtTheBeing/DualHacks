from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import openai
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy_utils import JSONType
from flask_cors import CORS
from generator import Generator

app = Flask(__name__)
CORS(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password=db.Column(db.String(200), nullable=False)
    flashcards = relationship('AllFlashCards', back_populates='author')
    def to_dict(self):
        return{c.name: getattr(self, c.name) for c in self.__table__.columns}    
    
class AllFlashCards(db.Model):
    __tablename__ = 'flashcards'
    id = db.Column(db.Integer, primary_key=True)
    flashcards = db.Column(JSONType)
    author = relationship('Users', back_populates='flashcards')
    author_id = db.Column(db.String(100), ForeignKey('users.id'))

    def to_dict(self):
        return{c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    
    
@app.route("/create_user", methods=["GET", "POST"])
def user():
    content = request.json
    new_user = Users(
        username = content['username'],
        password = content['password'],
    )
    db.session.add(new_user)
    db.session.commit()

@app.route('/create_cards', methods=['POST, GET'])
def flashcards():
    topic = request.args.get('topic')
    user_id = request.args.get('user_id')
    g = Generator(topic)
    flash = AllFlashCards(
        flashcards = g.parser(),
        author_id = user_id,
    )
    db.session.add(flash)
    db.session.commit()

with app.app_context():
     db.create_all()