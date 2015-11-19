#!/bin/python

import csv
import re
import os.path

def read_csv(filename):
    pass

class Tex_src:
    
    tab_col_sep = "\t& "
    tab_row_sep = "\\hline"
    tab_row_end = "\t\\\\"

    def __init__(self):
        pass

    def begin_tabular(self, out_format):
        return "\\begin{tabular}{"+out_format+"}"

    def end_tabular(self):
        return "\\end{tabular}"

    def tabular_row(self, cells):
        return self.tab_col_sep.join(cells) + self.tab_row_end

    def text(self, text, *args):
        """ Dummy function used in `process_in_format` """
        return text

    def num(self, num):
        return "\\num{"+num+"}"

    def SI(self, num, unit):
        return "\\SI{"+num+"}{"+err+"}"

    def num_err(self, num, err):
        return "\\num{"+num+" \\pm "+err+"}"

    def SI_err(self, num, err, unit):
        return '\\SI{'+num+' \\pm '+err+'}{'+content+'}'

def process_in_format(format_row):
    """ Take a format row and return the list of tuples (func, nargs) to
    format the following rows.
    """ 
    functions = {
        "t": (tex_src.text, 1),
        "n": (tex_src.num, 1),
        "nu": (tex_src.SI, 2),
        "ne": (tex_src.num_err, 2),
        "neu": (tex_src.SI_err, 3),
        }
    # in `functions`, simple pattern entries (n, nu, ne, neu) contain tuples (function,
    # nargs), while tricky patterns entries (t-+) contain only functions. 
    in_format_string = "".join((
        re_in_line.match(row[0]).group(1),
        *(cell.strip(' ') for cell in row[1:])
        ))
    in_format = []
    for chunk in re_in_format.finditer(in_format_string):
        try:
            in_format.append(functions[chunk.group(0)])
        except KeyError:
            in_format.append((functions[chunk.group(1)][0], len(chunk.group(2)) + 1))
    return in_format
    
re_in_line = re.compile("%in:% ?(.*)")
re_out_line = re.compile("%out:% ?(.*)")
re_hline = re.compile("%hline%")
re_in_format = re.compile(
    "(?:(t)(-+)?)|(?:n(?!u|(?:eu?)))|(?:nu)|(?:ne(?!u))|(?:neu)")
# (t[-]+)|(n)|(nu)|(ne)|(neu)
# simple patterns (ie n, nu, ne, neu) are returned in group 0
# for tricky patterns (ie t-+) group 1 contains the key for functions dict in
# process_in_format and group 2 contains the dashes (nargs-1 of the function)

# Rules:
# First row *may* be a %out:% lllll (any tabular format comprehensible by TeX).
# Default out format: left-aligned, with as many columns as in the 1st row.
# Any row *may* be a *in:* format, where each column contains one of t, n,
# nu, ne, neu or -.
# All following rows (until next %in:%) must follow this formatting.

if __name__ == '__main__':

    filename = 'tests/calib_test.csv'

    tex_data = []
    out_format = None
    in_format = None
    tex_src = Tex_src()
    f = open(filename, newline='')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    for row_num, row in enumerate(csv_reader):
        print("==>", row)
        if row_num == 0:
            # only accept out format in 1st row
            if re_out_line.match(row[0]):
                out_format = re_out_line.match(row[0]).group(1)
                continue
            else:
                # fallback to (number of output columns) * "l". based on 1st
                # line, and avoid being fooled by "in format" lines
                if re_in_line.match(row[0]):
                    out_format = "l" * len(process_in_format(row))
                else:
                    out_format = "l" * len(row)
        if re_in_line.match(row[0]):
            in_format = process_in_format(row)
        elif re_hline.match(row[0]):
            tex_data += [tex_src.tab_row_sep]
        else:
            msg = "Please insert a “%in:%” format row before any data in your CSV."
            assert in_format, msg
            col_num = 0
            tex_row = []
            for (func, nargs) in in_format:
                tex_row.append(func(*row[col_num:col_num+nargs]))
                col_num += nargs
            tex_data += [tex_src.tabular_row(tex_row)]

    tex_data.insert(0, tex_src.begin_tabular(out_format))
    tex_data.append(tex_src.end_tabular())
    tex_data = "\n".join(tex_data)
    print(tex_data)

    f.close()
