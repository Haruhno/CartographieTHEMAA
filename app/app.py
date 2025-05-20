from flask import Flask, render_template
from flask_login import LoginManager
from controllers.ControllerOrganisme import *
from controllers.ControllerFormation import *
from controllers.ControllerUtilisateur import *
from models.ModelUtilisateur import Utilisateur
from models.ModelFormation import Formation
from models.ModelOrganisme import Organisme
from database import *
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis .env

app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = os.getenv('SECRET_KEY')

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'utilisateur.connexion'

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

init_db(app)

app.register_blueprint(organisme_bp)
app.register_blueprint(formation_bp)
app.register_blueprint(utilisateur_bp)

@app.route('/')
def carte():
    return render_template("carte.html")

@app.route('/dashboard')
@login_required
def dashboard():
    nb_formations = Formation.query.count()
    nb_organismes = Organisme.query.count()
    return render_template('dashboard.html', user=current_user,
                           nb_formations=nb_formations,
                           nb_organismes=nb_organismes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)