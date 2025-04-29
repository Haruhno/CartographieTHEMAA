from flask import Flask, render_template
from controllers.ControllerOrganisme import *
from database import *

app = Flask(__name__)
app.config.from_object("config.Config")

init_db(app)

app.register_blueprint(organisme_bp)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
