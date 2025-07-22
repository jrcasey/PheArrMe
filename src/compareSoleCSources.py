import pandas
import sys

# Import tsv files with sole C sources for Devosia, Marinobacter and Alcanivorax
devosia_df = pandas.read_csv('data/phearr/soleC_lists/PTEAB7WZ.1.tsv', sep='\t')
marinobacter_df = pandas.read_csv('data/phearr/soleC_lists/PT3-2.1.tsv', sep='\t')
alcanivorax_df = pandas.read_csv('data/phearr/soleC_lists/EA2.1.tsv', sep='\t')

# Find the intersection between each pair of strains
devosia_marinobacter_intersection = set(devosia_df).intersection(set(marinobacter_df))
devosia_alcanivorax_intersection = set(devosia_df).intersection(set(alcanivorax_df))
marinobacter_alcanivorax_intersection = set(marinobacter_df).intersection(set(alcanivorax_df))

# Find the subset in each strain that is not present in the other strains
devosia_unique = set(devosia_df) - (set(marinobacter_df) | set(alcanivorax_df))
marinobacter_unique = set(marinobacter_df) - (set(devosia_df) | set(alcanivorax_df))
alcanivorax_unique = set(alcanivorax_df) - (set(devosia_df) | set(marinobacter_df))

print("Unique to Devosia:", devosia_unique)
print("Unique to Marinobacter:", marinobacter_unique)
print("Unique to Alcanivorax:", alcanivorax_unique)

# Print the results
print("Intersection between Devosia and Marinobacter:", devosia_marinobacter_intersection)
print("Intersection between Devosia and Alcanivorax:", devosia_alcanivorax_intersection)
print("Intersection between Marinobacter and Alcanivorax:", marinobacter_alcanivorax_intersection)