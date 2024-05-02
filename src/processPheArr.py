import pandas as pd
import os


# load phenotype array data
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

# Get PM columns min, max, range, min indices, and max indices
def getMinMaxRange(PM):
    PMmin = PM.iloc[:,3:].min()
    PMmax = PM.iloc[:,3:].max()
    PMrange = PMmax - PMmin
    PMminIndices = PM.iloc[:,3:].idxmin()
    PMmaxIndices = PM.iloc[:,3:].idxmax()
    return PMrange, PMminIndices, PMmaxIndices

# Get PM negative control range and standard deviation
def getPMNegativeControl(PM):
    PMneg = PM['Negative Control']
    PMnegRange = PMneg.max() - PMneg.min()
    PMnegStd = PMneg.std()
    return PMnegRange, PMnegStd

# Assign positive growth to carbon sources with ranges that are above 3 standard deviations of the negative control. Min indices should also occur before max indices.
def assignPositiveGrowth(PMrange, PMminIndices, PMmaxIndices, PMnegRange, PMnegStd):
    # method 1: positive growth if range is above 3 standard deviations of the negative control
    #PMpos = PMrange > (PMnegRange + 3*PMnegStd)
    # method 2: positive growth if range is 2 times the negative control range
    PMpos = PMrange > 2*PMnegRange
    # additional condition: min indices should occur before max indices
    PMpos = PMpos & (PMminIndices < PMmaxIndices)
    return PMpos

# build a list of carbon sources that are positive for growth
def buildPositiveGrowthList(PMpos,PM):
    PMposList = []
    for i, column in enumerate(PM.columns[3:]):
        if PMpos[i]:
            PMposList.append(column)
    return PMposList

# save list to tab-delimited file with the same name as filename1
def savePositiveGrowthList(PHEARRSOLECDIR,PMposList,filename1):
    filenamePrefix = filename1.split(".tsv")[0]
    with open(PHEARRSOLECDIR + filenamePrefix + '.tsv', 'w') as f1:
        for item in PMposList:
            f1.write("%s\t" % item)

# find any files with the same strain name that have both _PM1 and _PM2 files, and merge them into one file. Then write to a new tsv file with the same name as the strain name.
def mergePMFiles(PHEARRSOLECDIR):
    for filename1 in os.listdir(PHEARRSOLECDIR):
        if filename1.endswith('_PM1.tsv'):
            filenamePrefix = filename1.split("_PM1.tsv")[0]
            filename2 = filenamePrefix + '_PM2.tsv'
            if os.path.exists(PHEARRSOLECDIR + filename2):
                with open(PHEARRSOLECDIR + filename1, 'r') as f1:
                    PM1 = f1.read().splitlines()
                with open(PHEARRSOLECDIR + filename2, 'r') as f2:
                    PM2 = f2.read().splitlines()
                PM = list(set(PM1) | set(PM2))
                with open(PHEARRSOLECDIR + filenamePrefix + '.tsv', 'w') as f3:
                    for item in PM:
                        f3.write("%s\t" % item)

# clean up the _PM1 and _PM2 files
def cleanUpPMFiles(PHEARRSOLECDIR):
    for filename1 in os.listdir(PHEARRSOLECDIR):
        if filename1.endswith('_PM1.tsv') or filename1.endswith('_PM2.tsv'):
            os.remove(PHEARRSOLECDIR + filename1)

# main function
def main():
    # Directories
    PHEARRDIR = 'data/phearr/plates/tsv/'
    PHEARRSOLECDIR = 'data/phearr/soleC_lists/'
    # loop through all files in PHEARRDIR
    for filename1 in os.listdir(PHEARRDIR):
        if filename1.endswith('.tsv'):
            PM = loadBiologData(PHEARRDIR,filename1)
            PMrange, PMminIndices, PMmaxIndices = getMinMaxRange(PM)
            PMnegRange, PMnegStd = getPMNegativeControl(PM)
            PMpos = assignPositiveGrowth(PMrange, PMminIndices, PMmaxIndices, PMnegRange, PMnegStd)
            PMposList = buildPositiveGrowthList(PMpos,PM)
            savePositiveGrowthList(PHEARRSOLECDIR,PMposList,filename1)
    mergePMFiles(PHEARRSOLECDIR)
    cleanUpPMFiles(PHEARRSOLECDIR)

if __name__ == "__main__":
    main()

