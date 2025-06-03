from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from controllers.ControllerOrganisme import *
from controllers.ControllerFormation import *
from controllers.ControllerUtilisateur import *
from models.ModelUtilisateur import Utilisateur
from models.ModelFormation import Formation
from models.ModelOrganisme import Organisme
from database import *
import os
from dotenv import load_dotenv
from datetime import datetime

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

# Créer l'instance Flask-Mail avant l'import des controllers
mail = Mail()

# Initialiser Flask-Mail après la création de l'app
mail.init_app(app)

@app.route('/')
def carte():
    return render_template("carte.html")

@app.route('/dashboard')
@login_required
def dashboard():
    nb_formations = Formation.query.count()
    nb_organismes = Organisme.query.count()

    formations = []
    if current_user.id_organisme:
        # Récupérer toutes les formations liées à l'organisme de l'utilisateur
        formations = Formation.query.filter_by(id_organisme=current_user.id_organisme).all()

    return render_template('dashboard.html',
                           user=current_user,
                           nb_formations=nb_formations,
                           nb_organismes=nb_organismes,
                           formations=formations)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('404.html'), 403

@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 400

# Catch-all for any other exceptions
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return render_template('404.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)