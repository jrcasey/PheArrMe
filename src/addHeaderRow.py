import pandas as pd
import os

# This script adds a header row to csv file, saves as tab delimited file

# import mapping files for PM1 and PM2
headerMap_PM1 = pd.read_csv("data/phearr/HeaderMap_PM1.txt", sep="\t", header=None)
headerMap_PM2 = pd.read_csv("data/phearr/HeaderMap_PM2.txt", sep="\t", header=None)

# get the first column of each mapping file
header_PM1 = headerMap_PM1[0].tolist()
header_PM2 = headerMap_PM2[0].tolist()

# load a csv file, add the header row, and save as tab delimited file
def addHeaderRow(file, header):
    df = pd.read_csv(file, sep=",", header=None)
    df.columns = header
    return df

# get the list of files in the data/phearr directory
files = os.listdir("data/phearr/temp/biolog_v1_merged/formatted")

# loop through the files and add the header row
for file in files:
    if file.endswith(".csv"):
    # check if the file contains PM1 or PM2
        if "PM1" in file:
            df = addHeaderRow("data/phearr/temp/biolog_v1_merged/formatted/" + file, header_PM1)
            # save the file as a tab delimited file to data/biolog/temp/biolog_v1_merged/formatted2/ keeping the file name but changing the extension to .tsv
            df.to_csv("data/phearr/temp/biolog_v1_merged/formatted2/" + file[:-4] + ".tsv", sep="\t", index=False)
        elif "PM2" in file:
            df = addHeaderRow("data/phearr/temp/biolog_v1_merged/formatted/" + file, header_PM2)
            # save the file as a tab delimited file to data/biolog/temp/biolog_v1_merged/formatted2/ keeping the file name but changing the extension to .tsv
            df.to_csv("data/phearr/temp/biolog_v1_merged/formatted2/" + file[:-4] + ".tsv", sep="\t", index=False)
        else:
            print("Error: file name does not contain PM1 or PM2")
