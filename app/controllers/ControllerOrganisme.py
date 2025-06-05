from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.ModelOrganisme import Organisme
from models.ModelUtilisateur import Utilisateur
from database import db
from flask_login import current_user, login_required
from .ControllerUtilisateur import admin_required

organisme_bp = Blueprint("organisme", __name__, url_prefix="/organismes")

def normalize_website_url(site_web):
    """
    Normalise l'URL d'un site web en ajoutant https:// si nécessaire.
    
    Args:
        site_web (str): L'URL du site web
        
    Returns:
        str: L'URL normalisée ou None si l'entrée est vide
    """
    if site_web and not site_web.startswith("http://") and not site_web.startswith("https://"):
        return "https://" + site_web
    return site_web

@organisme_bp.route("/all", methods=["GET"])
def get_all_organismes():
    organismes = Organisme.query.all()
    resultats = []

    for o in organismes:
        resultats.append({
            "id": o.id_organisme,
            "nom": o.nom,
            "adresse": o.adresse,
            "email": o.email,
            "telephone": o.telephone,
            "site_web": o.site_web,
            "presentation": o.presentation,
            "num_adherent": o.num_adherent,
            "statut": o.statut,
            "label": o.label
        })

    return jsonify(resultats)

@organisme_bp.route("/edit", methods=["GET"])
@admin_required
def edit_organismes():
    organismes = Organisme.query.all()
    
    # Récupération des labels
    labels_raw = db.session.query(Organisme.label).distinct().all()
    labels_set = set()
    for label_row in labels_raw:
        if label_row[0]:
            # Diviser les labels par virgule
            for label in label_row[0].split(','):
                label = label.strip()
                if label and label.lower() != 'none':
                    labels_set.add(label)
    
    return render_template("edit_organismes.html", 
                         organismes=organismes,
                         labels=sorted(list(labels_set)))

@organisme_bp.route("/update", methods=["POST"])
@admin_required
def update_organismes():
    if "delete" in request.form:
        id_ = request.form["delete"]
        organisme = Organisme.query.get_or_404(int(id_))
        db.session.delete(organisme)
        db.session.commit()
        flash("Organisme supprimé avec succès.", "success")
        return redirect(url_for("organisme.edit_organismes"))

    for key, value in request.form.items():
        if key.startswith("nom_"):
            id_ = key.split("_")[1]
            organisme = Organisme.query.get(int(id_))
            organisme.nom = value
            organisme.email = request.form.get(f"email_{id_}")
            organisme.telephone = request.form.get(f"telephone_{id_}")
            organisme.site_web = normalize_website_url(request.form.get(f"site_web_{id_}"))
            organisme.statut = request.form.get(f"statut_{id_}")
            organisme.label = request.form.get(f"label_{id_}")
            organisme.adresse = request.form.get(f"adresse_{id_}", organisme.adresse)
            organisme.presentation = request.form.get(f"presentation_{id_}", organisme.presentation)
            organisme.num_adherent = request.form.get(f"num_adherent_{id_}", organisme.num_adherent)

    db.session.commit()
    flash("Tous les organismes ont été mis à jour avec succès.", "success")
    return redirect(url_for("organisme.edit_organismes"))

@organisme_bp.route("/new", methods=["GET"])
@admin_required
def new_organisme():
    statuts = db.session.query(Organisme.statut).distinct().all()
    return render_template("new_organisme.html", statuts=[s[0] for s in statuts if s[0]])

@organisme_bp.route("/create", methods=["POST"])
@admin_required
def create_organisme():
    nom = request.form["nom"]
    adresse = request.form["adresse"]
    email = request.form["email"]
    telephone = request.form["telephone"]
    site_web = normalize_website_url(request.form.get("site_web"))
    presentation = request.form["presentation"]
    num_adherent = request.form.get("num_adherent")
    statut = request.form["statut"]
    label = request.form.get("label")

    nouvel_organisme = Organisme(
        nom=nom,
        adresse=adresse,
        email=email,
        telephone=telephone,
        site_web=site_web,
        presentation=presentation,
        num_adherent=num_adherent,
        statut=statut,
        label=label
    )
    db.session.add(nouvel_organisme)
    db.session.commit()
    flash("Organisme créé avec succès.", "success")
    return redirect(url_for("organisme.edit_organismes"))

@organisme_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_organisme(id):
    organisme = Organisme.query.get_or_404(id)
    db.session.delete(organisme)
    db.session.commit()
    flash("Organisme supprimé avec succès.", "success")
    return redirect(url_for("organisme.edit_organismes"))

@organisme_bp.route("/choose", methods=["GET", "POST"])
@login_required
def choose_organisme():
    if request.method == "POST":
        # Vérifier si un ID d'organisme a été fourni
        organisme_id = request.form.get("id_organisme")
        if organisme_id:
            current_user.id_organisme = organisme_id
            db.session.commit()
            flash("Organisme associé avec succès!", "success")
            return redirect(url_for("utilisateur.profil"))
    
    # GET: Afficher la liste des organismes
    organismes = Organisme.query.all()
    return render_template("choose_organisme.html", organismes=organismes)

@organisme_bp.route("/new/user", methods=["GET"])
@login_required
def new_organisme_user():
    statuts = db.session.query(Organisme.statut).distinct().all()
    return render_template("formulaire_organisme.html", statuts=[s[0] for s in statuts if s[0]])

@organisme_bp.route("/create/user", methods=["POST"])
@login_required
def create_organisme_user():
    nom = request.form["nom"]
    adresse = request.form["adresse"]
    email = request.form["email"]
    telephone = request.form["telephone"]
    site_web = normalize_website_url(request.form.get("site_web"))
    presentation = request.form["presentation"]
    num_adherent = request.form.get("num_adherent")
    statut = request.form["statut"]
    label = request.form.get("label")

    nouvel_organisme = Organisme(
        nom=nom,
        adresse=adresse,
        email=email,
        telephone=telephone,
        site_web=site_web,
        presentation=presentation,
        num_adherent=num_adherent,
        statut=statut,
        label=label
    )
    
    db.session.add(nouvel_organisme)
    db.session.flush()  # Pour obtenir l'ID
    
    # Associer l'organisme à l'utilisateur
    current_user.id_organisme = nouvel_organisme.id_organisme
    db.session.commit()
    
    flash("Organisme créé et associé avec succès!", "success")
    return redirect(url_for("utilisateur.profil"))

@organisme_bp.route("/preview/<int:id>", methods=["GET"])
@admin_required
def preview_organisme(id):
    organisme = Organisme.query.get_or_404(id)
    statuts = db.session.query(Organisme.statut).distinct().all()
    formations = organisme.formations if hasattr(organisme, 'formations') else []
    
    # Récupérer tous les labels distincts
    labels_raw = db.session.query(Organisme.label).distinct().all()
    labels_set = set()
    for label_row in labels_raw:
        if label_row[0]:
            # Diviser les labels par virgule et les ajouter au set
            for label in label_row[0].split(','):
                label = label.strip()
                if label and label.lower() != 'none':
                    labels_set.add(label)
    
    # Labels de base à toujours proposer
    BASE_LABELS = [
        "Qualiopi",
        "RNCP",
        "Erasmus+"
    ]
    labels_set.update(BASE_LABELS)
    
    return render_template("preview_organisme.html", 
                         organisme=organisme,
                         statuts=[s[0] for s in statuts if s[0]],
                         formations=formations,
                         labels=sorted(list(labels_set)))

@organisme_bp.route("/update/<int:id>", methods=["POST"])
@admin_required
def update_organisme_by_id(id):
    organisme = Organisme.query.get_or_404(id)

    # Si c'est une requête JSON (depuis JavaScript)
    if request.is_json:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Aucune donnée reçue."}), 400

        organisme.nom = data.get('nom', organisme.nom)
        organisme.email = data.get('email', organisme.email)
        organisme.telephone = data.get('telephone', organisme.telephone)
        organisme.statut = data.get('statut', organisme.statut)
        
        # Gestion des labels
        labels = data.get('labels', [])
        organisme.label = ','.join(labels) if labels else None

        db.session.commit()
        return jsonify({"success": True, "message": "Organisme mis à jour avec succès."})

    # Sinon, c'est un POST HTML classique (formulaire dans `preview`)
    else:
        organisme.nom = request.form.get('nom')
        organisme.statut = request.form.get('statut')
        organisme.email = request.form.get('email')
        organisme.telephone = request.form.get('telephone')
        organisme.adresse = request.form.get('adresse')
        
        site_web = normalize_website_url(request.form.get("site_web"))
        organisme.site_web = site_web

        organisme.presentation = request.form.get('presentation')
        organisme.num_adherent = request.form.get('num_adherent')
        
        # Gestion des labels multiples
        labels = request.form.getlist('labels[]')
        organisme.label = ','.join(labels) if labels else None

        db.session.commit()
        flash("Organisme mis à jour avec succès!", "success")
        return redirect(url_for("organisme.edit_organismes", id=organisme.id_organisme))