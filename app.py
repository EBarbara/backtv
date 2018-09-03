from flask import render_template
import connexion

app = connexion.FlaskApp(__name__, specification_dir='swagger/')
app.add_api('BackScreen.yaml')
app.run(host='0.0.0.0', port=5000, debug=True)


@app.route('/')
def home():
    return render_template('home.html')

