from flask import Flask, render_template

# Crée l'application Flask
app = Flask(__name__)

# Route d'accueil
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    # Lance l'app sur 0.0.0.0 pour être accessible à l'extérieur du container
    app.run(host='0.0.0.0', port=5000)
