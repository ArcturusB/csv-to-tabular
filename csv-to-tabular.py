#!/bin/python

import csv
import os.path

def read_csv(filename):
	array = []
	with open(filename, newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in csvreader:
			array += [row]
	return array

def process_in_format(in_format_str):
	'''
	Formats: 
		t
		n
		nu
		ne
		neu
	'''
	in_format_array = []
	i=0
	while i<len(in_format_str):
		skip = 1
		if in_format_str[i] is 't':
			in_format_array.append(in_format_str[i])
		elif in_format_str[i] is 'n':
			try:
				if in_format_str[i+1] is 'u':
					in_format_array.append(in_format_str[i:i+2])
					skip += 1
				elif in_format_str[i+1] is 'e':
					try:
						if in_format_str[i+2] is 'u':
							in_format_array.append(in_format_str[i:i+3])
							skip += 2
						else:
							in_format_array.append(in_format_str[i:i+2])
							skip += 1
					except IndexError: # format string ends with 'ne'
						in_format_array.append(in_format_str[i:i+2])
						skip += 1
				else:
					in_format_array.append(in_format_str[i])
			except IndexError: # format string ends with 'n'
				in_format_array.append(in_format_str[i])
		else: 
			raise FormatStringError('Invalid input format string.')
		i += skip
	return in_format_array


class FormatStringError(Exception):
	pass

class Tex_src:
	def __init__(self):
		pass

	def begin_tabular(self,out_format):
		return '\\begin{tabular}{'+out_format+'}\n'

	def end_tabular(self):
		return '\\end{tabular}\n'

	def tabular_complete_row(self,row):
		return row.rstrip('\t& ') + '\t\\\\\n'

	def tabular_cell(self,in_format,content):
		'''
		Formats:
		t
		n
		nu
		ne
		neu
		'''
		# # Elegent but can raise IndexError
		# cell_content = {
			# 't':	content,
			# 'n':	'\\num{'+content+'}',
			# 'nu':	'\\SI{'+content[0]+'}{'+content[1]+'}',
			# 'ne':	'\\num{'+content[0]+' \\pm '+content[1]+'}',
			# # 'ne':	'\\num{'+content[0]+'}\\pm\\num{'+content[1]+'}',
			# 'neu':	'\\SI{'+content[0]+' \\pm '+content[1]+'}{'+content[2]+'}'}
		# # then use cell_content[in_format]
		if in_format == 't':
			cell_content = content[0]
		elif in_format == 'n':
			cell_content = '\\num{'+content[0]+'}'
		elif in_format == 'nu':
			cell_content = '\\SI{'+content[0]+'}{'+content[1]+'}'
		elif in_format == 'ne':
			cell_content = '\\num{'+content[0]+' \\pm '+content[1]+'}'
		elif in_format == 'neu':
			cell_content = '\\SI{'+content[0]+' \\pm '+content[1]+'}{'+content[2]+'}'
		else:
			cell_content = ''
		cell_begin	= ''
		cell_end	= '\t& '
		return cell_begin + cell_content + cell_end

	def tabular_row_sep(self,n_rows=1):
		return n_rows*'\\hline'+'\n'

def process_row(row, in_format):
	tex = Tex_src()
	tex_string = ''
	format_index = 0
	offset = 0
	for cell_format in in_format:
		tex_string += tex.tabular_cell(cell_format, row[offset:len(cell_format)+offset])
		offset += len(cell_format)
	return tex.tabular_complete_row(tex_string)

def process_csv(csv_array, in_format, label_rows, Label=False):
	tex_string = ''

	if Label:
		for row in csv_array[:label_rows]:
			tex_string += process_row(row, in_format)
	else:
		for row in csv_array[label_rows:]:
			tex_string += process_row(row, in_format)

	return tex_string

def csv_to_tex( csv_filename,\
				tex_filename='',\
				label_rows=1,\
				in_format_label='',\
				out_format_label='',\
				in_format_content='',\
				out_format_content='',\
				label_content_rows_sep=2,\
				Verbose=False,\
				):

	# open csv
	csv_array = read_csv(csv_filename)

	tex=Tex_src()

	# remove '' cells
	for i in range(len(csv_array)):
		row = csv_array.pop(i)
		row = list(filter(('').__ne__, row))
		csv_array.insert(i,row)

	if csv_array[0][0] == 'in format':
		in_format_label = csv_array[0][1]
		in_format_content = csv_array[0][2]
		csv_array.remove(csv_array[0])
	if csv_array[0][0] == 'out format':
		in_format_label = csv_array[0][1]
		in_format_content = csv_array[0][2]
		csv_array.remove(csv_array[0])


	# generate arguments:
	if tex_filename == '': # simply change ext
		tex_filename = os.path.splitext(csv_filename)[0]+'.tex'
	# TODO: automatically determine label lines
	if in_format_label == '': # assume we have simple text
		in_format_label = 't'*len(csv_array[0])
	if out_format_label == '':
		out_format_label = 'l'*(len(csv_array[0])-csv_array[0].count(''))
	if in_format_content == '': # same as label
		in_format_content = in_format_label
	if out_format_content == '':
		out_format_content = out_format_label

	# process in_format*
	in_format_label = process_in_format(in_format_label)
	in_format_content = process_in_format(in_format_content)

	try: 
		assert len(in_format_content) is len(in_format_label)
		assert len(out_format_content) is len(out_format_label)
		assert len(in_format_content) is len(out_format_content)
	except AssertionError:
		raise FormatStringError('All four format strings must have the same length. (For now!)')

	tex_string = tex.begin_tabular(out_format_content)
	tex_string += process_csv(csv_array, in_format_label, label_rows, Label=True)
	tex_string += tex.tabular_row_sep(label_content_rows_sep)
	tex_string += process_csv(csv_array, in_format_content, label_rows)
	tex_string += tex.end_tabular()

	if Verbose:
		print(tex_string)

	tex_file = open(tex_filename,'w')
	tex_file.write(tex_string)
	tex_file.close()

if __name__ == '__main__':

	import argparse
	parser = argparse.ArgumentParser(description='Parses a CSV file and transforms it into a TeX tabular environment. First and second lines of the CSV may contain : in format,LABEL IN FORMAT,CONTENT IN FORMAT; out format,LABEL OUT FORMAT,CONTENT OUT FORMAT')
	# FIXME
	parser.add_argument('csv_filename', metavar='csv_filename', type=str, 
						default='',
						help='Filename of the CSV file to parse')
	parser.add_argument('-t', '--tex_filename', metavar='tex_filename', type=str, 
						default='',
						help='Filename of the TeX file to write the result to')
	parser.add_argument('-L', '--label_rows', metavar='label_rows', type=int, 
						default=1,
						help='Number of label rows in the beginning of the tabular')
	parser.add_argument('-IL', '--in_format_label', metavar='in_format_label', type=str, 
						default='',
						help='In format of label rows. Possible formats are t, n, ne, nu, neu for text, number, number±error, number~unit, number±error~unit')
	parser.add_argument('-IC', '--in_format_content', metavar='in_format_content', 
						type=str, 
						default='',
						help='In format of content rows')
	parser.add_argument('-OL', '--out_format_label', metavar='out_format_label', type=str, 
						default='',
						help='Out format of content rows. This is a TeX argument.')
	parser.add_argument('-OC', '--out_format_content', metavar='out_format_content', 
						type=str, 
						default='',
						help='In format of content rows')
	parser.add_argument('-S', '--label_content_rows_sep', metavar='label_content_rows_sep', 
						type=int, 
						default=2,
						help='Number of \hlines used to separate label from content')
	parser.add_argument('-v', '--verbose', dest='Verbose', action='store_true',
						default=False,
						help='Verbose')
	args=parser.parse_args()

	csv_to_tex( args.csv_filename,\
				args.tex_filename,\
				args.label_rows,\
				args.in_format_label,\
				args.out_format_label,\
				args.in_format_content,\
				args.out_format_content,\
				args.label_content_rows_sep,\
				args.Verbose,\
				)
