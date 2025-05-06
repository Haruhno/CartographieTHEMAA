from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from models.ModelOrganisme import Organisme
from database import db

organisme_bp = Blueprint("organisme", __name__, url_prefix="/organismes")

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
            "telephone": o.telephone
        })

    return jsonify(resultats)

@organisme_bp.route("/edit", methods=["GET"])
def edit_organismes():
    organismes = Organisme.query.all()
    return render_template("edit_organismes.html", organismes=organismes)

@organisme_bp.route("/update", methods=["POST"])
def update_organismes():
    for key, value in request.form.items():
        if key.startswith("nom_"):
            id_ = key.split("_")[1]
            organisme = Organisme.query.get(int(id_))
            organisme.nom = value
            organisme.adresse = request.form.get(f"adresse_{id_}")
            organisme.email = request.form.get(f"email_{id_}")
            organisme.telephone = request.form.get(f"telephone_{id_}")
    
    db.session.commit()
    return redirect(url_for("organisme.edit_organismes"))

@organisme_bp.route("/new", methods=["GET"])
def new_organisme():
    return render_template("new_organisme.html")


@organisme_bp.route("/create", methods=["POST"])
def create_organisme():
    nom = request.form["nom"]
    adresse = request.form["adresse"]
    email = request.form["email"]
    telephone = request.form["telephone"]
    site_web = request.form.get("site_web")
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
    return redirect(url_for("organisme.edit_organismes"))

@organisme_bp.route("/delete/<int:id>", methods=["POST"])
def delete_organisme(id):
    organisme = Organisme.query.get_or_404(id)
    db.session.delete(organisme)
    db.session.commit()
    return jsonify({"success": True})
