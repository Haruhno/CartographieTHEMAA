from database import db

class Organisme(db.Model):
    """
    Modèle représentant un organisme dans la base de données.

    Attributs :
        id_organisme (int) : Identifiant unique de l'organisme (clé primaire).
        nom (str) : Nom de l'organisme (obligatoire).
        adresse (str) : Adresse de l'organisme (obligatoire).
        email (str) : Adresse email de l'organisme (obligatoire).
        telephone (str) : Numéro de téléphone de l'organisme (obligatoire).
        site_web (str) : Site web de l'organisme (optionnel).
        presentation (str) : Présentation ou description de l'organisme (obligatoire).
        num_adherent (str) : Numéro d'adhérent de l'organisme (optionnel).
        statut (str) : Statut de l'organisme (obligatoire).
        label (str) : Label ou distinction de l'organisme (optionnel).
    """
    __tablename__ = "Organisme"

    id_organisme = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    site_web = db.Column(db.String(100))
    presentation = db.Column(db.Text, nullable=False)
    num_adherent = db.Column(db.String(50))
    statut = db.Column(db.String(255), nullable=False)
    label = db.Column(db.String(255))
