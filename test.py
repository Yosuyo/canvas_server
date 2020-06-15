from rdkit import Chem
from rdkit.Chem import AllChem
# Molファイルの生成
sample = Chem.MolFromSmiles('C=CCC')
benzoic_acid = Chem.MolFromSmiles('c1ccccc1C(=O)O')
benzylamine = Chem.MolFromSmiles('c1ccccc1CN')

smarts = '[C:1](=[O:2])O.[N!0H:3][C:4]>>[C:1](=[O:2])[N!0H:3][C:4]'

rxn3 = AllChem.ReactionFromSmarts(smarts)

x = rxn3.RunReactants([benzoic_acid, benzylamine])

print(len(x))
print(x)
print(x[0][0])
print(Chem.MolToSmiles(x[0][0]))
"""
print(Chem.MolToSmiles(benzoic_acid))
print(Chem.MolToSmiles(sample)) #smilesとしての出力
"""