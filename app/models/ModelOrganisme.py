from database import db

class Organisme(db.Model):
    __tablename__ = "Organisme"

    id_organisme = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    site_web = db.Column(db.String(100))
    presentation = db.Column(db.Text, nullable=False)
    num_adherent = db.Column(db.String(50))
    statut = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50))
