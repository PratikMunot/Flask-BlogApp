from flaskblog import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    #we create columns in our Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    email = db.Column(db.String(50), unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)
    def get_reset_token(self,expires_sec=1200):
        s= Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # above line means the posts attribute from our User Model has a
    # relationship with the Post Model. posts is not a column its just a relationship
    # backref means adding another column to the post attribute but not in User model
    # when we have a post we can simply use author to find out who created this post
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)

    def posttime(self):
        dt = str(datetime.now().date())
        t = str(datetime.now().time().hour) + ':' + str(datetime.now().time().minute)
        return "Date - " + dt + " | Time - " + t + " Hrs"

    # print(posttime())
    date_posted = db.Column(db.String, nullable=False, default=posttime)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

