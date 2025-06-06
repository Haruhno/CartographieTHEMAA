from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models.ModelUtilisateur import Utilisateur
from models.ModelOrganisme import Organisme
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
import os
import re
from functools import wraps
import requests
from flask_mail import Mail, Message
from models.ModelFormation import Formation

utilisateur_bp = Blueprint("utilisateur", __name__, url_prefix="/utilisateur")

# Configuration pour les uploads de fichiers
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads/profils'

# Initialisation de Flask-Mail
mail = Mail()

def allowed_file(filename):
    """
    Vérifie si le fichier a une extension autorisée.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Vérifie si l'utilisateur est authentifié et a le rôle d'administrateur.
        Si ce n'est pas le cas, redirige vers le tableau de bord avec un message d'erreur.
        """
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Accès refusé : vous n'avez pas les permissions nécessaires", "error")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@utilisateur_bp.route("/connexion", methods=["GET", "POST"])
def connexion():
    """
    Gère la connexion des utilisateurs.
    """
    try:
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            
            if not email or not password:
                flash("Veuillez remplir tous les champs", "danger")
                return render_template("connexion.html")
            
            user = Utilisateur.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash("Connexion réussie!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Email ou mot de passe incorrect", "danger")
                return render_template("connexion.html")
        
        return render_template("connexion.html")
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la connexion: {str(e)}")
        flash("Une erreur est survenue lors de la connexion", "danger")
        return render_template("connexion.html"), 500

@utilisateur_bp.route("/deconnexion")
@login_required
def deconnexion():
    """
    Gère la déconnexion des utilisateurs.
    """
    logout_user()
    flash("Vous avez été déconnecté", "info")
    return redirect(url_for("carte"))

@utilisateur_bp.route("/inscription", methods=["GET", "POST"])
def inscription():
    """
    Gère l'inscription des nouveaux utilisateurs.
    Si la méthode est POST, vérifie les données du formulaire, valide le captcha, et crée un nouvel utilisateur.
    Si la méthode est GET, affiche le formulaire d'inscription.
    """
    if request.method == "POST":
        # Vérification du captcha
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not recaptcha_response:
            flash("Veuillez valider le captcha", "danger")
            return redirect(url_for("utilisateur.inscription"))

        # Vérification avec l'API Google
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': current_app.config['RECAPTCHA_PRIVATE_KEY'],
            'response': recaptcha_response
        }
        response = requests.post(verify_url, data=payload)
        result = response.json()

        if not result.get('success', False):
            flash("Échec de la vérification du captcha", "danger")
            return redirect(url_for("utilisateur.inscription"))

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
    """
    Gère le profil de l'utilisateur.
    Si la méthode est POST, traite les mises à jour du profil, y compris la photo de profil, le mot de passe, et les informations personnelles.
    Si la méthode est GET, affiche le formulaire de profil.
    """
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

@utilisateur_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """
    Gère la suppression du compte utilisateur.
    Vérifie le mot de passe avant de supprimer le compte et la photo de profil."""
    password = request.form.get('password')
    
    if not current_user.check_password(password):
        flash("Mot de passe incorrect", "danger")
        return redirect(url_for('utilisateur.profil'))
    
    try:
        # Supprimer la photo de profil si elle existe
        if current_user.photo_profil:
            try:
                filepath = os.path.join(current_app.root_path, current_user.photo_profil)
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                current_app.logger.error(f"Erreur suppression photo: {e}")
        
        # Supprimer l'utilisateur
        user_id = current_user.id_utilisateur
        logout_user()
        user_to_delete = Utilisateur.query.get(user_id)
        db.session.delete(user_to_delete)
        db.session.commit()
        
        flash("Votre compte a été supprimé avec succès", "success")
        return redirect(url_for('carte'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur suppression compte: {e}")
        flash("Une erreur est survenue lors de la suppression du compte", "danger")
        return redirect(url_for('utilisateur.profil'))

@utilisateur_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    Gère la demande de réinitialisation du mot de passe.
    Si la méthode est POST, envoie un email avec les instructions de réinitialisation.
    Si la méthode est GET, affiche le formulaire de demande de réinitialisation.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        user = Utilisateur.query.filter_by(email=email).first()
        
        if user:
            token = user.generate_reset_token()
            reset_url = url_for('utilisateur.reset_password', token=token, _external=True)
            
            msg = Message('Réinitialisation de votre mot de passe THEMAA',
                        sender='noreply@themaa.fr',
                        recipients=[user.email])
            
            msg.body = f'''Bonjour {user.nom},

Vous avez demandé la réinitialisation de votre mot de passe sur le site THEMAA.

Pour procéder au changement de votre mot de passe, veuillez cliquer sur le lien suivant :
{reset_url}

Ce lien est valable pendant 24 heures.

Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email. Votre mot de passe actuel restera inchangé.

Pour votre sécurité :
- Ne transmettez jamais ce lien à qui que ce soit
- Le service THEMAA ne vous demandera jamais votre mot de passe par email

Cordialement,
L'équipe THEMAA

---
Ceci est un message automatique, merci de ne pas y répondre.
'''
            try:
                mail.send(msg)
                flash('Un email avec les instructions de réinitialisation vous a été envoyé.', 'success')
                return redirect(url_for('utilisateur.connexion'))
            except Exception as e:
                current_app.logger.error(f"Erreur lors de l'envoi de l'email : {e}")
                flash("Impossible d'envoyer l'email. Veuillez réessayer plus tard.", "error")
                return redirect(url_for('utilisateur.reset_password_request'))

        # Message volontairement vague pour la sécurité
        flash('Si cette adresse email existe dans notre base, vous recevrez les instructions de réinitialisation.', 'info')
        return redirect(url_for('utilisateur.connexion'))
        
    return render_template('reset_password_request.html')

@utilisateur_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Gère la réinitialisation du mot de passe.
    Si la méthode est POST, met à jour le mot de passe de l'utilisateur.
    Si la méthode est GET, vérifie le token et affiche le formulaire de réinitialisation.
    """
    user = Utilisateur.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Le lien de réinitialisation est invalide ou a expiré', 'error')
        return redirect(url_for('utilisateur.reset_password_request'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        if password != password2:
            flash('Les mots de passe ne correspondent pas', 'error')
            return render_template('reset_password.html')
            
        if len(password) < 5:
            flash('Le mot de passe doit contenir au moins 5 caractères', 'error')
            return render_template('reset_password.html')
            
        user.set_password(password)
        user.reset_token = None
        user.reset_token_expiration = None
        db.session.commit()
        
        flash('Votre mot de passe a été mis à jour', 'success')
        return redirect(url_for('utilisateur.connexion'))
        
    return render_template('reset_password.html')

@utilisateur_bp.route("/new", methods=["GET"])
@admin_required
def new_utilisateur():
    """
    Affiche le formulaire de création d'un nouvel utilisateur.
    Récupère la liste des organismes pour les afficher dans le formulaire.
    """
    try:
        organismes = Organisme.query.all()  # Récupérer les organismes
        return render_template(
            "new_utilisateur.html",
            organismes=organismes,  # Passer les organismes au template
            user=current_user
        )
    except Exception as e:
        current_app.logger.error(f"Error in new_utilisateur: {str(e)}")
        flash("Une erreur est survenue lors du chargement de la page", "error")
        return redirect(url_for('utilisateur.edit_utilisateurs'))

@utilisateur_bp.route("/edit", methods=["GET"])
@admin_required
def edit_utilisateurs():
    """
    Affiche la liste des utilisateurs pour les administrateurs.
    Récupère tous les utilisateurs et les organismes pour les afficher dans le formulaire d'édition.
    """
    try:
        utilisateurs = Utilisateur.query.all()
        organismes = Organisme.query.all()
        roles = ['admin', 'user']
        return render_template(
            "edit_utilisateurs.html",
            utilisateurs=utilisateurs,
            organismes=organismes,
            roles=roles,
            user=current_user
        )
    except Exception as e:
        current_app.logger.error(f"Error in edit_utilisateurs: {str(e)}")
        flash("Une erreur est survenue lors du chargement de la page", "error")
        return redirect(url_for('dashboard'))

@utilisateur_bp.route("/update", methods=["POST"])
@admin_required
def update_utilisateurs():
    """
    Met à jour les informations des utilisateurs.
    Si un utilisateur est supprimé, il est retiré de la base de données.
    Si des informations sont modifiées, elles sont mises à jour dans la base de données.
    """
    if "delete" in request.form:
        id_ = request.form["delete"]
        utilisateur = Utilisateur.query.get_or_404(int(id_))
        if utilisateur.id_utilisateur == current_user.id_utilisateur:
            flash("Vous ne pouvez pas supprimer votre propre compte.", "error")
            return redirect(url_for("utilisateur.edit_utilisateurs"))
        db.session.delete(utilisateur)
        db.session.commit()
        flash("Utilisateur supprimé avec succès.", "success")
        return redirect(url_for("utilisateur.edit_utilisateurs"))

    for key, value in request.form.items():
        if key.startswith("nom_"):
            id_ = key.split("_")[1]
            utilisateur = Utilisateur.query.get(int(id_))
            if utilisateur:
                utilisateur.nom = value
                utilisateur.email = request.form.get(f"email_{id_}")
                utilisateur.role = request.form.get(f"role_{id_}")
                utilisateur.id_organisme = request.form.get(f"id_organisme_{id_}") if request.form.get(f"id_organisme_{id_}") else None

    db.session.commit()
    flash("Tous les utilisateurs ont été mis à jour avec succès.", "success")
    return redirect(url_for("utilisateur.edit_utilisateurs"))

@utilisateur_bp.route('/preview/<int:id>', methods=['GET'])
@admin_required
def preview_utilisateur(id):
    """
    Affiche les détails d'un utilisateur.
    Récupère l'utilisateur par son ID et affiche ses informations dans un template.
    """
    utilisateur = Utilisateur.query.get_or_404(id)
    organismes = Organisme.query.all()
    roles = ['admin', 'user']
    return render_template("preview_utilisateur.html", 
                         utilisateur=utilisateur,
                         organismes=organismes,
                         roles=roles)

@utilisateur_bp.route("/update/<int:id>", methods=["POST"])
@admin_required
def update_utilisateur_by_id(id):
    """
    Met à jour les informations d'un utilisateur.
    Gère la réinitialisation de la photo de profil, le retrait d'organisme, et les mises à jour des informations utilisateur.
    Si la requête est en JSON, elle traite les données JSON pour mettre à jour l'utilisateur.
    """
    utilisateur = Utilisateur.query.get_or_404(id)
    
    try:
        # Traitement de la réinitialisation de la photo
        if 'reset_photo' in request.form:
            if utilisateur.photo_profil:
                try:
                    filepath = os.path.join(current_app.root_path, utilisateur.photo_profil)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except Exception as e:
                    current_app.logger.error(f"Erreur suppression photo: {e}")
                utilisateur.photo_profil = None
                db.session.commit()
                flash("Photo de profil supprimée avec succès", "success")
                return redirect(url_for('utilisateur.preview_utilisateur', id=id))

        # Traitement du retrait d'organisme
        if 'retirer_organisme' in request.form:
            utilisateur.id_organisme = None
            db.session.commit()
            flash("L'organisme a été retiré avec succès", "success")
            return redirect(url_for('utilisateur.preview_utilisateur', id=id))

        # Traitement des données JSON (sauvegarde individuelle)
        if request.is_json:
            data = request.get_json()
            utilisateur.nom = data.get("nom")
            utilisateur.email = data.get("email")
            utilisateur.role = data.get("role")
            utilisateur.num_adherent = data.get("num_adherent") if data.get("num_adherent") else None
            utilisateur.id_organisme = int(data.get("id_organisme")) if data.get("id_organisme") else None
            
            db.session.commit()
            return jsonify({"success": True, "message": "Utilisateur mis à jour avec succès"})

        # Traitement du formulaire standard
        else:
            utilisateur.nom = request.form.get("nom")
            utilisateur.email = request.form.get("email")
            utilisateur.role = request.form.get("role")
            utilisateur.num_adherent = request.form.get("num_adherent") if request.form.get("num_adherent") else None
            utilisateur.id_organisme = request.form.get("id_organisme") if request.form.get("id_organisme") else None

            # Gestion de la photo de profil
            if 'photo_profil' in request.files:
                file = request.files['photo_profil']
                if file and file.filename != '':
                    if allowed_file(file.filename):
                        # Supprimer l'ancienne photo si elle existe
                        if utilisateur.photo_profil:
                            try:
                                old_filepath = os.path.join(current_app.root_path, utilisateur.photo_profil)
                                if os.path.exists(old_filepath):
                                    os.remove(old_filepath)
                            except Exception as e:
                                current_app.logger.error(f"Erreur suppression ancienne photo: {e}")

                        # Sauvegarder la nouvelle photo
                        extension = file.filename.rsplit('.', 1)[1].lower()
                        filename = secure_filename(f"user_{utilisateur.id_utilisateur}.{extension}")
                        upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
                        if not os.path.exists(upload_dir):
                            os.makedirs(upload_dir)
                        filepath = os.path.join(upload_dir, filename)
                        file.save(filepath)
                        utilisateur.photo_profil = os.path.join(UPLOAD_FOLDER, filename).replace('\\', '/')
                    else:
                        flash("Format de fichier non autorisé", "error")
                        return redirect(url_for('utilisateur.preview_utilisateur', id=id))

            # Gestion du mot de passe
            new_password = request.form.get("new_password")
            if new_password:
                if new_password != request.form.get("confirm_password"):
                    flash("Les mots de passe ne correspondent pas", "error")
                    return redirect(url_for('utilisateur.preview_utilisateur', id=id))
                utilisateur.set_password(new_password)

            db.session.commit()
            flash("Utilisateur mis à jour avec succès", "success")
            return redirect(url_for('utilisateur.edit_utilisateurs', id=id))

    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({"success": False, "message": str(e)})
        flash(f"Erreur lors de la mise à jour : {str(e)}", "error")
        return redirect(url_for('utilisateur.preview_utilisateur', id=id))

@utilisateur_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_utilisateur(id):
    """
    Supprime un utilisateur.
    Vérifie si l'utilisateur à supprimer n'est pas l'utilisateur actuel.
    Si c'est le cas, affiche un message d'erreur.
    Supprime également la photo de profil si elle existe.
    """
    utilisateur = Utilisateur.query.get_or_404(id)
    if utilisateur.id_utilisateur == current_user.id_utilisateur:
        flash("Vous ne pouvez pas supprimer votre propre compte.", "error")
        return redirect(url_for("utilisateur.edit_utilisateurs"))
    
    try:
        # Supprimer la photo de profil si elle existe
        if utilisateur.photo_profil:
            try:
                filepath = os.path.join(current_app.root_path, utilisateur.photo_profil)
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                current_app.logger.error(f"Erreur suppression photo: {e}")
        
        db.session.delete(utilisateur)
        db.session.commit()
        flash("Utilisateur supprimé avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "error")
    
    return redirect(url_for("utilisateur.edit_utilisateurs"))

@utilisateur_bp.route("/create", methods=["POST"])
@admin_required
def create_utilisateur():
    """
    Crée un nouvel utilisateur.
    Vérifie les champs obligatoires, l'unicité de l'email, et crée un nouvel utilisateur dans la base de données.
    """
    try:
        nom = request.form.get("nom")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "user")  # Par défaut 'user'
        num_adherent = request.form.get("num_adherent")
        id_organisme = request.form.get("id_organisme")

        if not nom or not email or not password:
            flash("Tous les champs obligatoires doivent être remplis", "error")
            return redirect(url_for("utilisateur.new_utilisateur"))

        if Utilisateur.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé", "error")
            return redirect(url_for("utilisateur.new_utilisateur"))

        new_user = Utilisateur(
            nom=nom,
            email=email,
            role=role,
            num_adherent=num_adherent if num_adherent else None,
            id_organisme=id_organisme if id_organisme else None
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash("Utilisateur créé avec succès", "success")
        return redirect(url_for("utilisateur.edit_utilisateurs"))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in create_utilisateur: {str(e)}")
        flash(f"Erreur lors de la création de l'utilisateur : {str(e)}", "error")
        return redirect(url_for("utilisateur.new_utilisateur"))

@utilisateur_bp.route('/contact_admin_organisme', methods=['POST'])
@login_required
def contact_admin_organisme():
    """
    Gère les demandes de modification d'organisme.
    Si la méthode est POST, envoie un email aux administrateurs avec les détails de la demande.
    Si la méthode est GET, affiche le formulaire de demande de modification d'organisme.
    """
    try:
        request_type = request.form.get('request_type')
        message = request.form.get('message')
        
        # Préparer l'email
        subject = f"Demande de modification d'organisme - {current_user.nom}"
        body = f"""
Une nouvelle demande de modification d'organisme a été soumise :

Utilisateur : {current_user.nom} (ID: {current_user.id_utilisateur})
Email : {current_user.email}
Organisme actuel : {current_user.organisme.nom if current_user.organisme else 'Aucun'}
Type de demande : {'Changement' if request_type == 'change' else 'Retrait'} d'organisme

Message de l'utilisateur :
{message}

---
Cet email a été envoyé automatiquement depuis le site THEMAA.
"""
        # Envoyer l'email aux administrateurs
        admins = Utilisateur.query.filter_by(role='admin').all()
        for admin in admins:
            msg = Message(subject,
                        sender='noreply@themaa.fr',
                        recipients=[admin.email])
            msg.body = body
            mail.send(msg)

        flash("Votre demande a été envoyée aux administrateurs. Vous serez contacté prochainement.", "success")
        return redirect(url_for('utilisateur.profil'))

    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi de la demande : {e}")
        flash("Une erreur est survenue lors de l'envoi de votre demande. Veuillez réessayer plus tard.", "error")
        return redirect(url_for('utilisateur.profil'))

@utilisateur_bp.route('/support', methods=['GET', 'POST'])
@login_required
def support():
    """
    Affiche la page de support pour les utilisateurs.
    """
    return render_template('support.html', user=current_user)

@utilisateur_bp.route('/contact_support', methods=['POST'])
@login_required
def contact_support():
    """
    Gère les demandes de support des utilisateurs.
    Si la méthode est POST, envoie un email aux administrateurs avec les détails de la demande.
    Si la méthode est GET, affiche le formulaire de demande de support.
    """
    try:
        subject = request.form.get('subject')
        priority = request.form.get('priority')
        message = request.form.get('message')

        # Préparer l'email pour les administrateurs
        subject_map = {
            'probleme_technique': 'Problème technique',
            'question_compte': 'Question sur le compte',
            'suggestion': 'Suggestion d\'amélioration',
            'autre': 'Autre demande'
        }

        email_subject = f"[Support THEMAA] {subject_map.get(subject, 'Demande')} - {priority.upper()}"
        email_body = f"""
Une nouvelle demande de support a été soumise :

Utilisateur : {current_user.nom}
ID : {current_user.id_utilisateur}
Email : {current_user.email}
Organisme : {current_user.organisme.nom if current_user.organisme else 'Aucun'}

Sujet : {subject_map.get(subject, 'Non spécifié')}
Priorité : {priority.upper()}

Message :
{message}

---
Cette demande a été envoyée depuis le formulaire de support THEMAA.
"""
        # Envoyer l'email aux administrateurs
        admins = Utilisateur.query.filter_by(role='admin').all()
        for admin in admins:
            msg = Message(
                subject=email_subject,
                sender='noreply@themaa.fr',
                recipients=[admin.email],
                body=email_body
            )
            mail.send(msg)

        flash("Votre demande a été envoyée avec succès. Notre équipe vous répondra dans les plus brefs délais.", "success")
        return redirect(url_for('utilisateur.support'))

    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi de la demande de support : {e}")
        flash("Une erreur est survenue lors de l'envoi de votre demande. Veuillez réessayer plus tard.", "error")
        return redirect(url_for('utilisateur.support'))



