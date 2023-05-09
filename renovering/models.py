from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from renovering import db, login_manager
from flask import current_app
from flask_login import UserMixin

        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) # post attribute has relationship to Post model. Lazy defines when Alchemy loads data from database.

    def get_reset_token(self, expires_seconds=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __rep__(self):
        return f"User('{self.username}, {self.email}, {self.image_file}')"
    

    # with current_app.app_context():
    #    db.create_all()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    
    content = db.Column(db.Text, nullable=False)
    date_start = db.Column(db.DateTime, nullable=False, default = datetime.today)
    date_end = db.Column(db.DateTime, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # relationen - nyckeln 

    def __rep__(self):
        return f"User('{self.title}, {self.date_posted}')"
    
    # with current_app.app_context():
    #     db.create_all() 


class PostImages(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    info = db.Column(db.String(150), nullable=True)
    data = db.Column(db.BLOB, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)

    def __rep__(self):
        return f"User('{self.info}')"
    