from flask import Flask, render_template, url_for
from forms import RunForm
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asbjomsl897jk'


@app.route("/")
@app.route("/home")
def hello():
    form = RunForm()
    return render_template('home.html', form=form)


@app.route("/about")
def about():
    return render_template('about.html')




if __name__ == '__main__':
    app.run(debug=True)



