from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from models.ModelFormation import Formation
from models.ModelOrganisme import Organisme
from database import db

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

@formation_bp.route("/edit", methods=["GET"])
def edit_formations():
    formations = Formation.query.all()
    organismes = Organisme.query.all()
    return render_template("edit_formations.html", formations=formations, organismes=organismes)

@formation_bp.route("/update", methods=["POST"])
def update_formations():
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
            formation.conditions_acces = request.form.get(f"conditions_acces_{id_}")
            formation.financement = request.form.get(f"financement_{id_}")
            formation.presentation_intervenants = request.form.get(f"presentation_intervenants_{id_}")
            formation.lien_inscription = request.form.get(f"lien_inscription_{id_}")
            formation.label = request.form.get(f"label_{id_}")
            formation.etat = request.form.get(f"etat_{id_}")  # Ajout de l'état
    
    db.session.commit()
    return redirect(url_for("formation.edit_formations"))

@formation_bp.route("/new", methods=["GET"])
def new_formation():
    organismes = Organisme.query.all()
    return render_template("new_formation.html", organismes=organismes)


@formation_bp.route("/create", methods=["POST"])
def create_formation():
    nom = request.form["nom"]
    type_ = request.form["type"]
    description = request.form["description"]
    duree = request.form["duree"]
    dates = request.form["dates"]
    lieu = request.form["lieu"]
    prix = request.form.get("prix")
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
    return redirect(url_for("formation.edit_formations"))


    
@formation_bp.route("/delete/<int:id>", methods=["POST"])
def delete_formation(id):
    formation = Formation.query.get_or_404(id)
    db.session.delete(formation)
    db.session.commit()
    return jsonify({"success": True})

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
    return redirect(url_for("dashboard"))  # Vous pouvez rediriger vers la page de confirmation

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


