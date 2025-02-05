#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose
-------

This module removes a set of loci from results of the
AlleleCall process.

Code documentation
------------------
"""


import csv

import pandas as pd

try:
	from utils import file_operations as fo
except ModuleNotFoundError:
	from CHEWBBACA.utils import file_operations as fo


def main(input_file, genes_list, output_file, inverse):
	"""Remove loci from allele calling results.

	Parameters
	----------
	input_file : str
		Path to a TSV file that contains allelic profiles
		determined by the AlleleCall module.
	genes_list : str
		Path to a file with a list of loci to keep or remove.
	output_file : str
		Path to the output file.
	inverse : bool
		Keep the loci included in `genes_list` and remove the
		rest instead.
	"""
	# Read genes list
	with open(genes_list, 'r') as infile:
		genes_list = list(csv.reader(infile, delimiter='\t'))
		genes_list = [g[0] for g in genes_list]

	# Get list of loci in allele call results
	loci = fo.read_lines(input_file, strip=True, num_lines=1)
	loci = loci[0].split('\t')[1:]
	print('Total loci: {0}'.format(len(loci)))

	if inverse is True:
		columns_to_keep = [g for g in loci if g in genes_list]
	else:
		columns_to_keep = [g for g in loci if g not in genes_list]

	columns_to_remove = (len(loci)) - len(columns_to_keep)
	print('Loci to remove: {0}'.format(columns_to_remove))

	# Include first column with sample ids
	columns_to_keep = ['FILE'] + columns_to_keep
	df = pd.read_csv(input_file, usecols=columns_to_keep,
					 sep='\t', dtype=str)

	# Save dataframe to file
	df.to_csv(output_file, header=True, sep='\t', index=False)

