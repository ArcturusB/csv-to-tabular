csv-to-tabular
==============
> A Python script to create TeX tabulars from CSV data.

## Usage

To use this script, simply call it from the command line with the CSV file you
want to convert as its only argument:

	./csv-to-tabular.py my_cool_data.csv

The CSV file may contain additional formatting instructions in special rows
that start with either “%in:%” or “%out:%”. The “in” format specifies how data
should be read in the CSV, while the “out” format specifies how it should be
rendered in TeX.

### In format

**In** format rows start with the special string “%in:%” and each of its cells
contains a letter which specifies the *meaning* of the data type.

    letter | meaning     
   --------+----------------
    t      | text
    n      | number
    e      | standard error
    u      | unit
    -      | skip this row
   --------+----------------

This allows a clearer representation of the data TeX: unit 


### Out format

**Out** format rows may contain only one cell, containing the special string
“%out:%” followed by the column format argument for the tabular environment.
Example:

> %out:% r|lll|

### Real-life example

> %out:% lllll
> %in:%     t, t, t,-, t,-, t,-
> Element,          Energy (keV),   Event count     , 
> %hline%
> %in:% t,          n,              n,              , e
> \ce{^{137}Cs},    661.659,
> \ce{^{60}Co},     1173.24,
> \ce{^{60}Co},     1332.508,
> \ce{^{22}Na},     511,
> \ce{^{22}Na},     1274.577,


## Help!
For some quick help, you can type in your terminal:

	./csv-to-tabular.py --help

## TODO
- `argparse` help

## License
csv-to-tabular.py
Copyright (C) 2015  Gabriel Pelouze

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
