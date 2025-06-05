from database import db

class Formation(db.Model):
    __tablename__ = "Formation"

    id_formation = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum('initiale', 'continue'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duree = db.Column(db.String(50), nullable=False)
    duree_heures = db.Column(db.Float, nullable=True)
    dates = db.Column(db.String(100), nullable=False)
    lieu = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Numeric(10, 2), nullable=True)
    conditions_acces = db.Column(db.Text)
    financement = db.Column(db.String(100))
    presentation_intervenants = db.Column(db.Text)
    lien_inscription = db.Column(db.String(200))
    label = db.Column(db.String(50))
    certifications = db.Column(db.String(255))
    id_organisme = db.Column(db.Integer, db.ForeignKey('Organisme.id_organisme'), nullable=False)
    etat = db.Column(db.Enum('valide', 'en_attente', name='etat_formation'), nullable=False, default='en_attente')
    raison = db.Column(db.Text)