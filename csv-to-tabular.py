#!/bin/python

import csv
import re
import os.path

class Tex_Src:
    
    tab_col_sep = "\t& "
    tab_row_sep = "\\hline"
    tab_row_end = "\t\\\\"

    def begin_tabular(out_format):
        return "\\begin{tabular}{"+out_format+"}"

    def end_tabular():
        return "\\end{tabular}"

    def tabular_row(cells):
        return Tex_Src.tab_col_sep.join(cells) + Tex_Src.tab_row_end

    def text(text, *args):
        """ Dummy function used in `process_in_format` """
        return text

    def num(num):
        return "\\num{"+num+"}"

    def SI(num, unit):
        return "\\SI{"+num+"}{"+err+"}"

    def num_err(num, err):
        return "\\num{"+num+" \\pm "+err+"}"

    def SI_err(num, err, unit):
        return '\\SI{'+num+' \\pm '+err+'}{'+content+'}'

class Csv_to_Tabular:
    
    re_in_line = re.compile("%in:% ?(.*)")
    re_out_line = re.compile("%out:% ?(.*)")
    re_hline = re.compile("%hline%")
    re_in_format = re.compile(
        "(?:(t)(-+)?)|(?:n(?!u|(?:eu?)))|(?:nu)|(?:ne(?!u))|(?:neu)")
    # (t[-]+)|(n)|(nu)|(ne)|(neu)
    # simple patterns (ie n, nu, ne, neu) are returned in group 0
    # for tricky patterns (ie t-+) group 1 contains the key for functions dict in
    # process_in_format and group 2 contains the dashes (nargs-1 of the function)

    functions = {
        "t": (Tex_Src.text, 1),
        "n": (Tex_Src.num, 1),
        "nu": (Tex_Src.SI, 2),
        "ne": (Tex_Src.num_err, 2),
        "neu": (Tex_Src.SI_err, 3),
        }
    # in `functions`, simple pattern entries (n, nu, ne, neu) contain tuples (function,
    # nargs), while tricky patterns entries (t-+) contain only functions. 

    # Rules:
    # First row *may* be a %out:% lllll (any tabular format comprehensible by TeX).
    # Default out format: left-aligned, with as many columns as in the 1st row.
    # Any row *may* be a *in:* format, where each column contains one of t, n,
    # nu, ne, neu or -.
    # All following rows (until next %in:%) must follow this formatting.

    def process_in_format(format_row):
        """ Take a format row and return the list of tuples (func, nargs) to
        format the following rows.
        """ 
        in_format_string = "".join((
            Csv_to_Tabular.re_in_line.match(format_row[0]).group(1),
            *(cell.strip(' ') for cell in format_row[1:])
            ))
        in_format = []
        for chunk in Csv_to_Tabular.re_in_format.finditer(in_format_string):
            try:
                in_format.append(Csv_to_Tabular.functions[chunk.group(0)])
            except KeyError:
                in_format.append((
                    Csv_to_Tabular.functions[chunk.group(1)][0], 
                    len(chunk.group(2)) + 1))
        return in_format
    
    def csv_to_tabular(filename):
        tex_data = []
        out_format = None
        in_format = None
        f = open(filename, newline='')
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        for row_num, row in enumerate(csv_reader):
            if row_num == 0:
                # only accept out format in 1st row
                if Csv_to_Tabular.re_out_line.match(row[0]):
                    out_format = Csv_to_Tabular.re_out_line.match(row[0]).group(1)
                    continue
                else:
                    # fallback to (number of output columns) * "l". based on 1st
                    # line, and avoid being fooled by "in format" lines
                    if Csv_to_Tabular.re_in_line.match(row[0]):
                        out_format = "l" * len(Csv_to_Tabular.process_in_format(row))
                    else:
                        out_format = "l" * len(row)
            if Csv_to_Tabular.re_in_line.match(row[0]):
                in_format = Csv_to_Tabular.process_in_format(row)
            elif Csv_to_Tabular.re_hline.match(row[0]):
                tex_data += [Tex_Src.tab_row_sep]
            else:
                if not in_format:
                    # fallback: assume everything is text ("t" format)
                    in_format = [(Tex_Src.text, 1)] * len(out_format)
                col_num = 0
                tex_row = []
                for (func, nargs) in in_format:
                    tex_row.append(func(*row[col_num:col_num+nargs]))
                    col_num += nargs
                tex_data += [Tex_Src.tabular_row(tex_row)]

        tex_data.insert(0, Tex_Src.begin_tabular(out_format))
        tex_data.append(Tex_Src.end_tabular())
        tex_data = "\n".join(tex_data)

        f.close()

        return tex_data


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument(
        "filename", 
        metavar="filename", 
        type=str, 
        default="",
        help='input CSV file')

    args=parser.parse_args()

    print(Csv_to_Tabular.csv_to_tabular(args.filename))
