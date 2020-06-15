from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/main/')
def main():
    return render_template("main.html")

@app.route("/main/test", methods=["GET"])
def main_test():
    test_result = "TEST"
    return render_template("main.html", test_result = test_result)


if __name__ == "__main__":
    app.run()