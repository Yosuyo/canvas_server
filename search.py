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
    with open("/static/csv/"+filename) as f:
        reader = csv.reader(f)
        for row in reader:
            reactionData.append(row)
    hitId = []
    for data in reactionData:
        smarts = Chem.MolFromSmarts(data["site"])
        if(mol.HasSubstructMatch(smarts)):
            hitId.append(data["id"])
    hitData = []
    for n in hitId:
        hitData.append(reactionData[n-1])
    return hitData

def getAdditionalReaction(id, filename):
    import csv
    reaction = []
    with open("/static/csv/"+filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == id:
                reaction = row
                break
    return reaction