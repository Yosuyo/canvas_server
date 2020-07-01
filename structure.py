def createImage(smiles):
    from rdkit import Chem
    from rdkit.Chem import rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D
    from rdkit.Chem.Draw.MolDrawing import DrawingOptions

    mol = Chem.MolFromSmiles(smiles)  # Penicillin
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
    with open("static/images/"+smiles+".svg", "w") as f:
        f.write(svg)