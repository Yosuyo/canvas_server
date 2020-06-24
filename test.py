from rdkit import Chem
from rdkit.Chem import AllChem

# Molファイルの生成
sample = Chem.MolFromSmiles('C=CCC')
benzoic_acid = Chem.MolFromSmiles('c1ccccc1C(=O)O')
benzylamine = Chem.MolFromSmiles('c1ccccc1CN')

smarts = '[C:1](=[O:2])O.[N!0H:3][C:4]>>[C:1](=[O:2])[N!0H:3][C:4]'

rxn3 = AllChem.ReactionFromSmarts(smarts)

x = rxn3.RunReactants([benzoic_acid, benzylamine])

"""
print(Chem.MolToSmiles(benzoic_acid))
print(Chem.MolToSmiles(sample)) #smilesとしての出力
"""

print(len(x))
print(x)
print(x[0][0])
print(Chem.MolToSmiles(x[0][0]))

from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.Draw.MolDrawing import DrawingOptions

mol = Chem.MolFromSmiles("CC1(C(N2C(S1)C(C2=O)NC(=O)CC3=CC=CC=C3)C(=O)O)C")  # Penicillin
rdDepictor.Compute2DCoords(mol)  # for generating conformer ID
# create a drawer container
drawer = rdMolDraw2D.MolDraw2DSVG(300, 300)
# define drawer options
drawer.drawOptions().updateAtomPalette({k: (0, 0, 0) for k in DrawingOptions.elemDict.keys()})
drawer.SetLineWidth(2)
drawer.SetFontSize(1.0)
#
drawer.DrawMolecule(mol)
drawer.FinishDrawing()
# generate and write the svg strings
svg = drawer.GetDrawingText().replace('svg:', '')
with open("mol.svg", "w") as f:
    f.write(svg)
