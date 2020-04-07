from rdkit import Chem

sample = Chem.MolFromSmiles('c1ccccc1')

print(sample)
print(Chem.MolToSmiles(sample))