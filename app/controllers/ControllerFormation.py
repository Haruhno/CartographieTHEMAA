from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.ModelFormation import Formation
from models.ModelOrganisme import Organisme
from database import db
from .ControllerUtilisateur import admin_required
from functools import wraps
from flask_login import current_user
from flask_login import login_required, current_user


formation_bp = Blueprint("formation", __name__, url_prefix="/formations")

def get_formulaire_context():
    organismes = Organisme.query.all()

    # ---------- Financements ----------
    financement_set = set()
    all_financements_raw = db.session.query(Formation.financement).filter(Formation.financement != None).all()
    for row in all_financements_raw:
        if row[0]:
            financement_set.update([f.strip() for f in str(row[0]).split(',')])

    # On affiche toujours toutes les options même si elles ne sont pas encore utilisées
    FINANCEMENT_OPTIONS = [
        "OPCO (Opérateur De Compétences)",
        "CPF (Compte Personnel de Formation)",
        "France Travail",
        "Fondations",
        "Bourses",
        "Employeur·euses",
        "Régions",
        "Autofinancement"
    ]
    financements = FINANCEMENT_OPTIONS

    # ---------- Labels ----------
    all_labels_raw = db.session.query(Formation.label).filter(Formation.label != None).all()
    label_set = set()
    for row in all_labels_raw:
        if row[0]:
            label_set.update([l.strip() for l in str(row[0]).split(',')])
    labels = sorted(label_set) if label_set else [
        "Qualiopi",
        "RNCP (Répertoire National des Certifications Professionnelles)",
        "Erasmus+"
    ]

    # ---------- Certifications ----------
    certifications = [
        "DE (Diplôme d'État)",
        "DNSP (Diplôme National Supérieur Professionnel)",
        "RS (Répertoire Spécifique)",
        "Formation Certifiante",
        "Formation Non Certifiante"
    ]
    if hasattr(Formation, "certifications"):
        all_certs_raw = db.session.query(Formation.certifications).filter(Formation.certifications != None).all()
        cert_set = set()
        for row in all_certs_raw:
            if row[0]:
                cert_set.update([c.strip() for c in str(row[0]).split(',')])
        certifications = sorted(cert_set) if cert_set else certifications

    return {
        "organismes": organismes,
        "financements": financements,
        "labels": labels,
        "certifications": certifications
    }

def organisme_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('utilisateur.connexion'))
        if not current_user.id_organisme:
            return redirect(url_for('dashboard'))  # Rediriger si l'utilisateur n'est pas un organisme
        return f(*args, **kwargs)
    return decorated_function


@formation_bp.route("/all", methods=["GET"])
def get_all_formations():
    formations = Formation.query.all()
    resultats = []

    for f in formations:
        resultats.append({
            "id": f.id_formation,
            "nom": f.nom,
            "type": f.type,
            "description": f.description,
            "duree": f.duree,
            "dates": f.dates,
            "lieu": f.lieu,
            "prix": f.prix,
            "conditions_acces": f.conditions_acces,
            "financement": f.financement,
            "presentation_intervenants": f.presentation_intervenants,
            "lien_inscription": f.lien_inscription,
            "label": f.label,
            "id_organisme": f.id_organisme
        })

    return jsonify(resultats)

@formation_bp.route('/edit/<int:id>', methods=["GET", "POST"],  endpoint="preview_formation")
@admin_required
def handle_formation(id):
    if request.method == "POST":
        # Code de update_formation_by_id
        formation = Formation.query.get_or_404(id)
        formation.nom = request.form.get("nom")
        formation.type = request.form.get("type")
        formation.description = request.form.get("description")
        formation.duree = request.form.get("duree")
        formation.dates = request.form.get("dates")
        formation.lieu = request.form.get("lieu")
        formation.prix = request.form.get("prix")
        formation.prix = float(formation.prix) if formation.prix else None
        formation.conditions_acces = request.form.get("conditions_acces")
        formation.financement = request.form.get("financement")
        formation.presentation_intervenants = request.form.get("presentation_intervenants")
        formation.lien_inscription = request.form.get("lien_inscription")
        formation.label = request.form.get("label")
        formation.id_organisme = request.form.get("id_organisme")
        formation.etat = request.form.get("etat")
        db.session.commit()
        return redirect(url_for("formation.edit_formations"))
    else:
        # Code de preview_formation
        formation = Formation.query.get(id)
        if not formation:
            flash("Formation non trouvée", "error")
            return redirect(url_for("formation.edit_formations"))
        organismes = Organisme.query.all()
        return render_template('preview_formation.html', formation=formation, organismes=organismes)

@formation_bp.route("/update/<int:id>", methods=["POST"])
@admin_required
def update_formation_by_id(id):
    formation = Formation.query.get_or_404(id)
    
    if request.is_json:
        data = request.get_json()
        
        formation.nom = data.get("nom")
        formation.type = data.get("type")
        formation.description = data.get("description")
        formation.duree = data.get("duree")
        formation.dates = data.get("dates")
        formation.lieu = data.get("lieu")
        prix = data.get("prix")
        formation.prix = float(prix) if prix else None
        formation.conditions_acces = data.get("conditions_acces")
        formation.financement = data.get("financement")
        formation.presentation_intervenants = data.get("presentation_intervenants")
        formation.lien_inscription = data.get("lien_inscription")
        if formation.lien_inscription and not formation.lien_inscription.startswith("http://") and not formation.lien_inscription.startswith("https://"):
            formation.lien_inscription = "https://" + formation.lien_inscription
        formation.label = data.get("label")
        formation.id_organisme = data.get("id_organisme")
        formation.etat = data.get("etat")
    else:
        # Garder l'ancienne version pour la compatibilité
        formation.nom = request.form["nom"]
        formation.type = request.form["type"]
        formation.description = request.form["description"]
        formation.duree = request.form["duree"]
        formation.dates = request.form["dates"]
        formation.lieu = request.form["lieu"]
        prix = request.form.get("prix")
        formation.prix = float(prix) if prix else None
        formation.conditions_acces = request.form.get("conditions_acces")
        formation.financement = request.form.get("financement")
        formation.presentation_intervenants = request.form.get("presentation_intervenants")
        
        lien_inscription = request.form.get("lien_inscription")
        if lien_inscription and not lien_inscription.startswith("http://") and not lien_inscription.startswith("https://"):
            lien_inscription = "https://" + lien_inscription
        formation.lien_inscription = lien_inscription

        formation.label = request.form.get("label")
        formation.id_organisme = request.form["id_organisme"]
        formation.etat = request.form.get("etat")

    db.session.commit()
    flash("Formation mise à jour avec succès.", "success")
    return redirect(url_for("formation.edit_formations"))

@formation_bp.route("/edit", methods=["GET"])
@admin_required
def edit_formations():
    formations = Formation.query.all()
    organismes = Organisme.query.all()

    # Récupérer les labels distincts (non vides, non null)
    labels = db.session.query(Formation.label).distinct().all()
    labels = [l[0] for l in labels if l[0] and l[0].strip().lower() != 'none']

    return render_template("edit_formations.html",
                           formations=formations,
                           organismes=organismes,
                           labels=labels)

@formation_bp.route("/update", methods=["POST"])
@admin_required
def update_formations():
    # Gérer les boutons delete et save
    if "delete" in request.form:
        id_ = request.form["delete"]
        formation = Formation.query.get_or_404(int(id_))
        db.session.delete(formation)
        db.session.commit()
        flash("Formation supprimée avec succès.", "success")
        return redirect(url_for("formation.edit_formations"))

    for key, value in request.form.items():
        if key.startswith("nom_"):
            id_ = key.split("_")[1]
            formation = Formation.query.get(int(id_))
            formation.nom = value
            formation.type = request.form.get(f"type_{id_}")
            formation.description = request.form.get(f"description_{id_}")
            formation.duree = request.form.get(f"duree_{id_}")
            formation.dates = request.form.get(f"dates_{id_}")
            formation.lieu = request.form.get(f"lieu_{id_}")
            formation.prix = request.form.get(f"prix_{id_}")
            formation.prix = float(formation.prix) if  formation.prix else None
            formation.conditions_acces = request.form.get(f"conditions_acces_{id_}")
            formation.financement = request.form.get(f"financement_{id_}")
            formation.presentation_intervenants = request.form.get(f"presentation_intervenants_{id_}")
            formation.lien_inscription = request.form.get(f"lien_inscription_{id_}")
            formation.label = request.form.get(f"label_{id_}")
            formation.etat = request.form.get(f"etat_{id_}")
    
    db.session.commit()
    flash("Toutes les formations ont été mises à jour avec succès.", "success")
    return redirect(url_for("formation.edit_formations"))

@formation_bp.route("/new", methods=["GET"])
@admin_required
def new_formation():
    context = get_formulaire_context()
    return render_template("formulaire.html", **context)


@formation_bp.route("/create", methods=["POST"])
@admin_required
def create_formation():
    nom = request.form["nom"]
    type_ = request.form["type"]
    description = request.form["description"]
    duree = request.form["duree"]
    dates = request.form["dates"]
    lieu = request.form["lieu"]
    prix = request.form.get("prix")
    prix = float(prix) if prix else None
    conditions_acces = request.form.get("conditions_acces")
    financement = request.form.get("financement")
    presentation_intervenants = request.form.get("presentation_intervenants")
    lien_inscription = request.form.get("lien_inscription")
    if lien_inscription and not lien_inscription.startswith("http://") and not lien_inscription.startswith("https://"):
        lien_inscription = "https://" + lien_inscription
    label = request.form.get("label")
    id_organisme = request.form["id_organisme"]

    nouvelle_formation = Formation(
        nom=nom,
        type=type_,
        description=description,
        duree=duree,
        dates=dates,
        lieu=lieu,
        prix=prix,
        conditions_acces=conditions_acces,
        financement=financement,
        presentation_intervenants=presentation_intervenants,
        lien_inscription=lien_inscription,
        label=label,
        id_organisme=id_organisme
    )
    db.session.add(nouvelle_formation)
    db.session.commit()
    flash("Formation créée avec succès.", "success")
    return redirect(url_for("formation.edit_formations"))


    
@formation_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_formation(id):
    formation = Formation.query.get_or_404(id)
    db.session.delete(formation)
    db.session.commit()
    flash("Formation supprimée avec succès.", "success")
    return redirect(url_for("formation.edit_formations"))


@formation_bp.route("/formulaire", methods=["GET"])
@organisme_required
def formulaire():
    context = get_formulaire_context()
    return render_template("formulaire.html", **context)

@formation_bp.route("/submit", methods=["POST"])
@login_required
def submit_formation():
    try:
        # Récupérer les données du formulaire
        nom = request.form.get('nom')
        type_formation = request.form.get('type')
        id_organisme = request.form.get('id_organisme')
        description = request.form.get('description')
        # Correction: reconstituer la durée complète
        duree_heures = request.form.get('duree_heures')
        duree_valeur = request.form.get('duree_valeur')
        duree_unite = request.form.get('duree_unite')
        # Compose la durée sous forme "75.0 heures / 10 jours"
        duree = None
        if duree_heures and duree_valeur and duree_unite:
            duree = f"{duree_heures} heures / {duree_valeur} {duree_unite}"
        elif duree_heures:
            duree = f"{duree_heures} heures"
        elif duree_valeur and duree_unite:
            duree = f"{duree_valeur} {duree_unite}"

        dates = request.form.get('dates')
        lieu = request.form.get('adresse')  # Correction: champ "adresse" dans le formulaire HTML
        prix = request.form.get('prix')
        prix = float(prix) if prix else None
        conditions_acces = request.form.get('conditions_acces')
        financement = request.form.get('financement')
        presentation_intervenants = request.form.get('presentation_intervenants')
        lien_inscription = request.form.get('lien_inscription')
        if lien_inscription and not lien_inscription.startswith("http://") and not lien_inscription.startswith("https://"):
            lien_inscription = "https://" + lien_inscription
        label = request.form.get('label')
        # num_adherent n'est PAS un champ du modèle Formation, donc on ne le passe pas au constructeur

        # Vérification des champs obligatoires pour éviter les erreurs d'intégrité
        if not nom or not type_formation or not id_organisme or not description or not duree or not dates or not lieu:
            flash("Merci de remplir tous les champs obligatoires du formulaire.", "danger")
            return redirect(url_for('formation.formulaire'))

        # Créer la nouvelle formation avec l'état "en_attente"
        nouvelle_formation = Formation(
            nom=nom,
            type=type_formation,
            id_organisme=id_organisme,
            description=description,
            duree=duree,
            dates=dates,
            lieu=lieu,
            prix=prix,
            conditions_acces=conditions_acces,
            financement=financement,
            presentation_intervenants=presentation_intervenants,
            lien_inscription=lien_inscription,
            label=label,
            etat='en_attente'
        )

        db.session.add(nouvelle_formation)
        db.session.commit()

        flash('Votre formation a été soumise avec succès et est en attente de validation.', 'success')

        # Redirection en fonction du rôle
        if hasattr(current_user, "is_admin") and current_user.is_admin:
            return redirect(url_for('formation.edit_formations', filtre='en_attente'))
        else:
            return redirect(url_for('dashboard'))

    except Exception as e:
        db.session.rollback()
        flash(f"Une erreur s'est produite lors de la soumission du formulaire: {str(e)}", 'danger')
        return redirect(url_for('formation.formulaire'))

@formation_bp.route("/valides", methods=["GET"])
def get_formations_valides():
    formations = Formation.query.filter_by(etat="valide").all()
    resultats = []

    for f in formations:
        resultats.append({
            "id": f.id_formation,
            "nom": f.nom,
            "type": f.type,
            "description": f.description,
            "duree": f.duree,
            "dates": f.dates,
            "lieu": f.lieu,
            "prix": f.prix,
            "conditions_acces": f.conditions_acces,
            "financement": f.financement,
            "presentation_intervenants": f.presentation_intervenants,
            "lien_inscription": f.lien_inscription,
            "label": f.label,
            "id_organisme": f.id_organisme
        })

    return jsonify(resultats)

@formation_bp.route("/informations/<int:organisme_id>", methods=["GET"])
def formation_informations(organisme_id):
    organisme = Organisme.query.get_or_404(organisme_id)
    formations = Formation.query.filter_by(id_organisme=organisme_id, etat="valide").all()
    
    return render_template("formation_informations.html", 
                         organisme=organisme, 
                         formations=formations)


@formation_bp.route('/modify/<int:id>', methods=['GET'])
def modify_formation(id):
    formation = Formation.query.get_or_404(id)
    return render_template('modify_formation.html', formation=formation)

@formation_bp.route('/modify_with_reason', methods=['POST'])
def modify_with_reason():
    formation = Formation.query.get_or_404(request.form['id'])
    
    # Mettre à jour les champs de la formation
    formation.nom = request.form['nom']
    formation.type = request.form['type']
    formation.description = request.form['description']
    formation.duree = request.form['duree']
    formation.dates = request.form['dates']
    formation.lieu = request.form['lieu']
    prix = request.form.get('prix')
    formation.prix = float(prix) if prix else None
    formation.conditions_acces = request.form['conditions_acces']
    formation.financement = request.form['financement']
    formation.presentation_intervenants = request.form['presentation_intervenants']
    formation.lien_inscription = request.form['lien_inscription']
    
    # Mettre en attente avec la raison
    formation.etat = 'en_attente'
    formation.raison = f"Modifier:{request.form['reason']}"
    
    db.session.commit()
    
    flash("Modification soumise avec succès et en attente de validation.", "success")
    return redirect(url_for("dashboard"))

@formation_bp.route('/delete_with_reason', methods=["POST"])
def delete_with_reason():
    formation = Formation.query.get_or_404(request.form['id'])
    
    # Mettre en attente avec la raison au lieu de supprimer
    formation.etat = 'en_attente'
    formation.raison = f"Supprimer:{request.form['reason']}"
    
    db.session.commit()
    
    flash("Demande de suppression soumise avec succès et en attente de validation.", "success")
    return redirect(url_for("dashboard"))

@formation_bp.route('/delete_reason/<int:id>', methods=['POST'])
@admin_required
def delete_reason(id):
    formation = Formation.query.get_or_404(id)
    formation.raison = None  # Effacer la raison
    db.session.commit()
    
    flash("Raison supprimée avec succès.", "success")
    return redirect(url_for('formation.edit_formations'))

