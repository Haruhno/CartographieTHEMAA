from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.ModelOrganisme import Organisme
from models.ModelUtilisateur import Utilisateur
from models.ModelFormation import Formation
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

def get_labels_for_organisme():
    # Labels par défaut
    BASE_LABELS = [
        "Qualiopi",
        "RNCP (Répertoire National des Certifications Professionnelles)",
        "Erasmus+"
    ]
    # Récupérer tous les labels distincts de la BDD
    all_labels_raw = db.session.query(Formation.label).filter(Formation.label != None).all()
    label_set = set()
    for row in all_labels_raw:
        if row[0]:
            for l in str(row[0]).split(','):
                l = l.strip()
                if l:
                    label_set.add(l)
    label_set.update(BASE_LABELS)
    return sorted(label_set)

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

@organisme_bp.route("/edit")
@admin_required
def edit_organismes():
    """
    Affiche le formulaire d'édition des organismes.
    Récupère tous les organismes, statuts et labels distincts depuis la base de données.
    """
    organismes = Organisme.query.all()
    
    # Récupérer tous les statuts distincts depuis la base de données
    statuts = db.session.query(Organisme.statut).distinct().filter(Organisme.statut.isnot(None)).all()
    statuts = [statut[0] for statut in statuts] # Convertir en liste simple
    
    # Récupérer tous les labels distincts depuis la base de données
    labels = []
    labels_records = db.session.query(Organisme.label).distinct().filter(Organisme.label.isnot(None)).all()
    for label_record in labels_records:
        if label_record[0]:  # Si le label n'est pas None
            # Split les labels (car ils sont stockés avec des virgules)
            label_list = [l.strip() for l in label_record[0].split(',')]
            labels.extend(label_list)
    # Supprimer les doublons et trier
    labels = sorted(list(set(labels)))

    return render_template(
        "edit_organismes.html",
        organismes=organismes,
        statuts=statuts,
        labels=labels
    )

@organisme_bp.route("/update", methods=["POST"])
@admin_required
def update_organismes():
    """
    Met à jour les informations des organismes.
    Si un organisme est supprimé, il est retiré de la base de données.
    Si des informations sont modifiées, elles sont mises à jour dans la base de données.
    """
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
    """
    Affiche le formulaire de création d'un nouvel organisme.
    Récupère les statuts distincts depuis la base de données pour les afficher dans le formulaire.
    """
    statuts = db.session.query(Organisme.statut).distinct().all()
    return render_template("new_organisme.html", statuts=[s[0] for s in statuts if s[0]])

@organisme_bp.route("/create", methods=["POST"])
@admin_required
def create_organisme():
    """
    Crée un nouvel organisme.
    Récupère les informations du formulaire, crée un nouvel objet Organisme et l'ajoute à la base de données.
    Si l'URL du site web n'est pas complète, elle est normalisée en ajoutant "https://".
    """
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
    """
    Supprime un organisme de la base de données.
    Récupère l'ID de l'organisme à supprimer depuis l'URL, le cherche dans la base de données,
    et le supprime si trouvé. Affiche un message de succès après la suppression.
    """
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
    """
    Affiche le formulaire de création d'un nouvel organisme.
    Récupère les statuts distincts depuis la base de données pour les afficher dans le formulaire.
    """
    statuts = db.session.query(Organisme.statut).distinct().all()
    labels = get_labels_for_organisme()
    return render_template("formulaire_organisme.html", statuts=[s[0] for s in statuts if s[0]], labels=labels)

@organisme_bp.route("/create/user", methods=["POST"])
@login_required
def create_organisme_user():
    """
    Crée un nouvel organisme.
    Récupère les informations du formulaire, crée un nouvel objet Organisme et l'associe à l'utilisateur connecté.
    Si l'URL du site web n'est pas complète, elle est normalisée en ajoutant "https://".
    Si l'utilisateur a déjà un organisme associé, il est mis à jour avec les nouvelles informations.
    """
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
    """
    Affiche un aperçu des informations d'un organisme spécifique.
    Récupère les détails de l'organisme, les statuts distincts et les labels associés.
    """
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
        "RNCP (Répertoire National des Certifications Professionnelles)",
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
    """
    Met à jour les informations d'un organisme spécifique.
    Récupère l'ID de l'organisme depuis l'URL, cherche l'organisme dans la base de données,
    et met à jour ses informations en fonction des données reçues dans la requête.
    """
    organisme = Organisme.query.get_or_404(id)

    if request.is_json:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Aucune donnée reçue."}), 400

        organisme.nom = data.get('nom', organisme.nom)
        organisme.email = data.get('email', organisme.email)
        organisme.telephone = data.get('telephone', organisme.telephone)
        organisme.statut = data.get('statut', organisme.statut)
        organisme.label = data.get('label')  # Directement prendre la valeur formatée
        organisme.adresse = data.get('adresse', organisme.adresse)
        organisme.presentation = data.get('presentation', organisme.presentation)
        organisme.num_adherent = data.get('num_adherent', organisme.num_adherent)

        db.session.commit()
        return jsonify({
            "success": True, 
            "message": "Organisme mis à jour avec succès.",
            "label": organisme.label  # Renvoyer le label mis à jour
        })