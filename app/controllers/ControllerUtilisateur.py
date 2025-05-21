from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models.ModelUtilisateur import Utilisateur
from models.ModelOrganisme import Organisme
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
import os
import re
from functools import wraps

utilisateur_bp = Blueprint("utilisateur", __name__, url_prefix="/utilisateur")

# Configuration pour les uploads de fichiers
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads/profils'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Ajoutez ce décorateur si vous n'avez pas créé le fichier de décorateurs séparé
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Accès refusé : vous n'avez pas les permissions nécessaires", "error")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

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
        
        # Validations
        if not nom or len(nom.strip()) == 0 or len(nom) > 50:
            flash("Le nom doit contenir entre 1 et 50 caractères", "danger")
            return redirect(url_for("utilisateur.inscription"))
            
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or len(email) > 100:
            flash("Veuillez entrer une adresse email valide (max 100 caractères)", "danger")
            return redirect(url_for("utilisateur.inscription"))
            
        if len(password) < 5 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
            flash("Le mot de passe doit contenir au moins 5 caractères, une majuscule et un chiffre", "danger")
            return redirect(url_for("utilisateur.inscription"))
            
        if num_adherent and len(num_adherent) > 50:
            flash("Le numéro d'adhérent ne doit pas dépasser 50 caractères", "danger")
            return redirect(url_for("utilisateur.inscription"))

        if Utilisateur.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé", "danger")
            return redirect(url_for("utilisateur.inscription"))
        
        new_user = Utilisateur(
            nom=nom,
            email=email,
            role='user',
            num_adherent=num_adherent if num_adherent else None
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Inscription réussie! Vous pouvez maintenant vous connecter", "success")
            return redirect(url_for("utilisateur.connexion"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'inscription: {str(e)}", "danger")
    
    return render_template("inscription.html")

@utilisateur_bp.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if request.method == 'POST':
        # Réinitialisation de la photo de profil
        if 'reset_photo' in request.form:
            if current_user.photo_profil:
                try:
                    filepath = os.path.join(current_app.root_path, current_user.photo_profil)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except Exception as e:
                    current_app.logger.error(f"Erreur suppression photo: {e}")
                current_user.photo_profil = None
                db.session.commit()
                flash("Photo de profil réinitialisée.", "success")
                return redirect(url_for('utilisateur.profil'))
            
        if 'retirer_organisme' in request.form:
            current_user.id_organisme = None
            db.session.commit()
            flash("Organisme retiré avec succès.", "success")
            return redirect(url_for("utilisateur.profil"))

        # Vérification du nom complet
        nom = request.form.get('nom')
        if not nom or len(nom.strip()) == 0:
            flash("Le nom complet est obligatoire.", "danger")
            return redirect(url_for("utilisateur.profil"))
        if len(nom) > 50:
            flash("Le nom complet ne doit pas dépasser 50 caractères.", "danger")
            return redirect(url_for("utilisateur.profil"))

        # Vérification de l'email
        email = request.form.get('email')
        if not email or len(email.strip()) == 0:
            flash("L'email est obligatoire.", "danger")
            return redirect(url_for("utilisateur.profil"))
        if len(email) > 100:
            flash("L'email ne doit pas dépasser 100 caractères.", "danger")
            return redirect(url_for("utilisateur.profil"))
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Veuillez entrer une adresse email valide.", "danger")
            return redirect(url_for("utilisateur.profil"))

        # Vérification unicité email
        if email != current_user.email:
            if Utilisateur.query.filter(Utilisateur.email == email).first():
                flash("Cet email est déjà utilisé par un autre compte", "danger")
                return redirect(url_for('utilisateur.profil'))

        # Vérification numéro adhérent
        num_adherent = request.form.get('num_adherent')
        if num_adherent and len(num_adherent) > 50:
            flash("Le numéro d'adhérent ne doit pas dépasser 50 caractères.", "danger")
            return redirect(url_for("utilisateur.profil"))

        # Vérification mot de passe
        new_password = request.form.get('new_password')
        if new_password:
            old_password = request.form.get('old_password')
            if not old_password:
                flash("Vous devez fournir l'ancien mot de passe pour le changer", "danger")
                return redirect(url_for('utilisateur.profil'))
                
            if not current_user.check_password(old_password):
                flash("Ancien mot de passe incorrect", "danger")
                return redirect(url_for('utilisateur.profil'))
            
            if current_user.check_password(new_password):
                flash("Le nouveau mot de passe ne peut pas être identique à l'ancien", "danger")
                return redirect(url_for('utilisateur.profil'))

            if len(new_password) < 5:
                flash("Le mot de passe doit contenir au moins 5 caractères", "danger")
                return redirect(url_for('utilisateur.profil'))
                
        # Vérification photo de profil
        if 'photo_profil' in request.files:
            file = request.files['photo_profil']
            if file and file.filename != '':
                if not allowed_file(file.filename):
                    flash("Format de fichier non autorisé. Utilisez JPG, PNG ou GIF.", "danger")
                    return redirect(url_for('utilisateur.profil'))
                
                # Vérification taille fichier (2MB max)
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                if file_length > 2 * 1024 * 1024:
                    flash("La photo ne doit pas dépasser 2MB", "danger")
                    return redirect(url_for('utilisateur.profil'))
                file.seek(0)

        # Mise à jour des informations
        try:
            current_user.nom = nom
            current_user.email = email
            current_user.num_adherent = num_adherent if num_adherent else None

            # Mise à jour mot de passe si fourni
            if new_password:
                current_user.set_password(new_password)
                flash("Mot de passe mis à jour avec succès", "success")

            # Mise à jour photo si fournie
            if 'photo_profil' in request.files and file and file.filename != '':
                # Supprimer l'ancienne photo si elle existe
                if current_user.photo_profil:
                    try:
                        old_filepath = os.path.join(current_app.root_path, current_user.photo_profil)
                        if os.path.exists(old_filepath):
                            os.remove(old_filepath)
                    except Exception as e:
                        current_app.logger.error(f"Erreur suppression ancienne photo: {e}")

                # Sauvegarder la nouvelle photo
                extension = file.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"user_{current_user.id_utilisateur}.{extension}")
                upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                filepath = os.path.join(upload_dir, filename)
                file.save(filepath)
                current_user.photo_profil = os.path.join(UPLOAD_FOLDER, filename)

            # Mise à jour organisme
            if 'id_organisme' in request.form:
                current_user.id_organisme = request.form['id_organisme'] if request.form['id_organisme'] else None

            db.session.commit()
            flash("Profil mis à jour avec succès", "success")
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur mise à jour profil: {e}")
            flash("Une erreur est survenue lors de la mise à jour du profil", "danger")

        next_url = request.form.get('next_url')
        if next_url:
            return redirect(next_url)
        else:
            # Rester sur la page profil avec un message de succès
            return redirect(url_for('utilisateur.profil'))

    # GET request - afficher le formulaire
    organismes = Organisme.query.all()
    return render_template('profil.html', user=current_user, organismes=organismes)