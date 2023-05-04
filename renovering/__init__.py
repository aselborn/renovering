from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from renovering.config import Config 
# from flask import current_app

# current_app.app_context().push()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # function name of the route - blueprint för users
login_manager.login_message_category = 'info' # maps to bootstrap ?


mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # from flaskblog import routes
    from renovering.users.routes import users
    from renovering.posts.routes import posts 
    from renovering.main.routes import main 
    from renovering.errors.handlers import errors # instance of bluepring (errors = Blueprint('errors, __name__'))


    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors) # registrerar error-blueprint...!
    
    with app.app_context():
        db.create_all()

    return app 

