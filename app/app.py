from flask import Flask, render_template
from controllers.ControllerOrganisme import *
from controllers.ControllerFormation import *
from database import *

app = Flask(__name__)
app.config.from_object("config.Config")

init_db(app)

app.register_blueprint(organisme_bp)
app.register_blueprint(formation_bp)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/carte')
def carte():
    return render_template('carte.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
