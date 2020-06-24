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

@app.route("/main/reaction")
def reactionDef():
    return "REACTION!!"

@app.route("/main/smiles")
def returnSmiles():
    import re
    get = request.args.get("smiles","")
    out = get.translate(str.maketrans({"~":r"#"})) #送られてきたsmilesの~を#に翻訳
    out = re.sub("H","",out) #送られてきたsmilesのHを削除

    from rdkit import Chem
    mol = Chem.MolFromSmiles(out)

    return Chem.MolToSmiles(mol)

if __name__ == "__main__":
    app.run()