from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/main/')
def main():
    return render_template("main.html")

@app.route("/main/reaction")
def reactionDef():
    return "REACTION!!"

@app.route("/main/smiles")
def returnSmiles():
    import re
    get = request.args.get("smiles","")
    out = get.translate(str.maketrans({"~":r"#"})) #送られてきたsmilesの~を#に翻訳
    out = re.sub("H","",out) #送られてきたsmilesのHを削除

    import search
    results = search.searchReaction(out)

    return render_template("list.html", results = results)

@app.route("/main/detail")
def reactionDetail():
    getid = request.args.get("id","")
    getsmiles = request.args.get("smiles","")
    
    import sql
    reaction = sql.sqlSELECT("SELECT * FROM reaction WHERE id = %s" % str(getid))

    #入力構造式のsvgを作成
    import structure
    structure.createImage(getsmiles)
    #smartsによる変換の実行
    from rdkit import Chem
    from rdkit.Chem import AllChem
    mol = Chem.MolFromSmiles(getsmiles)
    rxn = AllChem.ReactionFromSmarts(reaction[0]["smarts"])
    precursor = rxn.RunReactants([mol])
    #出力構造式のsvgを作成
    prelist = []
    print(prelist)
    for x in precursor:
        prelist.append(Chem.MolToSmiles(x[0]))
        print(Chem.MolToSmiles(x[0]))
    prelist = list(set(prelist)) #被り無しの前駆体smilesリスト
    for item in prelist:
        structure.createImage(item)

    return render_template("detail.html", prelist = prelist, getsmiles = getsmiles)

@app.route("/main/test")
def glap_test():
    return render_template("imgtest.html")

if __name__ == "__main__":
    app.run()