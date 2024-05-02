from Bio import SeqIO
import os

def convert_GBKtoFAA(gbk_filename, faa_filename):
    input_handle  = open(gbk_filename, "r")
    output_handle = open(faa_filename, "w")
    for seq_record in SeqIO.parse(input_handle, "genbank") :
        print("Dealing with GenBank record %s" % seq_record.id)
        for seq_feature in seq_record.features :
            if seq_feature.type=="CDS" :
                assert len(seq_feature.qualifiers['translation'])==1
                output_handle.write(">%s from %s\n%s\n" % (
                       seq_feature.qualifiers['locus_tag'][0],
                       seq_record.name,
                       seq_feature.qualifiers['translation'][0]))
    input_handle.close()
    output_handle.close()

def main():
    for filename in os.listdir("data/genomes/gbk/"):
        if filename.endswith(".gbk"):
            gbk_filename = "data/genomes/gbk/" + filename
            faa_filename = "data/genomes/faa/" + filename[:-4] + ".faa"
            convert_GBKtoFAA(gbk_filename, faa_filename)

if __name__ == "__main__":
    main()