from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Utilisateur(db.Model, UserMixin):
    __tablename__ = "Utilisateur"

    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('visiteur', 'user', 'admin'), nullable=False, default='visiteur')
    num_adherent = db.Column(db.String(50))
    id_organisme = db.Column(db.Integer, db.ForeignKey('Organisme.id_organisme'))
    photo_profil = db.Column(db.String(255))  # Chemin vers l'image

    def set_password(self, password):
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe, password)

    def get_id(self):
        return str(self.id_utilisateur)

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    def is_visiteur(self):
        return self.role == 'visiteur'