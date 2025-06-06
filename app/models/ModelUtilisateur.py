from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets

class Utilisateur(db.Model, UserMixin):
    """
    Modèle représentant un utilisateur de l'application.
    
    Attributs :
        id_utilisateur (int) : Identifiant unique de l'utilisateur (clé primaire).
        nom (str) : Nom de l'utilisateur.
        email (str) : Adresse email de l'utilisateur (doit être unique).
        mot_de_passe (str) : Mot de passe haché de l'utilisateur.
        role (Enum) : Rôle de l'utilisateur ('visiteur', 'user', 'admin').
        num_adherent (str) : Numéro d'adhérent de l'utilisateur (optionnel).
        id_organisme (int) : Clé étrangère vers l'organisme associé.
        photo_profil (str) : Chemin vers la photo de profil de l'utilisateur (optionnel).
        reset_token (str) : Jeton de réinitialisation du mot de passe (optionnel).
        reset_token_expiration (datetime) : Date d'expiration du jeton de réinitialisation.
        
    Relations :
        organisme (Organisme) : Organisme auquel l'utilisateur est rattaché.
        
    Méthodes :

        set_password(password) : Définit le mot de passe de l'utilisateur (haché).
        check_password(password) : Vérifie si le mot de passe fourni correspond au mot de passe haché.
        get_id() : Retourne l'identifiant de l'utilisateur sous forme de chaîne.
        is_admin() : Retourne True si l'utilisateur a le rôle 'admin'.
        is_user() : Retourne True si l'utilisateur a le rôle 'user'.
        is_visiteur() : Retourne True si l'utilisateur a le rôle 'visiteur'.
        generate_reset_token() : Génère un jeton de réinitialisation du mot de passe et définit son expiration.
        verify_reset_token(token) : Vérifie la validité d'un jeton de réinitialisation.
    """
    __tablename__ = "Utilisateur"

    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('visiteur', 'user', 'admin'), nullable=False, default='visiteur')
    num_adherent = db.Column(db.String(150))
    id_organisme = db.Column(db.Integer, db.ForeignKey('Organisme.id_organisme'))
    photo_profil = db.Column(db.String(255))  # Chemin vers l'image
    reset_token = db.Column(db.String(100))
    reset_token_expiration = db.Column(db.DateTime)

    # Relation avec Organisme
    organisme = db.relationship('Organisme', backref='utilisateurs')

    def set_password(self, password):
        """
        Définit le mot de passe de l'utilisateur (haché).
        """
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        """
        Vérifie si le mot de passe fourni correspond au mot de passe haché.
        """
        return check_password_hash(self.mot_de_passe, password)

    def get_id(self):
        """
        Retourne l'identifiant de l'utilisateur sous forme de chaîne.
        """
        return str(self.id_utilisateur)

    def is_admin(self):
        """
        Vérifie si l'utilisateur a le rôle 'admin'.
        """
        return self.role == 'admin'

    def is_user(self):
        """
        Vérifie si l'utilisateur a le rôle 'user'.
        """
        return self.role == 'user'

    def is_visiteur(self):
        """
        Vérifie si l'utilisateur a le rôle 'visiteur'.
        """
        return self.role == 'visiteur'

    def generate_reset_token(self):
        """
        Génère un jeton de réinitialisation du mot de passe et définit son expiration.
        Le jeton est stocké dans l'attribut reset_token et sa validité est de 1 heure.
        """
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return self.reset_token

    def verify_reset_token(self, token):
        """
        Vérifie la validité d'un jeton de réinitialisation.
        """
        if not self.reset_token or not self.reset_token_expiration:
            return False
        if token != self.reset_token:
            return False
        if datetime.utcnow() > self.reset_token_expiration:
            return False
        return True