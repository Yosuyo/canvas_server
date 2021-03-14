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
    results = ""
    try:
        results = search.searchReaction(out)
        if getfilename != "":
            results = results + search.searchAdditionalReaction(out,getfilename)
        else:
            pass
    except:
        import traceback
        traceback.print_exc()
        pass

    return render_template("list.html", results=results)
#反応を選択したとき
@app.route("/main/detail")
def reactionDetail():
    import re
    getid = request.args.get("id","")
    getsmiles = request.args.get("smiles","")
    getsmiles = getsmiles.translate(str.maketrans({"~":r"#"}))
    getsmiles = re.sub("H","",getsmiles)
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
    structure.createImage(getsmiles)
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
    #構造式を出力する。出来ない場合はありえない構造としてエラー表示を返し、前駆体リストを消去する
    error = ""
    try:
        for x in prelist:
            for y in x:
                structure.createImage(y)
    except:
        error = "※ERROR:適用できない反応です"
        prelist = []
    #反応部位の*を^に置換してHTMLへ渡す
    rSmarts = reaction[0]["site"].translate(str.maketrans({"*":"^"}))

    return render_template("detail.html", getid=getid, prelist=prelist, getsmiles=getsmiles, reaction=reaction[0], num=0, rSmarts=rSmarts, err=error)
#反応の別パターンを選択したとき
@app.route("/main/detail_celect")
def reactionDetailCelect():
    import re
    getid = request.args.get("id","")
    getnum = request.args.get("num","")
    getsmiles = request.args.get("smiles","")
    getsmiles = getsmiles.translate(str.maketrans({"~":r"#"}))
    getsmiles = re.sub("H","",getsmiles)
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
    #反応部位の*を^に置換してHTMLへ渡す
    rSmarts = reaction[0]["site"].translate(str.maketrans({"*":"^"}))

    return render_template("detail.html", getid=getid, prelist=prelist, getsmiles=getsmiles, reaction=reaction[0], num=int(getnum), rSmarts=rSmarts)
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

#ツリーの構造式画像送信
@app.route('/main/tree')
def tree_pic():
    return render_template("img.html")

#反応データベースの編集
@app.route('/main/reactiondb_menu')
def reactiondb():
    return render_template("reactiondb.html")

#反応データベースのリストを表示
@app.route('/main/reactiondb_all')
def reactiondb_all():
    import sql
    result = sql.sqlSELECT("SELECT * from reaction")
    return render_template("reactiondb_all.html", result=result)

#反応データの追加
@app.route('/main/reactiondb_add', methods=["POST"])
def reactiondb_add():
    from flask import request
    import sql
    name = str(request.form["name"])
    site = str(request.form["site"])
    smarts = str(request.form["smarts"])
    condition = str(request.form["condition"])
    id_list = sql.sqlSELECT("SELECT id from reaction")
    newid = str(id_list[-1]["id"] +1)
    try:
        sql.sqlUPDATE("INSERT INTO reaction VALUES ("+newid+",'"+name+"','"+site+"','"+smarts+"','"+condition+"')")
        result = "データの追加に成功しました。反応データ一覧からご確認ください。　反応id："+newid
    except Exception as e:
        result = e.args

    return render_template("reactiondb_result.html",result=result)

#反応データの修正
@app.route('/main/reactiondb_change', methods=["POST"])
def reactiondb_change():
    from flask import request
    import sql
    id = str(request.form["id"])
    name = str(request.form["name"])
    site = str(request.form["site"])
    smarts = str(request.form["smarts"])
    condition = str(request.form["condition"])
    command = ""
    if id == "":
        result = "エラー：idを入力してください"
        return render_template("reactiondb_result.html",result=result)
    if name != "":
        command = command + " name='" + name + "'"
    if site != "":
        command = command + " site='" + site + "'"
    if smarts != "":
        smarts = command + " smarts='" + smarts + "'"
    if condition != "":
        condition = command + " condition='" + condition + "'"
    try:
        sql.sqlUPDATE("UPDATE reaction SET"+command+" WHERE id="+id)
        result = "データの修正に成功しました。反応データ一覧からご確認ください。　反応id："+id
    except Exception as e:
        result = e.args

    return render_template("reactiondb_result.html",result=result)

#反応データの削除
@app.route('/main/reactiondb_delete', methods=["POST"])
def reactiondb_delete():
    from flask import request
    import sql
    import datetime
    id = str(request.form["id"])
    try:
        data = sql.sqlSELECT("SELECT * FROM reaction")
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y-%m-%d-%H-%M-%S')
        with open("static/data/"+time+".txt", "w") as f:
            for row in data:
                frow = "id:"+str(row["id"])+" name:"+row["name"]+" site:"+row["site"]+" smarts:"+row["smarts"]+" condition:"+row["condition"]+"\n"
                f.write(frow)
        sql.sqlUPDATE("DELETE FROM reaction WHERE id="+id)
        result = "データの削除に成功しました。反応データ一覧からご確認ください。　削除済み反応id："+id
    except Exception as e:
        result = e.args

    return render_template("reactiondb_result.html",result=result)

if __name__ == "__main__":
    app.run()