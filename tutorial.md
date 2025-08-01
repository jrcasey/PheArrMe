# Tutorial Slides

### Description
PheArrMe automates the workflow from phenotype array data to draft genome-scale metabolic network reconstruction. The script takes raw absorbance time-series data from a platereader, generates a list of sole carbon sources for each strain and sets everything up to run CarveMe to generate draft GEMs for each of your collection of strains. Finally, it generates a summary table for each gapfilled model. 



---

# Installation

### Clone from GH
- Clone `git clone git@github.com:jrcasey/PheArrMe.git`
- Switch to `dev` branch `git checkout dev` and pull `git pull origin dev`

### Requirements
- CPLEX Studio (Instructions below)
- A conda environment (called PheArrMe) is included `environment.yml`.  Create this environment `conda env create -f environment.yml` and then switch to the PheArrMe environment `conda activate PheArrMe`
- In my experience, the pip packages don't always install, so you may need to do those manually. They are:
	- carveme
	- biopython
	- cplex (see below)
	- cobra

---

## Setting up the conda env
1. Create a new environment with no packages `conda create -n PheArrMe` 
2. Activate `conda activate PheArrMe`
3. (If conda dist is arm, do this:) Change the subdir variable to be osx-64 `conda config --env --set subdir osx-64`
4. Install python 3.8 `conda install python=3.8`
5. Install CPLEX `python /Applications/CPLEX_Studio2211/python/setup.py install`
6. Install DIAMOND `conda install -c bioconda diamond`
7. Verify that pip is in the env list
8. Install cobra `pip install cobra`
9. Install CarveMe `pip install carveme` !!! Currently, version 1.6.0 has solver issues. Use 1.5.2 instead until a fix `pip install --force-reinstall -v "carveme==1.5.2"`
10. Install pandas, numpy, and matplotlib `conda install pandas numpy matplotlib`
11. Install biopython `pip install biopython`
12. Install SMETANA `pip install smetana`

---

## Inputs
- Protein multifasta (.faa) files for each strain in `data/genomes/faa/`. I've included a script to convert from GenBank format (.gbk), which can be deposited in `data/genomes/gbk/` [link to dir](data/genomes/gbk/). 
- One of the following:
 	- A tab-separated list of sole carbon sources for each strain in `data/phearr/soleC_lists/` [link to dir](data/phearr/soleC_lists/). Substrate names should match the biolog ID's. The filename should match the genome filename, but with extension .tsv.
 	- A a tab-separated biolog table. The filename format should be `<genome>_PM#.tsv`, where `genome` is the filename of genome for the corresponding strain, and `#` is the plate number (e.g., `_PM2.tsv`. The format and column headers can be found [here](docs/examples/exampleBiologData.tsv).
 	 	- WARNING: If you're exporting a tsv from excel, make sure that it doesn't copy over double-quotes in the column headers. This is weird excel behavior that is difficult to detect and will result in omission of the corresponding substrates from gapfilling.

---

# Libraries
- A base medium composition `data/phearr/baseMedium.tsv` [link to file](data/phearr/baseMedium.tsv). A table of all components of the media without a carbon source. This is used to build the media tables. You are encouraged to take a look at this composition and edit as necessary (make sure to use BiGG ID's for metabolites - search for them [here](http://bigg.ucsd.edu/)).  
- A map from substrate ID's to BiGG ID'. In our case, we used Biolog plates so we include the mapping from Biolog to BiGG `data/phearr/mapping_Biolog_BiGG.tsv` [link to file](data/phearr/mapping_Biolog_BiGG.tsv). If you are using a different phenotype array format, you will need to change this mapping file to match your substrate ID's. 

---

## Outputs
- Optional: protein sequences in .faa files `data/genomes/faa/` [link to dir](data/genomes/faa/) either deposited by the user or generated with `downloadNCBI.py` [link to file](src/downloadNCBI.py).
- Combined media tables formatted for CarveMe in `data/phearr/mediaTables/` [link to dir](data/phearr/mediaTables/)
- Gap-filled draft GEM's `data/models/` [link to dir](data/models/). These will retain the strain name and will be stored in sbml format (.xml)
- Model summary tables, including model size and gapfilling details `data/tables/` [link to dir](data/tables/)

---

## Modules
- `src/downloadNCBI.py` [link to file](src/downloadNCBI.py) Download a .gbk genome file for any organism, saved to `data/genomes/gbk/`
- `src/convert_GBKtoFAA.py` [link to file](src/convert_GBKtoFAA.py) Convert .gbk format to .faa, saved to `data/genomes/faa/`
- `src/processPheArr.py` [link to file](src/processPheArr.py) Determines which substrates are sole carbon sources for each strain from biolog plots.
- `src/PheArrPlots.py` [link to file](src/PheArrPlots.py) Generates plots of the absorbance time series for all substrates, for each plate, for each strain. Substrates identified in `processPheArr.py` as sole carbon sources are colored red, no-growth substrates are colored blue.  
- `src/generateMedia.py` [link to file](src/generateMedia.py) Create a concatenated table of all media, saved to `data/biolog/mediaTables/`
- `src/runCarveBatch.py` [link to file](src/runCarveBatch.py) Execute CarveMe for each strain, generates a gapfilled draft GEM and saves to `data/models/`. (planned: also generate a non-gapfilled model)
- `src/analyzeGapfilling.py` [link to file](src/analyzeGapfilling.py) Generates a table summarizing the gapfilled models, including number of genes, reactions, metabolites, gapfilled reactions, and a list of which reactions were added. This is output to `data/tables/modelDescriptions.tsv`[link to file](data/tables/modelDescriptions.tsv)

---

## Tests
- `test/screenSubstrates.py` [link to file](test/screenSubstrates.py) Checks through all Biolog substrates for ones that are problematic for CarveMe gapfilling. Dumps an error log to the `test/` directory `test/error.log` [link to file](test/error.log). I've provided a quick one-liner shell script to return a list of problem media ID's from this error log. I then manually added a boolean 'false' to any problem substrates in the mapping file `data/phearr/mapping_Biolog_BiGG.tsv`


## Usage
Currently, BiologMe is run with `python PheArrMe.py` [link to file](PheArrMe.py), or you can run a a subset of modules in the order given above.  

I started a dev branch to implement a CLI and package the code using either setuptools or conda. Planned arguments and options (in no particular order): 

- method for determining growth/no-growth
- run PheArrMe with just an NCBI organism ID
- run PheArrMe with no raw biolog data, just a list of known sole C substrates
- option to re-run a gapfill if it fails due to a problematic substrate (by eliminating that substrate). Continue until gapfill completes.
- more to come

---

## CPLEX Studio installation guide
1. Get an academic license through [here](https://academic.ibm.com/a2mt/email-auth)
2. Navigate to 'Data Science' then 'Software' then 'ILOG CPLEX Optimization Studio' then 'Downloads' then 'IBM ILOG CPLEX Optimization Studio V22.1.1 for OSX ARM64' (or whatever version it currently is). Start the download... it will fail because you need to:
3. Download an installer. Do this and then you can launch the installer to actually:
4. Download the right CPLEX (using the ARM architecture again)
5. Follow the instructions. When done:
6. Switch to the `BiologMe` environment. Run the python script `python /Applications/CPLEX_Studio2211/python/setup.py install` (or whatever version you're using). 