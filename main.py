from flask import Flask ,render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/main/')
def main():
    return render_template("main.html")

@app.route("/show/<name>", methods=["GET"])
def main_test(name):
    return "Smiles, {}".format(name)

if __name__ == "__main__":
    app.run()