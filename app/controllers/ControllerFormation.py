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
    # Labels de base à toujours proposer
    BASE_LABELS = [
        "Qualiopi",
        "RNCP (Répertoire National des Certifications Professionnelles)",
        "Erasmus+"
    ]
    all_labels_raw = db.session.query(Formation.label).filter(Formation.label != None).all()
    label_set = set()
    for row in all_labels_raw:
        if row[0]:
            for l in str(row[0]).split(','):
                l = l.strip()
                # Mapper la valeur BDD "RNCP" vers le label complet pour l'affichage
                if l.upper() == "RNCP":
                    label_set.add("RNCP (Répertoire National des Certifications Professionnelles)")
                elif l:
                    label_set.add(l)
    label_set.update(BASE_LABELS)
    labels = sorted(label_set)

    # ---------- Certifications ----------
    # Définir le mapping des certifications
    CERTIFICATION_MAPPING = {
        "DE": "DE (Diplôme d'État)",
        "DNSP": "DNSP (Diplôme National Supérieur Professionnel)",
        "RS": "RS (Répertoire Spécifique)",
        "Formation Certifiante": "Formation Certifiante",
        "Formation Non Certifiante": "Formation Non Certifiante"
    }
    
    # Pour l'affichage dans le formulaire
    certifications = [
        "DE (Diplôme d'État)",
        "DNSP (Diplôme National Supérieur Professionnel)",
        "RS (Répertoire Spécifique)",
        "Formation Certifiante",
        "Formation Non Certifiante"
    ]

    return {
        "organismes": organismes,
        "financements": financements,
        "labels": labels,
        "certifications": certifications,
        "certification_mapping": CERTIFICATION_MAPPING
    }

def organisme_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('utilisateur.connexion'))
        # Permettre à l'admin de passer
        if current_user.is_admin:
            return f(*args, **kwargs)
        # Vérifier si l'utilisateur est lié à un organisme
        if not current_user.id_organisme:
            return redirect(url_for('dashboard'))
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
            "duree_heures": f.duree_heures,
            "dates": f.dates,
            "lieu": f.lieu,
            "prix": f.prix,
            "conditions_acces": f.conditions_acces,
            "financement": f.financement,
            "presentation_intervenants": f.presentation_intervenants,
            "lien_inscription": f.lien_inscription,
            "label": f.label,
            "certifications": f.certifications,
            "id_organisme": f.id_organisme
        })

    return jsonify(resultats)

@formation_bp.route('/edit/<int:id>', methods=["GET", "POST"], endpoint="preview_formation")
@admin_required
def handle_formation(id):
    if request.method == "POST":
        # Code de update_formation_by_id
        formation = Formation.query.get_or_404(id)
        formation.nom = request.form.get("nom")
        formation.type = request.form.get("type")
        formation.description = request.form.get("description")
        formation.duree = request.form.get("duree")
        duree_heures = request.form.get("duree_heures")
        formation.duree_heures = float(duree_heures) if duree_heures else None
        formation.dates = request.form.get("dates")
        formation.lieu = request.form.get("lieu")
        formation.prix = request.form.get("prix")
        formation.prix = float(formation.prix) if formation.prix else None
        formation.conditions_acces = request.form.get("conditions_acces")
        formation.financement = request.form.get("financement")
        formation.presentation_intervenants = request.form.get("presentation_intervenants")
        formation.lien_inscription = request.form.get("lien_inscription")
        formation.label = request.form.get("label")
        formation.certifications = request.form.get("certifications")
        formation.id_organisme = request.form.get("id_organisme")
        formation.etat = request.form.get("etat")
        db.session.commit()
        return redirect(url_for("formation.edit_formations"))
    else:
        formation = Formation.query.get_or_404(id)
        if not formation:
            flash("Formation non trouvée", "error")
            return redirect(url_for("formation.edit_formations"))
        
        # Récupérer tous les labels existants
        labels_from_db = db.session.query(Formation.label).distinct().filter(Formation.label != None).all()
        labels_set = set()
        
        # Labels par défaut
        default_labels = ["Qualiopi", "RNCP", "Erasmus+"]
        labels_set.update(default_labels)
        
        # Ajouter les labels de la base de données
        for label_row in labels_from_db:
            if label_row[0]:
                labels_set.update([l.strip() for l in label_row[0].split(',') if l.strip()])
        
        organismes = Organisme.query.all()
        return render_template('preview_formation.html', 
                            formation=formation, 
                            organismes=organismes,
                            labels=sorted(list(labels_set)))  # Liste triée de tous les labels

@formation_bp.route("/update/<int:id>", methods=["POST"])
@admin_required
def update_formation_by_id(id):
    try:
        formation = Formation.query.get_or_404(id)
        
        if request.is_json:
            data = request.get_json()
            
            formation.nom = data.get("nom")
            formation.type = data.get("type")
            formation.description = data.get("description")
            # Utiliser directement la durée pour la vue liste
            formation.duree = data.get("duree") or formation.duree  # Garde l'ancienne valeur si pas de nouvelle
            duree_heures = data.get("duree_heures")
            formation.duree_heures = float(duree_heures) if duree_heures else None
            formation.dates = data.get("dates")
            formation.lieu = data.get("lieu")
            prix = data.get("prix")
            formation.prix = float(prix) if prix else None
            formation.conditions_acces = data.get("conditions_acces")
            formation.financement = data.get("financement")
            formation.presentation_intervenants = data.get("presentation_intervenants")
            formation.lien_inscription = data.get("lien_inscription")
            
            # Gestion des labels multiples
            labels = data.get("labels", [])
            formation.label = ','.join(labels) if labels else None
            
            # Utiliser la valeur courte pour la certification
            certification_value = request.form.get('certification_value')
            if certification_value:
                formation.certifications = certification_value
            
            formation.id_organisme = data.get("id_organisme")
            formation.etat = data.get("etat")
            
            db.session.commit()
            flash("Formation mise à jour avec succès!", "success")
            return redirect(url_for("formation.edit_formations"))
            
        else:
            # Pour les soumissions de formulaire (preview_formation.html)
            duree_valeur = request.form.get("duree_valeur")
            duree_unite = request.form.get("duree_unite")
            formation.duree = f"{duree_valeur} {duree_unite}" if duree_valeur and duree_unite else formation.duree
            
            formation.nom = request.form.get("nom")
            formation.type = request.form.get("type")
            formation.description = request.form.get("description")
            duree_heures = request.form.get("duree_heures")
            formation.duree_heures = float(duree_heures) if duree_heures else None
            formation.dates = request.form.get("dates")
            formation.lieu = request.form.get("lieu")
            prix = request.form.get("prix")
            formation.prix = float(prix) if prix else None
            formation.conditions_acces = request.form.get("conditions_acces")
            formation.financement = request.form.get("financement")
            formation.presentation_intervenants = request.form.get("presentation_intervenants")
            
            lien_inscription = request.form.get("lien_inscription")
            if lien_inscription and not lien_inscription.startswith(("http://", "https://")):
                lien_inscription = "https://" + lien_inscription
            formation.lien_inscription = lien_inscription
            
            # Gestion des labels multiples depuis le formulaire
            labels = request.form.getlist("labels[]")
            formation.label = ','.join(labels) if labels else None
            
            # Gestion spéciale des certifications
            certification_input = request.form.get("certifications")
            if certification_input:
                # Mapping des certifications complètes vers leurs versions courtes
                certification_mapping = {
                    "DE (Diplôme d'État)": "DE",
                    "DNSP (Diplôme National Supérieur Professionnel)": "DNSP",
                    "RS (Répertoire Spécifique)": "RS",
                    "Formation Certifiante": "Formation Certifiante",
                    "Formation Non Certifiante": "Formation Non Certifiante"
                }
                # Utiliser la version courte si elle existe, sinon garder la valeur saisie
                formation.certifications = certification_mapping.get(certification_input, certification_input)
            else:
                formation.certifications = None

            formation.id_organisme = request.form.get("id_organisme")
            formation.etat = request.form.get("etat")

            db.session.commit()
            flash("Formation mise à jour avec succès!", "success")
            return redirect(url_for("formation.edit_formations"))
            
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la mise à jour: {str(e)}", "error")
        return redirect(url_for("formation.edit_formations"))

@formation_bp.route("/edit", methods=["GET"])
@admin_required
def edit_formations():
    formations = Formation.query.all()
    organismes = Organisme.query.all()

    # Récupérer les labels distincts
    labels_raw = db.session.query(Formation.label).distinct().all()
    labels_set = set()
    for label_row in labels_raw:
        if label_row[0] and label_row[0].strip().lower() != 'none':
            individual_labels = [l.strip() for l in label_row[0].split(',')]
            labels_set.update(individual_labels)
    labels = sorted([l for l in labels_set if l])

    # Récupérer les certifications distinctes
    certifications_raw = db.session.query(Formation.certifications).distinct().all()
    certifications_set = set()
    for cert_row in certifications_raw:
        if cert_row[0] and cert_row[0].strip().lower() != 'none':
            certifications_set.add(cert_row[0].strip())
    certifications = sorted([c for c in certifications_set if c])

    return render_template("edit_formations.html",
                         formations=formations,
                         organismes=organismes,
                         labels=labels,
                         certifications=certifications)

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
            formation.duree_heures = request.form.get(f"duree_heures_{id_}")
            formation.duree_heures = float(formation.duree_heures) if formation.duree_heures else None
            formation.dates = request.form.get(f"dates_{id_}")
            formation.lieu = request.form.get(f"lieu_{id_}")
            formation.prix = request.form.get(f"prix_{id_}")
            formation.prix = float(formation.prix) if  formation.prix else None
            formation.conditions_acces = request.form.get(f"conditions_acces_{id_}")
            formation.financement = request.form.get(f"financement_{id_}")
            formation.presentation_intervenants = request.form.get(f"presentation_intervenants_{id_}")
            formation.lien_inscription = request.form.get(f"lien_inscription_{id_}")
            formation.label = request.form.get(f"label_{id_}")
            formation.certifications = request.form.get(f"certifications_{id_}")
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
    duree_heures = request.form.get("duree_heures")
    duree_heures = float(duree_heures) if duree_heures else None
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
    certifications = request.form.get("certifications")
    id_organisme = request.form["id_organisme"]

    nouvelle_formation = Formation(
        nom=nom,
        type=type_,
        description=description,
        duree=duree,
        duree_heures=duree_heures,
        dates=dates,
        lieu=lieu,
        prix=prix,
        conditions_acces=conditions_acces,
        financement=financement,
        presentation_intervenants=presentation_intervenants,
        lien_inscription=lien_inscription,
        label=label,
        certifications=certifications,
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
        try:
            id_organisme = int(id_organisme) if id_organisme else None
        except ValueError:
            id_organisme = None
        description = request.form.get('description')
        duree_heures = request.form.get('duree_heures')
        try:
            duree_heures = float(duree_heures) if duree_heures else None
        except ValueError:
            duree_heures = None
        duree_valeur = request.form.get('duree_valeur')
        duree_unite = request.form.get('duree_unite')
        # Stocker dans la BDD uniquement la partie jours/semaines/mois/années
        duree = None
        if duree_valeur and duree_unite:
            duree = f"{duree_valeur} {duree_unite}"
        elif duree_heures:
            duree = f"{duree_heures} heures"
        elif duree_valeur and duree_unite:
            duree = f"{duree_valeur} {duree_unite}"

        dates = request.form.get('dates')
        lieu = request.form.get('adresse')
        prix = request.form.get('prix')
        prix = float(prix) if prix else None
        conditions_acces = request.form.get('conditions_acces')
        financement = request.form.get('financement')
        presentation_intervenants = request.form.get('presentation_intervenants')
        lien_inscription = request.form.get('lien_inscription')
        if lien_inscription and not lien_inscription.startswith("http://") and not lien_inscription.startswith("https://"):
            lien_inscription = "https://" + lien_inscription
        label = request.form.get('label')
        certifications = request.form.get('certifications')

        # Vérification des champs obligatoires pour éviter les erreurs d'intégrité
        if not nom or not type_formation or not id_organisme or not description or not duree or not dates or not lieu:
            flash("Merci de remplir tous les champs obligatoires du formulaire.", "danger")
            return redirect(url_for('formation.formulaire'))

        # Combiner adresse + code postal + ville
        adresse = request.form.get('adresse', '')
        code_postal = request.form.get('code_postal', '')
        ville = request.form.get('ville', '')
        lieu_complet = f"{adresse}, {code_postal} {ville}".strip()
        
        nouvelle_formation = Formation(
            nom=nom,
            type=type_formation,
            id_organisme=id_organisme,
            description=description,
            duree=duree,
            duree_heures=duree_heures,
            dates=dates,
            lieu=lieu_complet,
            prix=prix,
            conditions_acces=conditions_acces,
            financement=financement,
            presentation_intervenants=presentation_intervenants,
            lien_inscription=lien_inscription,
            label=label,
            certifications=certifications,
            etat='en_attente'
        )

        db.session.add(nouvelle_formation)
        db.session.commit()

        flash('Votre formation a été soumise avec succès et est en attente de validation.', 'success')

        # Redirection selon le rôle
        if hasattr(current_user, "is_admin") and current_user.is_admin:
            return redirect(url_for('formation.edit_formations', filtre='en_attente'))
        else:
            return redirect(url_for('dashboard'))

    except Exception as e:
        import traceback; print(traceback.format_exc())
        db.session.rollback()
        flash(f"Une erreur s'est produite lors de la soumission du formulaire: {str(e)}", 'danger')
        # Redirection selon le rôle même en cas d'erreur
        if hasattr(current_user, "is_admin") and current_user.is_admin:
            return redirect(url_for('formation.edit_formations'))
        else:
            return redirect(url_for('dashboard'))

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
            "duree_heures": f.duree_heures,
            "dates": f.dates,
            "lieu": f.lieu,
            "prix": f.prix,
            "conditions_acces": f.conditions_acces,
            "financement": f.financement,
            "presentation_intervenants": f.presentation_intervenants,
            "lien_inscription": f.lien_inscription,
            "label": f.label,
            "id_organisme": f.id_organisme,
            "duree_heures": float(f.duree_heures) if f.duree_heures is not None else None
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
    formation.raison = None
    db.session.commit()
    
    flash("Raison supprimée avec succès.", "success")
    return redirect(url_for('formation.edit_formations'))

@formation_bp.route("/duree-heures-range", methods=["GET"])
def get_duree_heures_range():
    # Récupérer les valeurs non nulles
    durees = db.session.query(Formation.duree_heures)\
        .filter(Formation.duree_heures != None)\
        .all()
    
    # Convertir en liste de nombres
    durees = [float(d[0]) for d in durees if d[0] is not None]
    
    # Si moins de 2 formations avec des durées, retourner les valeurs par défaut
    if len(durees) < 2:
        return jsonify({
            "min": 0,
            "max": 100
        })
    
    return jsonify({
        "min": min(durees),
        "max": max(durees)
    })

@formation_bp.route("/get-filters-data", methods=["GET"])
def get_filters_data():
    # Récupérer uniquement les formations validées
    formations_validees = Formation.query.filter_by(etat="valide")

    # Récupérer les labels distincts des formations validées
    labels_raw = formations_validees.with_entities(Formation.label).distinct().filter(Formation.label != None).all()
    labels_set = set()
    for label_row in labels_raw:
        if label_row[0]:
            for l in str(label_row[0]).split(','):
                l = l.strip()
                if l:
                    labels_set.add(l)
    
    # Récupérer les financements distincts des formations validées
    financements_raw = formations_validees.with_entities(Formation.financement).distinct().filter(Formation.financement != None).all()
    financements_set = set()
    for financement_row in financements_raw:
        if financement_row[0]:
            for f in str(financement_row[0]).split(','):
                f = f.strip()
                if f:
                    financements_set.add(f)
    
    # Récupérer les certifications distinctes des formations validées
    certifications_raw = formations_validees.with_entities(Formation.certifications).distinct().filter(Formation.certifications != None).all()
    certifications_set = set()
    for cert_row in certifications_raw:
        if cert_row[0]:
            cert = cert_row[0].strip()
            if cert:
                certifications_set.add(cert)

    return jsonify({
        'labels': sorted(list(labels_set)),
        'financements': sorted(list(financements_set)),
        'certifications': sorted(list(certifications_set))
    })

