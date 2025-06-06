from flask import Flask, render_template, send_file
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
from datetime import datetime, timezone
import csv
import io
import json

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
    nb_users = Utilisateur.query.count()
    users = Utilisateur.query.all()

    # Récupérer toutes les formations pour l'administrateur
    if current_user.role == 'admin':
        formations = Formation.query.all()
    else:
        formations = Formation.query.filter_by(id_organisme=current_user.id_organisme).all() if current_user.id_organisme else []

    return render_template('dashboard.html',
                         user=current_user,
                         nb_formations=nb_formations,
                         nb_organismes=nb_organismes,
                         nb_users=nb_users,
                         users=users,
                         formations=formations)


@app.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}

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

# Ajouter après les autres routes
@app.route('/export/<string:type>/<string:format>')
@login_required
@admin_required
def export_data(type, format):
    if type == 'organismes':
        data = Organisme.query.all()
        fields = ['id_organisme', 'nom', 'adresse', 'email', 'telephone', 
                 'site_web', 'presentation', 'num_adherent', 'statut', 'label']
    else:
        data = Formation.query.all()
        fields = ['id_formation', 'nom', 'type', 'description', 'duree', 
                 'duree_heures', 'dates', 'lieu', 'prix', 'conditions_acces',
                 'financement', 'presentation_intervenants', 'lien_inscription',
                 'label', 'certifications', 'id_organisme', 'etat']

    if format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(fields)
        
        for item in data:
            row = []
            for field in fields:
                value = getattr(item, field)
                row.append(str(value) if value is not None else '')
            writer.writerow(row)
            
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{type}_export.csv'
        )

    elif format == 'json':
        result = []
        for item in data:
            item_dict = {}
            for field in fields:
                value = getattr(item, field)
                item_dict[field] = str(value) if value is not None else None
            result.append(item_dict)

        return send_file(
            io.BytesIO(json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'{type}_export.json'
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)