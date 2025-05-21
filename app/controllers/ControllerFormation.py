from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.ModelFormation import Formation
from models.ModelOrganisme import Organisme
from database import db
from .ControllerUtilisateur import admin_required

formation_bp = Blueprint("formation", __name__, url_prefix="/formations")

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
        formation.lien_inscription = request.form.get("lien_inscription")
        formation.label = request.form.get("label")
        formation.id_organisme = request.form["id_organisme"]
        formation.etat = request.form.get("etat")

    db.session.commit()
    
    if request.is_json:
        return jsonify({
            "success": True,
            "message": "Formation mise à jour avec succès."
        })
    
    flash("Formation mise à jour avec succès.", "success")
    return redirect(url_for("formation.edit_formations"))

@formation_bp.route("/edit", methods=["GET"])
@admin_required
def edit_formations():
    formations = Formation.query.all()
    organismes = Organisme.query.all()
    return render_template("edit_formations.html", formations=formations, organismes=organismes)

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
    organismes = Organisme.query.all()
    return render_template("new_formation.html", organismes=organismes)


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
    return redirect(url_for("formation.edit_formations"))  # Modifié pour un redirect classique

@formation_bp.route("/formulaire", methods=["GET"])
def formulaire():
    organismes = Organisme.query.all()
    return render_template("formulaire.html", organismes=organismes)

@formation_bp.route("/submit", methods=["POST"])
def submit_formation():
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
    label = request.form.get("label")
    id_organisme = request.form["id_organisme"]

    formation_en_attente = Formation(
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
    db.session.add(formation_en_attente)
    db.session.commit()

    print("Formation ajoutée avec succès.")  # Debugging print
    return redirect(url_for("dashboard")) 

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
