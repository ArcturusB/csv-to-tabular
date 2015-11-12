#!/bin/python

import csv
import re
import os.path

def read_csv(filename):
    pass

class Tex_src:
    
    tab_row_sep = "\\hline\n"
    tab_row_end = "\t\\\\\n"

    def __init__(self):
        pass

    def begin_tabular(self, out_format):
        return "\\begin{tabular}{"+out_format+"}\n"

    def end_tabular(self):
        return "\\end{tabular}\n"

    def tabular_complete_row(self, row):
        return row.rstrip('\t& ') + '\t\\\\\n'

    def tabular_row(self, cells):
        return "\t& ".join(cells) + self_row_end

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
        "t": (lambda t, *args: t, 1),
        "n": (Tex_src.num, 1),
        "nu": (Tex_src.SI, 2),
        "ne": (Tex_src.num_err, 2),
        "neu": (Tex_src.SI_err, 3),
        }
    format_row = list(format_row)
    in_format = []
    last = {
        'n': -3,
        'e': -3,
        'u': -3,
        }
    # format_row = 
    for i,f in enumerate(format_row):
        try:
            last[f] = i
        except IndexError:
            pass
        if f == "u":
            if i-last["n"] == 1:
                in_format.append('nu')
            elif i-last["n"] == 2 and i-last["e"] == 1:
                in_format.append('neu')
        else:
            if i-last["n"] == 2:
                if i-last["e"] == 1:
                    in_format.append('ne')
                else:
                    in_format.append('n')
            else:
                in_format.append(format_row[i-2])
    return in_format
    # FIXME: this does not work!
    
re_in = re.compile("%in:% ?(.*)")
re_out = re.compile("%out:% ?(.*)")
re_hline = re.compile("%hline%")

if __name__ == '__main__':

    filename = 'tests/calib_test.csv'

    tex_data = []
    out_format = ""
    f = open(filename, newline='')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in csv_reader:
        print(row)
        if re_in.match(row[0]):
            in_format = (
                re_in.match(row[0]).group(1),
                *(cell.strip(' ') for cell in row[1:])
                )
            print(in_format)
            print(process_in_format(in_format))
        elif re_out.match(row[0]):
            out_format = re_out.match(row[0]).group(1)
            print(out_format)
        elif re_hline.match(row[0]):
            tex_data += [Tex_src.tab_row_sep]

    f.close()
