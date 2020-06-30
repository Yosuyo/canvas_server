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

if __name__ == "__main__":
    searchReaction("CC=C")
