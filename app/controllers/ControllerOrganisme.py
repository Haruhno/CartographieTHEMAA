from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.ModelOrganisme import Organisme
from models.ModelUtilisateur import Utilisateur
from database import db
from flask_login import current_user, login_required

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
    statuts = db.session.query(Organisme.statut).distinct().all()
    labels = db.session.query(Organisme.label).distinct().all()
    return render_template("edit_organismes.html", organismes=organismes,
                           statuts=[s[0] for s in statuts if s[0]],
                           labels=[l[0] for l in labels if l[0]])


@organisme_bp.route("/update", methods=["POST"])
def update_organismes():
    for key, value in request.form.items():
        if key.startswith("nom_"):
            id_ = key.split("_")[1]
            organisme = Organisme.query.get(int(id_))
            organisme.nom = value
            organisme.email = request.form.get(f"email_{id_}")
            organisme.telephone = request.form.get(f"telephone_{id_}")
            site_web = request.form.get(f"site_web_{id_}")
            if site_web and not site_web.startswith("http://") and not site_web.startswith("https://"):
                site_web = "https://" + site_web
            organisme.site_web = site_web
            organisme.statut = request.form.get(f"statut_{id_}")
            organisme.label = request.form.get(f"label_{id_}")
            organisme.adresse = request.form.get(f"adresse_{id_}") or organisme.adresse

    db.session.commit()
    flash("Tous les organismes ont été mis à jour avec succès.", "success")
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
    if site_web and not site_web.startswith("http://") and not site_web.startswith("https://"): 
        site_web = "https://" + site_web
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
    flash("Organisme supprimé avec succès.", "success")
    return redirect(url_for("organisme.edit_organismes"))

@organisme_bp.route("/choose", methods=["GET", "POST"])
@login_required
def choose_organisme():
    if request.method == "POST":
        # Si l'utilisateur a choisi un organisme existant
        if "id_organisme" in request.form:
            organisme_id = request.form["id_organisme"]
            current_user.id_organisme = organisme_id
            db.session.commit()
            flash("Organisme associé avec succès!", "success")
            return redirect(url_for("utilisateur.profil"))
        
        # Si l'utilisateur veut créer un nouvel organisme
        elif "create_new" in request.form:
            return redirect(url_for("organisme.new_organisme_user"))
    
    # GET: Afficher la liste des organismes
    organismes = Organisme.query.all()
    return render_template("choose_organisme.html", organismes=organismes)

@organisme_bp.route("/new/user", methods=["GET"])
@login_required
def new_organisme_user():
    return render_template("formulaire_organisme.html")

@organisme_bp.route("/create/user", methods=["POST"])
@login_required
def create_organisme_user():
    nom = request.form["nom"]
    adresse = request.form["adresse"]
    email = request.form["email"]
    telephone = request.form["telephone"]
    site_web = request.form.get("site_web")
    if site_web and not site_web.startswith("http://") and not site_web.startswith("https://"):
        site_web = "https://" + site_web
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
def preview_organisme(id):
    organisme = Organisme.query.get_or_404(id)
    statuts = db.session.query(Organisme.statut).distinct().all()
    formations = organisme.formations if hasattr(organisme, 'formations') else []
    return render_template("preview_organisme.html", 
                            organisme=organisme,
                            statuts=[s[0] for s in statuts if s[0]],
                            formations=formations)

@organisme_bp.route("/update/<int:id>", methods=["POST"])
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
        organisme.label = data.get('label', organisme.label)

        db.session.commit()
        return jsonify({"success": True, "message": "Organisme mis à jour avec succès."})

    # Sinon, c'est un POST HTML classique (formulaire dans `preview`)
    else:
        organisme.nom = request.form.get('nom')
        organisme.statut = request.form.get('statut')
        organisme.email = request.form.get('email')
        organisme.telephone = request.form.get('telephone')
        organisme.adresse = request.form.get('adresse')
        
        site_web = request.form.get("site_web")
        if site_web and not site_web.startswith("http://") and not site_web.startswith("https://"):
            site_web = "https://" + site_web
        organisme.site_web = site_web

        organisme.presentation = request.form.get('presentation')
        organisme.num_adherent = request.form.get('num_adherent')
        organisme.label = request.form.get('label')

        db.session.commit()
        flash("Organisme mis à jour avec succès!", "success")
        return redirect(url_for("organisme.edit_organismes", id=organisme.id_organisme))
