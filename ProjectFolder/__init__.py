
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_login import LoginManager

from ProjectFolder.Components.Analyser import Analyser

# Code takened and adapted from Digital Ocean:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-5-creating-user-models

#creating the databae
db = SQLAlchemy()

def create_app():
    #code takened and adapted from Flask: 
    #https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
    UPLOAD_FOLDER = './uploads'
    DOWNLOAD_FOLDER = './downloads' #Original Addition
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    #Flask addition ends here ^
    app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER #Original Addition
    app.config['SECRET_KEY'] = 'Ge-cwoTGa0xctuy5ivQJvQ'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    skill_pattern_path = "ProjectFolder/Components/ModelData/jz_skill_patterns.jsonl" #Original Addition

    Markdown(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    AN = Analyser() #Original Addition
    AN.createSkillsExtractor(skill_pattern_path) #Original Addition
    app.config['Analyser'] = AN  #Original Addition
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app