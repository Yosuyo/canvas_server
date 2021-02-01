def searchReaction(smiles):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    import sql

    mol = Chem.MolFromSmiles(smiles)

    reactionData = sql.sqlSELECT("SELECT * FROM reaction")

    hitId = []
    for data in reactionData:
        smarts = Chem.MolFromSmarts(data["site"])
        if(mol.HasSubstructMatch(smarts)):
            hitId.append(data["id"])

    hitData = []
    for n in hitId:
        hitData.append(reactionData[n-1])

    return hitData

def searchAdditionalReaction(smiles, filename):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    import csv
    mol = Chem.MolFromSmiles(smiles)
    reactionData = []
    with open("./static/csv/"+filename) as f:
        reader = csv.reader(f)
        for row in reader:
            reactionData.append(row)
    hitData = []
    for data in reactionData:
        smarts = Chem.MolFromSmarts(data[2])
        if(mol.HasSubstructMatch(smarts)):
            dic = {"id":data[0],"name":data[1],"site":data[2],"smarts":data[3],"condition":data[4]}
            hitData.append(dic)
    return hitData

def getAdditionalReaction(id, filename):
    import csv
    reaction = []
    with open("./static/csv/"+filename) as f:
        reader = csv.reader(f)
        for data in reader:
            if int(data[0]) == id:
                dic = {"id":data[0],"name":data[1],"site":data[2],"smarts":data[3],"condition":data[4]}
                reaction.append(dic)
                break
    return reaction

    #反応データベースのデータ構造
    #'id': 番号(int), 'name': 反応名(varchar), 'site': 生成部位SMARTS(varchar), 'smarts': 逆合成変換reactionSMARTS(varchar), 'condition': 反応詳細(varchar)}