# PheArrPlots.py - generate plots of biolog data

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Housekeeping: convert extensions in PHEARRDIR to .tsv
def convertBiologExtensions(PHEARRDIR):
    for filename in os.listdir(PHEARRDIR):
        if filename.endswith('.txt'):
            os.rename(PHEARRDIR + filename, PHEARRDIR + filename[:-4] + '.tsv')

# parse strain name from filename
def parseStrainName(filename):
    strainName = filename.split("_PM")[0]
    return strainName

# load sole carbon source list
def loadSoleCList(SOLEC_LIST_DIR,strainName):
    soleC_list = pd.read_csv(SOLEC_LIST_DIR + strainName + '.tsv', sep='\t', header=None)
    soleC_list = soleC_list.iloc[0,:].astype(str).values.tolist() # Convert to list of strings
    # there shouldn't be nan's in the soleC_list, but just in case
    soleC_list = [x for x in soleC_list if str(x) != 'nan']
    return soleC_list

def loadBiologData(PHEARRDIR,filename):
    if filename.endswith('_PM1.tsv'):
        PM = pd.read_csv(PHEARRDIR + filename, sep='\t', header=0)
        PM = PM.drop(PM.index[0])
        
    elif filename.endswith('_PM2.tsv'):
        PM = pd.read_csv(PHEARRDIR + filename, sep='\t', header=0)
        PM = PM.drop(PM.index[0])
    else:
        print("Error: filename must end with '_PM1.tsv' or '_PM2.tsv'")
        return None
    
    # Convert columns to numeric
    PM = PM.apply(pd.to_numeric)
    
    return PM

# generate plots
def plotPM(PHEARRPLOTDIR,PM,filename,soleC_list):
    # vertical axes should all be the same, get the range of the data
    ymin = 0
    ymax = PM.iloc[:,2:].max().max()
    fig, ax = plt.subplots(8, 12, figsize=(60, 40))  # Create figure
    for i, column in enumerate(PM.columns[2:]):  # Iterate through all columns except the first (which is the well name) and the last (which is the strain name)
        # check if column is in soleC_list, if it is, plot it in red, otherwise plot it in blue
        if column in soleC_list:
            LineColor = 'red'     
        else:
            LineColor = 'blue'
        
        row = i // 12
        col = i % 12
        x = PM['Time'].to_numpy()
        y = PM[column].to_numpy()
        ax[row, col].plot(x,y, color=LineColor)  # Plot PM data
        ax[row, col].set_ylim([ymin,ymax])
        ax[row, col].set_xlabel('Time (hours)',fontsize=12)  # Set x-axis label
        ax[row, col].set_ylabel('OD600',fontsize=12)  # Set y-axis label
        ax[row, col].set_title(column,fontsize=12)  # Set title
        ax[row, col].plot(x,y, color=LineColor, linewidth=5.0)  # Plot PM data
        # make tick labels larger and show fewer ticks
        ax[row, col].tick_params(axis='both', which='major', labelsize=12)
        ax[row, col].locator_params(axis='x', nbins=5)
    fig.tight_layout()  # Make figure compact
    # Save figure
    filenamePrefix = filename.split(".tsv")[0]
    fig.savefig(PHEARRPLOTDIR + filenamePrefix + '.png')  # Save figure
    plt.close(fig)  # Close figure


# Main function - loop through all sole carbon lists and generate plots
def main():
    # Directories
    PHEARRDIR = 'data/phearr/plates/tsv/'
    PHEARRPLOTDIR = 'data/phearr/plots/'
    SOLEC_LIST_DIR = 'data/phearr/soleC_lists/'
    # Convert extensions in PHEARRDIR to .tsv
    convertBiologExtensions(PHEARRDIR)
    # Loop through all files in PHEARRDIR
    for filename in os.listdir(PHEARRDIR):
        if filename.endswith('_PM1.tsv') or filename.endswith('_PM2.tsv'): # only process files that end with '_PM1.tsv' or '_PM2.tsv'
            strainName = parseStrainName(filename) # parse strain name from filename
            soleC_list = loadSoleCList(SOLEC_LIST_DIR,strainName) # load sole carbon source list
            PM = loadBiologData(PHEARRDIR,filename) # load biolog data
            plotPM(PHEARRPLOTDIR,PM,filename,soleC_list) # generate plots

if __name__ == "__main__":
    main()