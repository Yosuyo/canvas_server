from flask import Flask ,render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/main/')
def main():
    return render_template("main.html")

@app.route("/test", methods=["GET","POST"])
def main_test(name):

    if request.methods =="POST":
        param = request.
        return "Smiles, {}".format(name)
    else:
        return render_template("main.html")

if __name__ == "__main__":
    app.run()