from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")
#メイン画面
@app.route('/main/')
def main():
    return render_template("main.html")
#smilesを送信したとき
@app.route("/main/smiles")
def returnSmiles():
    import re
    get = request.args.get("smiles","")
    out = get.translate(str.maketrans({"~":r"#"})) #送られてきたsmilesの~を#に翻訳
    out = re.sub("H","",out) #送られてきたsmilesのHを削除
    getfilename = request.args.get("additionlFilename","")

    import search
    results = search.searchReaction(out)
    try:
        results = results + search.searchAdditionalReaction(out,getfilename)
    except:
        print("pass")
        pass

    return render_template("list.html", results=results)
#反応を選択したとき
@app.route("/main/detail")
def reactionDetail():
    getid = request.args.get("id","")
    getsmiles = request.args.get("smiles","")
    getsmiles = getsmiles.translate(str.maketrans({"~":r"#"}))
    getfilename = request.args.get("additionlFilename","")

    if int(getid) < 10000:
        import sql
        reaction = sql.sqlSELECT("SELECT * FROM reaction WHERE id = %s" % str(getid))
    else:
        import search
        reaction = search.getAdditionalReaction(int(getid),getfilename)
    #入力構造式のsvgを作成
    import structure
    print(reaction)
    structure.createImageHighlight(getsmiles, reaction[0]["site"])
    #smartsによる変換の実行
    from rdkit import Chem
    from rdkit.Chem import AllChem
    mol = Chem.MolFromSmiles(getsmiles)
    rxn = AllChem.ReactionFromSmarts(reaction[0]["smarts"])
    precursor = rxn.RunReactants([mol])
    #出力構造式のsvgを作成
    prelist = []
    for x in precursor:
        xlist = []
        for y in x:
            xlist.append(Chem.MolToSmiles(y))
        prelist.append(xlist)
    def get_unique_list(seq): #リスト内の被りを削除する関数
        seen = []
        return [x for x in seq if x not in seen and not seen.append(x)]
    prelist = get_unique_list(prelist)
    for x in prelist:
        for y in x:
            structure.createImage(y)

    return render_template("detail.html", getid=getid, prelist=prelist, getsmiles=getsmiles, reaction=reaction[0], num=0)
#反応の別パターンを選択したとき
@app.route("/main/detail_celect")
def reactionDetailCelect():
    getid = request.args.get("id","")
    getnum = request.args.get("num","")
    getsmiles = request.args.get("smiles","")
    getsmiles = getsmiles.translate(str.maketrans({"~":r"#"}))
    getfilename = request.args.get("additionlFilename","")
    if int(getid) < 10000:
        import sql
        reaction = sql.sqlSELECT("SELECT * FROM reaction WHERE id = %s" % str(getid))
    else:
        import search
        reaction = search.getAdditionalReaction(int(getid),getfilename)
    #smartsによる変換の実行
    from rdkit import Chem
    from rdkit.Chem import AllChem
    mol = Chem.MolFromSmiles(getsmiles)
    rxn = AllChem.ReactionFromSmarts(reaction[0]["smarts"])
    precursor = rxn.RunReactants([mol])
    prelist = []
    for x in precursor:
        xlist = []
        for y in x:
            xlist.append(Chem.MolToSmiles(y))
        prelist.append(xlist)
    def get_unique_list(seq): #リスト内の被りを削除する関数
        seen = []
        return [x for x in seq if x not in seen and not seen.append(x)]
    prelist = get_unique_list(prelist)

    return render_template("detail.html", getid=getid, prelist=prelist, getsmiles=getsmiles, reaction=reaction[0], num=int(getnum))
#設定から反応ファイルをアップロードしたとき
@app.route("/main/upload", methods=["POST"])
def upload_additionalData():
    import os
    if "file" not in request.files:
        return "エラー：ファイルが正しく選択されていません"
    fs = request.files["file"]
    filename = fs.filename
    if not filename.endswith(".csv"):
        return "エラー：ファイルがcsv形式ではありません"
    saveaddress = "./static/csv/"
    fs.save(os.path.join(saveaddress, "pre_"+filename)) #保存
    #Shift_JISならutf-8に変換
    try:
        with open(saveaddress+"pre_"+filename,"rb") as f:
            with open(saveaddress+filename,"w",newline="") as g:
                g.write(f.read().decode(encoding="utf-8"))
        os.remove(saveaddress+"pre_"+filename)
    except:
        pass

    return render_template("main.html", filename=filename)

if __name__ == "__main__":
    app.run()