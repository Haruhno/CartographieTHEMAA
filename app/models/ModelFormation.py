from database import db

class Formation(db.Model):
    """
    Représente une formation proposée par un organisme.
    
    Attributs :
        id_formation (int) : Identifiant unique de la formation.
        nom (str) : Nom de la formation.
        type (Enum) : Type de formation ('initiale' ou 'continue').
        description (str) : Description détaillée de la formation.
        duree (str) : Durée de la formation (ex : "2 semaines").
        duree_heures (float, optionnel) : Durée de la formation en heures.
        dates (str) : Dates de la formation.
        lieu (str) : Lieu où se déroule la formation.
        prix (Decimal, optionnel) : Prix de la formation.
        conditions_acces (str, optionnel) : Conditions d'accès à la formation.
        financement (str, optionnel) : Informations sur le financement possible.
        presentation_intervenants (str, optionnel) : Présentation des intervenants.
        lien_inscription (str, optionnel) : Lien pour s'inscrire à la formation.
        label (str, optionnel) : Label(s) associé(s) à la formation.
        certifications (str, optionnel) : Certifications délivrées à l'issue de la formation.
        id_organisme (int) : Identifiant de l'organisme proposant la formation.
        etat (Enum) : État de validation de la formation ('valide', 'en_attente').
        raison (str, optionnel) : Raison éventuelle en cas de refus ou d'attente de validation.
    """
    __tablename__ = "Formation"

    id_formation = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum('initiale', 'continue'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duree = db.Column(db.String(50), nullable=False)
    duree_heures = db.Column(db.Float, nullable=True)
    dates = db.Column(db.String(100), nullable=False)
    lieu = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Numeric(10, 2), nullable=True)
    conditions_acces = db.Column(db.Text)
    financement = db.Column(db.String(255))
    presentation_intervenants = db.Column(db.Text)
    lien_inscription = db.Column(db.String(200))
    label = db.Column(db.String(255))
    certifications = db.Column(db.String(255))
    id_organisme = db.Column(db.Integer, db.ForeignKey('Organisme.id_organisme'), nullable=False)
    etat = db.Column(db.Enum('valide', 'en_attente', name='etat_formation'), nullable=False, default='en_attente')
    raison = db.Column(db.Text)