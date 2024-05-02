import subprocess
import sys
import os
import argparse
import pandas as pd

# # Parse arguments
# parser = argparse.ArgumentParser(description='Run carve on a batch of genomes')
# parser.add_argument('genomes', type=str, help='A list of organisms to run carve on. Each genome should be named identically to the corresponding media table (ignoring the extension, obviously).')
# args = parser.parse_args()
# genomes = args.genomes.split(',')

# find the corresponding genome faa directory for each organism
def findGenome(GENOME_PATH,genome):
    genome_dir = GENOME_PATH + genome + ".faa"
    # check if the genome directory exists
    if not os.path.exists(genome_dir):
        raise ValueError("The genome directory does not exist.")
    return genome_dir

# find the corresponding media table for each organism
def findMediaTable(MEDIADB_PATH,genome):
    mediadb_dir = MEDIADB_PATH + genome + ".tsv"
    # check if the media table exists
    if not os.path.exists(mediadb_dir):
        raise ValueError("The media table does not exist.")
    return mediadb_dir

# generate a comma-separated list of the media IDs
def generateMediaList(mediadb_dir):
    # read in the media table
    mediaTable = pd.read_csv(mediadb_dir, sep='\t')
    # extract the media IDs
    mediaIDs = mediaTable['medium'].unique().tolist()
    # convert the list to a comma-separated string
    gf_media_list = ','.join(mediaIDs)
    return gf_media_list

# Set up the arguments for carve (carve --gapfill <genome_dir> --mediadb <mediadb_dir> -o <output_dir>)
def compileCommand(genome_dir, gf_media_list, mediadb_dir, output_dir):
    # assign carve command
    command = "carve"
    # first argument is the path to the genome (faa file)
    arg1 = genome_dir
    # second argument is the gapfill flag "--gapfill"
    arg2 = "--gapfill"
    # third argument is a comma-separated list of the gapfilling media to use
    arg3 = gf_media_list
    # fourth argument is the media database flag "--mediadb"
    arg4 = "--mediadb"
    # fifth argument is the path to the media database (tsv file)
    arg5 = mediadb_dir
    # sixth argument is the output directory flag "-o"
    arg6 = "-o"
    # seventh argument is the output directory name (xml file)
    arg7 = output_dir
    # compile the command
    cmd = [command, arg1, arg2, arg3, arg4, arg5, arg6, arg7]
    return cmd

# Generate a non-gapfilled model for each organism
def compileCommandNoGapfill(genome_dir, output_dir):
    # assign carve command
    command = "carve"
    # first argument is the path to the genome (faa file)
    arg1 = genome_dir
    # second argument is the output directory flag "-o"
    arg2 = "-o"
    # third argument is the output directory name (xml file)
    arg3 = output_dir
    # compile the command
    cmd = [command, arg1, arg2, arg3]
    return cmd

def main():
    # Set up the paths
    GENOME_PATH = "data/genomes/faa/"
    MEDIADB_PATH = "data/phearr/mediaTables/"

    # Retrieve a list of all genomes with a corresponding media table
    genomes_FAA = [os.path.splitext(file)[0] for file in os.listdir(GENOME_PATH) if file.endswith('.faa')]
    genomes_mediaTables = [os.path.splitext(file)[0] for file in os.listdir(MEDIADB_PATH) if file.endswith('.tsv')]
    genomes = list(set(genomes_FAA).intersection(genomes_mediaTables))
    for genome in genomes:
        # find the corresponding genome faa and media table for each organism
        genome_dir = GENOME_PATH + genome + ".faa"
        
        # generate gapfilled model
        mediadb_dir = MEDIADB_PATH + genome + ".tsv"
        gf_media_list = generateMediaList(mediadb_dir)
        output_dir = "data/models/" + genome + "_gf.xml"
        cmd = compileCommand(genome_dir, gf_media_list, mediadb_dir, output_dir)
        # run carve
        subprocess.run(cmd)

        # generate non-gapfilled model
        output_dir = "data/models/" + genome + "_ngf.xml"
        cmd = compileCommandNoGapfill(genome_dir, output_dir)
        # run carve
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
