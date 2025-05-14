from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.ModelUtilisateur import Utilisateur
from database import db

utilisateur_bp = Blueprint("utilisateur", __name__, url_prefix="/utilisateur")

@utilisateur_bp.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = Utilisateur.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash("Connexion réussie!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Email ou mot de passe incorrect", "danger")
    
    return render_template("connexion.html")

@utilisateur_bp.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    flash("Vous avez été déconnecté", "info")
    return redirect(url_for("carte"))

@utilisateur_bp.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        password = request.form.get("password")
        num_adherent = request.form.get("num_adherent")
        
        if Utilisateur.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé", "danger")
            return redirect(url_for("utilisateur.inscription"))
        
        new_user = Utilisateur(
            nom=nom,
            email=email,
            role='user',
            num_adherent=num_adherent
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Inscription réussie! Vous pouvez maintenant vous connecter", "success")
        return redirect(url_for("utilisateur.connexion"))
    
    return render_template("inscription.html")