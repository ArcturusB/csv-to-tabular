csv-to-tabular
==============
An script to create LaTeX tabulars from CSV data, with easy units and
uncertainties handling.

This script relies on the `siunitx` package to display numbers and
uncertainties. 

## Usage

To use this script, simply call it from the command line with the CSV file you
want to convert as its only argument:

	./csv-to-tabular.py my_cool_data.csv

The CSV file may contain additional formatting instructions in special rows
that start with either `%in:%` or `%out:%`. The “in” format specifies how data
should be read in the CSV, while the “out” format specifies how it should be
rendered in TeX.

Finally, one or several solid horizontal lines may be inserted in the tabular
by adding to the CSV a row that contains only a `%hline%` string.

### In format

**In** format rows start with the special string `%in:%` and each of its cells
contains a letter which specifies the *meaning* of the data type.

    letter | meaning     
   --------+----------------
    t      | text
    m      | math
    n      | number
    e      | standard error
    u      | unit
    -      | skip this row

This allows a clearer representation of the data in TeX tabular environments by
gathering values, uncertainties and units in the same column, if appropriate.
For example, a `n,e,u` column sequence in the CSV will be merged in a single
row where elements formatted as `\num{n}\pm\num{e}\si{u}`. `n,e` would be as
well merged in a single column. 

Note that the first cell of this format line must contain both the special
string `%in:%` and the format for the first column. 

You may use several input format rows in your file. This can help, for
instance, to implement different formats for the header, body and footer of a
table. 


### Out format

The **Out** format row may only appear on the first row of the CSV file. It is
composed of only one cell that contains the special string `%out:%` followed by
the column format argument for the tabular environment.  Example:

    %out:% r|lll|

### Real-life example

CSV input:

    %out:% l|ll
    %in:% t           , t             , t             , -
    Element           , Energy (keV)  , Event count   ,  
    %hline%
    %in:% t           , n             , n             , e
    \ce{^{137}Cs}     , 661.659       , 45.4e6        , 2.4e5
    \ce{^{60}Co}      , 1173.24       , 20.8e6        , 2.5e5
    \ce{^{60}Co}      , 1332.508      , 17.3e6        , 2.0e5
    \ce{^{22}Na}      , 511           , 62.8e6        , 4.2e5
    \ce{^{22}Na}      , 1274.577      , 13.8e6        , 2.3e5

TeX output:

    \begin{tabular}{l|ll}
    Element        &  Energy (keV)     &  Event count   \\
    \hline
    \ce{^{137}Cs}  & \num{ 661.659  }  & \num{ 45.4e6 }$\pm$\num{ 2.4e5 } \\
    \ce{^{60}Co}   & \num{ 1173.24  }  & \num{ 20.8e6 }$\pm$\num{ 2.5e5 } \\
    \ce{^{60}Co}   & \num{ 1332.508 }  & \num{ 17.3e6 }$\pm$\num{ 2.0e5 } \\
    \ce{^{22}Na}   & \num{ 511      }  & \num{ 62.8e6 }$\pm$\num{ 4.2e5 } \\
    \ce{^{22}Na}   & \num{ 1274.577 }  & \num{ 13.8e6 }$\pm$\num{ 2.3e5 } \\
    \end{tabular}

## Help!
For some quick help, you can type in your terminal:

	./csv-to-tabular.py --help

## TODO
- `argparse` help
- code cleanup

## Hacking
…is obviously warmly welcome. All my apologies for the “quick and dirty” appeal
of the code. 

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
