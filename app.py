from flask import render_template
import connexion

app = connexion.FlaskApp(__name__, specification_dir='swagger/')
app.add_api('BackScreen.yaml', strict_validation=True)


@app.route('/')
def home():
    return render_template('home.html')

