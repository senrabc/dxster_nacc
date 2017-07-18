#!/usr/bin/env python
################################################################################
#  _____        _____ _
# |  __ \      / ____| |
# | |  | |_  __ (___ | |_ ___ _ __
# | |  | \ \/ /\___ \| __/ _ \ '__|
# | |__| |>  < ____) | |_  __/ |
# |_____//_/\_\_____/ \__\___|_|V2
#
# Copyright 2017 Christopher P. Barnes <senrabc@gmail.com>
# Copyright 2017 Kevin Hanson <kshanson@ufl.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################

"""Dxster

Usage: dxster_v2.py [options]


Options:
    -h, --help
    -c, --config=<file>  Path to the config file [TODO: MAKE THIS WORK]
    -e, --ealgdx_data=<file> Full path to ealgdx.csv file [ex. '/home/senrabc/ealgdx.csv']
    -i, --input_file=<file>  Path to CSV data file [ex. '/home/senrabc/mydata.csv']
    -o, --output_file=<file>  Path to output CSV file [ex. '~/myoutput.csv']
    -r, --property_here        THIS NEEDS REMOVAL: Start the server if yes [default: 'no']
"""

from docopt import docopt
import csv
import sys
import pprint

#TODO: take inputs from a config file so you don't have to enumerate all args
#       on command line


class Dxster(object):
    #create dicts here to hold ref data files
    dict_input_file=[]
    dict_output_file={}
    dict_ealgdx_file={}


    def __init__(self, my_property, **kwargs):

        # example object property from CLI arg: use or remove alter if uneeded
        self.my_property = my_property

        # optional properties
        # using kwargs.pop will return '' if no arg present
        self.input_file = kwargs.pop('input_file','')
        self.output_file = kwargs.pop('output_file','')
        self.ealgdx_file = kwargs.pop('ealgdx_data','')

    def load_dict_input_file(self, input_file):
        # This function should read the CSV file and load it into the class
        # dict called 'dict_input_file' that will hold the data to be processed
        reader = csv.DictReader(open(input_file, 'rb'))
        for line in reader:
            self.dict_input_file.append(line)
        return  self.dict_input_file

    def load_dict_ealgdx_file():
        # This function should read the CSV file and load it into the class
        # dict called 'dict_ealgdx_file' that will hold the reference algo data
        print ''
    #Sample Function for CLI args. REMOVE later
    def print_msg(self):
        print self.my_property
        print self.input_file
        print self.output_file
        print self.ealgdx_file

        #test load of the input file
        input_values = self.load_dict_input_file(self.input_file)
        pprint.pprint(input_values)

if __name__ == '__main__':
    args = docopt(__doc__)

    #sample usage output for ali args form docopt. REMOVE later
    print args
    dxster = Dxster(
        my_property=args['--property_here'],
        input_file=args['--input_file'],
        output_file=args['--output_file'],
        ealgdx_data=args['--ealgdx_data']

    )
    dxster.print_msg()
