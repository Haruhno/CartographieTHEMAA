# Cartographie des formations en arts de la marionnette

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)

Application web développée pour THEMAA (Association nationale des Théâtres de Marionnettes et des Arts Associés) dans le cadre d'un stage.

## Fonctionnalités principales

- 🌍 **Carte interactive** des formations avec Leaflet.js
- 🔍 **Moteur de recherche** avec filtres (type de formation, techniques, financements...)
- 📝 **Formulaire** de contribution (ajouts de formations) pour les organismes
- 👥 **Gestion des rôles** (visiteur, adhérent, administrateur)
- ✅ **Système de modération** des contributions
- 📱 **Design responsive** adapté à tous les appareils

## Prérequis (Si docker n'est pas utilisé)

- Python 3.9+
- pip
- WampServer (ou MAMP, XAMPP..)


## 🚀 Installation avec Docker (recommandé)

### Prérequis
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé
- Git (pour cloner le dépôt)

### Premier démarrage

#### 1. Cloner le dépôt
```bash
git clone https://github.com/Haruhno/CartographieTHEMAA.git
cd CartographieTHEMAA
```

# 2. Lancer les containers Docker
```bash
docker-compose up --build -d
```

# 3. Accéder aux services :
```bash
Application : http://localhost:5000/

phpMyAdmin : http://localhost:8080/ 
```
