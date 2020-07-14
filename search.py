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

def searchAdditionalReaction(smiles, fileName):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    import csv
    mol = Chem.MolFromSmiles(smiles)
    data = []
    with open("/static/csv/"+fileName) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    print(type(data))
    print(data)
