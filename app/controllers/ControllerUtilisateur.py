from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models.ModelUtilisateur import Utilisateur
from models.ModelOrganisme import Organisme
from werkzeug.utils import secure_filename
from database import db
import os

utilisateur_bp = Blueprint("utilisateur", __name__, url_prefix="/utilisateur")

@utilisateur_bp.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = Utilisateur.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash("Connexion réussie!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Email ou mot de passe incorrect", "danger")
    
    return render_template("connexion.html")

@utilisateur_bp.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    flash("Vous avez été déconnecté", "info")
    return redirect(url_for("carte"))

@utilisateur_bp.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        password = request.form.get("password")
        num_adherent = request.form.get("num_adherent")
        
        if Utilisateur.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé", "danger")
            return redirect(url_for("utilisateur.inscription"))
        
        new_user = Utilisateur(
            nom=nom,
            email=email,
            role='user',
            num_adherent=num_adherent
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Inscription réussie! Vous pouvez maintenant vous connecter", "success")
        return redirect(url_for("utilisateur.connexion"))
    
    return render_template("inscription.html")

# Configuration pour les uploads de fichiers
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads/profils'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@utilisateur_bp.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if request.method == 'POST':
        # Réinitialisation de la photo de profil
        if 'reset_photo' in request.form:
            if current_user.photo_profil:
                try:
                    os.remove(os.path.join(current_app.root_path, current_user.photo_profil))
                except Exception as e:
                    print(f"Erreur lors de la suppression de la photo : {e}")
                current_user.photo_profil = None
                db.session.commit()
                flash("Photo de profil réinitialisée.", "success")
                return redirect(url_for('utilisateur.profil'))

        # Gestion de l'upload de la photo de profil
        if 'photo_profil' in request.files:
            file = request.files['photo_profil']
            if file and allowed_file(file.filename):
                extension = file.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"user_{current_user.id_utilisateur}.{extension}")

                upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                filepath = os.path.join(upload_dir, filename)
                file.save(filepath)

                current_user.photo_profil = os.path.join(UPLOAD_FOLDER, filename)

        # Mise à jour des champs texte
        current_user.nom = request.form.get('nom', current_user.nom)
        current_user.num_adherent = request.form.get('num_adherent', current_user.num_adherent)

        # Mise à jour de l'organisme
        if 'id_organisme' in request.form:
            current_user.id_organisme = request.form['id_organisme']

        # Mise à jour de l'email avec vérification
        new_email = request.form.get('email', current_user.email)
        if new_email != current_user.email:
            email_exists = Utilisateur.query.filter(
                Utilisateur.email == new_email,
                Utilisateur.id_utilisateur != current_user.id_utilisateur
            ).first()
            if email_exists:
                flash("Cet email est déjà utilisé par un autre compte", "danger")
                return redirect(url_for('utilisateur.profil'))
            current_user.email = new_email

        # Mise à jour du mot de passe
        new_password = request.form.get('new_password')
        if new_password:
            old_password = request.form.get('old_password')
            if not current_user.check_password(old_password):
                flash("Ancien mot de passe incorrect", "danger")
                return redirect(url_for('utilisateur.profil'))
            current_user.set_password(new_password)
            flash("Mot de passe mis à jour avec succès", "success")

        db.session.commit()
        flash("Profil mis à jour avec succès", "success")
        return redirect(url_for('utilisateur.profil'))

    organismes = Organisme.query.all()
    return render_template('profil.html', user=current_user, organismes=organismes)
