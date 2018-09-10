from flask import Flask, render_template

app = Flask('back_tv')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
