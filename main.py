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
    
    import sql
    reaction = sql.sqlSELECT("SELECT * FROM reaction WHERE id = %s" % str(getid))
    print(reaction)

    return reaction[0]["name"]

@app.route("/main/test")
def glap_test():
    return render_template("imgtest.html")

if __name__ == "__main__":
    app.run()