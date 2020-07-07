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
    with open("static/images/svgs/"+smiles+".svg", "w") as f:
        f.write(svg)

def createImageHighlight(smiles, smarts):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from rdkit.Chem import rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D
    from rdkit.Chem.Draw.MolDrawing import DrawingOptions

    mol = Chem.MolFromSmiles(smiles)
    patt = Chem.MolFromSmarts(smarts)
    hitatoms = mol.GetSubstructMatches(patt) #反応部位のアトムインデックス
    hitatomslist = []
    for x in hitatoms:
        hitatomslist += x
    hitatomsSum = tuple(hitatomslist)
    tm = rdMolDraw2D.PrepareMolForDrawing(mol)
    rdDepictor.Compute2DCoords(mol)  # for generating conformer ID
    # create a drawer container
    drawer = rdMolDraw2D.MolDraw2DSVG(300, 300)
    # define drawer options
    drawer.drawOptions().updateAtomPalette({k: (0, 0, 0) for k in DrawingOptions.elemDict.keys()})
    drawer.SetLineWidth(2)
    drawer.SetFontSize(1.0)
    drawer.drawOptions().setHighlightColour((0.95,0.7,0.95)) #ハイライトの色指定
    drawer.DrawMolecule(tm, highlightAtoms=hitatomsSum)
    drawer.FinishDrawing()
    # generate and write the svg strings
    svg = drawer.GetDrawingText().replace('svg:', '')
    with open("static/images/svgs/"+smiles+"_"+smarts+".svg", "w") as f:
        f.write(svg)