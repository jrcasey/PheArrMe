from cobra.io import read_sbml_model
import os
import pandas as pd


# Check in data/models/ for strains with both gapfilled and ungapfilled models
def findBothModels(MODELDIR):
    # Find all files in data/models/
    file_list = os.listdir(MODELDIR)

    # Find files with "_gf" in their names
    gf_list = []
    for file in file_list:
        if "_gf" in file:
            gf_list.append(file)

    # Find files with "_ngf" in their names
    nongf_list = []
    for file in file_list:
        if "_ngf" in file:
            nongf_list.append(file)

    # Find the strains with both gapfilled and ungapfilled models
    both_list = []
    for gf in gf_list:
        gf_strain = gf.split("_gf.xml")[0]
        for nongf in nongf_list:
            nongf_strain = nongf.split("_ngf.xml")[0]
            if gf_strain == nongf_strain:
                both_list.append(gf_strain)
    return both_list

# Load both gapfilled and ungapfilled models
def loadBothModels(both_list, MODELDIR):
    gf_models = []
    nongf_models = []
    for strain in both_list:
        gf_models.append(read_sbml_model(MODELDIR + strain + "_gf.xml"))
        nongf_models.append(read_sbml_model(MODELDIR + strain + "_ngf.xml"))
    return gf_models, nongf_models


# Find the reactions that are in the gapfilled model but not in the ungapfilled model
def findGapfillReactions(gf_models, nongf_models):
    gapfill_reactions = []
    for i in range(len(gf_models)):
        gf_model = gf_models[i]
        nongf_model = nongf_models[i]
        gf_reactions = set([r.id for r in gf_model.reactions])
        nongf_reactions = set([r.id for r in nongf_model.reactions])
        gapfill_reactions.append(gf_reactions.difference(nongf_reactions))
    return gapfill_reactions

# Create a dataframe with the strain name, the number of reactions, the number of metabolites, the number of genes, the number of gapfilled reactions, and the gapfilled reactions.
def createTable(gapfill_reactions, both_list, gf_models):
    table = pd.DataFrame(columns=['strain', 'num_reactions', 'num_metabolites', 'num_genes', 'num_gapfill_reactions', 'gapfill_reactions'])
    for i in range(len(both_list)):
        table.loc[i] = [both_list[i], len(gf_models[i].reactions), len(gf_models[i].metabolites), len(gf_models[i].genes), len(gapfill_reactions[i]), gapfill_reactions[i]]
    return table

# Write the table to a file
def writeTable(table):
    table.to_csv("data/tables/modelDescriptions.tsv", sep='\t', index=False)

def main():
    # Directories
    MODELDIR = "data/models/"
    both_list = findBothModels(MODELDIR)
    gf_models, nongf_models = loadBothModels(both_list, MODELDIR)
    gapfill_reactions = findGapfillReactions(gf_models, nongf_models)
    table = createTable(gapfill_reactions, both_list, gf_models)
    writeTable(table)

if __name__ == "__main__":
    main()

