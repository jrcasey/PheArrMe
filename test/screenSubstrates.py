# Check which substrates in the Biolog database are a problem for CarveMe

import pandas as pd
from src.generateMedia import load_mapping, load_baseMedium, load_soleC_lists, map_to_BiGG, build_media_tables
from src.runCarveBatch import generateMediaList, compileCommand
import subprocess


# DIRECTORIES
BASEMEDIUM_PATH = "data/biolog/baseMedium.tsv"
MAPPING_PATH = "data/biolog/mapping_Biolog_BiGG.tsv"

# load biolog mapping file
mapping = load_mapping(MAPPING_PATH)

# Check if matching BiGG ID is 'nan' or if 'include' column is 0, if not, append 'Biolog_name' to a list and 'BiGG' to another list. 
matching_BiGG_IDs = []
soleC_list = []
for i in range(len(mapping)):
    if not mapping.loc[i, 'BiGG'] == 'nan' and mapping.loc[i, 'include'] == 1:
        matching_BiGG_IDs.append(mapping.loc[i, 'BiGG'])
        soleC_list.append(mapping.loc[i, 'Biolog_name'])

# load base medium
baseMedium = load_baseMedium(BASEMEDIUM_PATH)
# generate media tables
mediaTable = build_media_tables(baseMedium, matching_BiGG_IDs, soleC_list)
# save media table to test/allMedia.tsv
mediaTable.to_csv("test/allMedia.tsv", sep='\t', index=False)

# generate a comma-separated list of the media IDs
mediaIDs = mediaTable['medium'].unique().tolist()
media_list = ','.join(mediaIDs)

# inputs for carve
genome_dir = "data/genomes/faa/13M1.1.faa" # pick a genome
mediadb_dir = "test/allMedia.tsv" # use the full media table generated above
output_dir = "test/testModel.xml"


# compile the command for each medium in the media list
for medium in mediaIDs:
    cmd = compileCommand(genome_dir, medium, mediadb_dir, output_dir)
    # run carve
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        # write the error to a log file
        with open("test/error.log", "a") as f:
            f.write(f"Command failed for medium {medium}:\n")
            f.write(e.stderr.decode())
