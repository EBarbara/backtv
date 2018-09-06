from flask import render_template
from flask_jwt_extended import JWTManager
import connexion

app = connexion.FlaskApp(__name__, specification_dir='swagger/')
app.add_api('BackScreen.yaml', strict_validation=True)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
