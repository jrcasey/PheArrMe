from Bio import Entrez
from Bio import SeqIO

import os

outdir = "~/data/genomes/NCBI/"
os.makedirs(outdir, exist_ok=True)

Entrez.email = "jrcasey@hawaii.edu"
Entrez.tool = "Biopython_NCBI_Entrez_downloads.ipynb"


handle = Entrez.esearch(db="assembly", term="GCF_003201775", retmax=100)
record = Entrez.read(handle)

