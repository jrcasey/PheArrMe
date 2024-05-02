import os
import pandas as pd

# Read in mapping
def load_mapping(MAPPING_PATH):
    mapping = pd.read_csv(MAPPING_PATH, sep='\t')
    # specify the types of the columns
    mapping['Biolog_name'] = mapping['Biolog_name'].astype(str)
    mapping['BiGG'] = mapping['BiGG'].astype(str)
    mapping['include'] = mapping['include'].astype(int)
    return mapping

# Read in base medium
def load_baseMedium(BASEMEDIUM_PATH):
    baseMedium = pd.read_csv(BASEMEDIUM_PATH, sep='\t')
    return baseMedium

# Read in sole carbon lists for all strains
def load_soleC_lists(file):
    soleC_list = pd.read_csv(file, sep='\t', header=None)
    soleC_list = soleC_list.iloc[0,:].astype(str).values.tolist() # Convert to list of strings
    return soleC_list

def map_to_BiGG(mapping, soleC_list):
    # preallocate new soleC_list and matching_BiGG_IDs
    soleC_list_new = []
    matching_BiGG_IDs = []
    # Loop through each entry in soleC_list and find matching BiGG ID in mapping
    for i in range(len(soleC_list)):
        # Check if soleC_list entry is in mapping
        if soleC_list[i] in mapping['Biolog_name'].values.tolist():
            # If so, get the matching BiGG ID
            matching_BiGG_ID = mapping.loc[mapping['Biolog_name'] == soleC_list[i], 'BiGG'].values.tolist()[0]
            # Check if matching BiGG ID is NaN, if so, remove it. Also check if the 'include' column is 1
            if not matching_BiGG_ID == 'nan' and mapping.loc[mapping['Biolog_name'] == soleC_list[i], 'include'].values.tolist()[0] == 1:
                soleC_list_new.append(soleC_list[i])
                matching_BiGG_IDs.append(matching_BiGG_ID)
    return matching_BiGG_IDs, soleC_list_new

# build the media tables by concatenating the base medium with the sole carbon sources
def build_media_tables(baseMedium, matching_BiGG_IDs, soleC_list_new):
    # Add '_medium' to BiGG ID to get media ID
    newMediaID = [cpd + '_medium' for cpd in matching_BiGG_IDs] 
    # Add description for media
    newMediaDesc = ['M9 medium containing ' + cpdName + ' as sole carbon source' for cpdName in soleC_list_new]
    # Initialize dataframe
    mediaTable = pd.DataFrame(columns=['medium', 'description', 'compound', 'name'])
    # Loop through all sole carbon sources and concatenate with base medium
    for i in range(len(matching_BiGG_IDs)):
        newMedia = pd.DataFrame({'medium': newMediaID[i], 'description': newMediaDesc[i], 'compound': matching_BiGG_IDs[i], 'name': soleC_list_new[i]},index=[0]).merge(baseMedium, how='outer')
        # replace medium and description with newMediaID and newMediaDesc for all rows
        newMedia['medium'] = newMediaID[i]
        newMedia['description'] = newMediaDesc[i]
        # Concatenate the newMedia dataframe with the mediaTable
        mediaTable = pd.concat([mediaTable, newMedia])
    return mediaTable

# Main function - loop through all sole carbon lists and generate media tables
def main():
    # Directories
    BASEMEDIUM_PATH = "data/phearr/baseMedium.tsv"
    SOLEC_LIST_DIR = "data/phearr/soleC_lists/"
    MEDIATABLES_DIR = "data/phearr/mediaTables/"
    MAPPING_PATH = "data/phearr/mapping_Biolog_BiGG.tsv"
    mapping = load_mapping(MAPPING_PATH)
    baseMedium = load_baseMedium(BASEMEDIUM_PATH)
    files = os.listdir(SOLEC_LIST_DIR)
    for file in files:
        soleC_list = load_soleC_lists(SOLEC_LIST_DIR + file)
        matching_BiGG_IDs, soleC_list_new = map_to_BiGG(mapping, soleC_list)
        # now build the media tables by concatenating the base medium with the sole carbon sources
        mediaTable = build_media_tables(baseMedium, matching_BiGG_IDs, soleC_list_new)
        # save the media tables for each strain
        mediaTable.to_csv(MEDIATABLES_DIR + file, sep='\t', index=False)

# Run main function
if __name__ == "__main__":
    main()
