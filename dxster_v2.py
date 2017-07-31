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
    -e, --ealgdx_file=<file> Full path to ealgdx.csv file [ex. '/home/senrabc/ealgdx.csv']
    -i, --input_file=<file>  Path to CSV data file [ex. '/home/senrabc/mydata.csv']
    -o, --output_file=<file>  Path to output CSV file [ex. '~/myoutput.csv']
    -r, --property_here        THIS NEEDS REMOVAL: Start the server if yes [default: 'no']
    -d, --debug  turn on all debug statements
"""

from docopt import docopt
import csv
import sys
import pprint
#import numpy as np
import pdb


#TODO: take inputs from a config file so you don't have to enumerate all args
#       on command line


class Dxster(object):
    #create dicts here to hold ref data files
    list_input_file=[]
    list_output_file=[]
    list_ealgdx_file=[]

#TODO: implement catach docopt --debug option to turn it on and off

    DEBUG = False
    #DEBUG = True

    if (DEBUG): print '[DEBUG] Debug on... Will now print all debug statements to stdout.'

    def __init__(self, **kwargs):

        # optional properties
        # using kwargs.pop will return '' if no arg present
        self.input_file = kwargs.pop('input_file','')
        self.output_file = kwargs.pop('output_file','')
        self.ealgdx_file = kwargs.pop('ealgdx_file','')


        # get the reference table
        self.f = open(self.ealgdx_file,'rt')
        self.ealgdx_values = csv.reader(self.f, delimiter=',')

        #self.ealgdx_values = np.genfromtxt(self.ealgdx_file, delimiter=',', names=True, dtype=None)
        #self.ealgdx_values = open(self.ealgdx_file, 'rt')




    def search_ealgdx(self,cdrsum,naccudsd,normcog,nacctmci,demented):

        # reset the iterator to the begining.
        self.f.seek(0)

        normcog=normcog
        naccudsd=naccudsd
        nacctmci=nacctmci
        demented=demented
        debug_str=''
        ealgdx = ''
        if (self.DEBUG): print '[DEBUG] Start new case ...'
        if (self.DEBUG): print '[DEBUG] In search_ealgdx, input normcog=' + normcog
        if (self.DEBUG): print '[DEBUG] In search_ealgdx, input naccudsd=' + naccudsd
        if (self.DEBUG): print '[DEBUG] In search_ealgdx, input nacctmci=' + nacctmci
        if (self.DEBUG): print '[DEBUG] In search_ealgdx, input demented=' + demented
        # cntrs for debugging lookup
        k=0
        j=0
        # skip the header row
        next(self.ealgdx_values, None)

        for row in self.ealgdx_values:
            #print (row)
            k=k+1
            # naccudsd=1 and normcog=1 are equivalents in this case
            # in the data we have as of 20170724 the ALWAYS appear together
            # so only need to test for one
            # pdb.set_trace()
            if (int(normcog)==1):
                if (self.DEBUG): print '[DEBUG] In normcog=1' + str(k)
                if ("normcog=1" in row[2].replace("'","")):
                    if (float(cdrsum) == float(row[0].replace("'",""))):
                        j=j+1
                        ealgdx = row[3]
                        debug_str = 'normcog=1 condition = true : ' + str(j) + ':'  + str(k)+ ' cdrmatch=' + str(cdrsum) + ':' + str(row[0])
                        if (self.DEBUG): print debug_str
            elif (int(naccudsd)==2):
               if (self.DEBUG): print '[DEBUG] In naccudsd=2'
               if (float(cdrsum) == float(row[0].replace("'",""))):
                   if ("naccudsd=2" in row[2].replace("'","")):
                       j=j+1
                       ealgdx = row[3]
                       debug_str = 'naccudsd=2 condition = true : ' + str(j)+ ':'  + str(k)+ ' cdrmatch=' + str(cdrsum) + ':' + str(row[0])
                       if (self.DEBUG): print debug_str
            elif (int(naccudsd)==3):
                #pdb.set_trace()
                if (self.DEBUG): print '[DEBUG] In naccudsd=3 ' + str(row[2]) + ", " + str(k)
                if ("naccudsd=3" in row[2].replace("'","")):
                    if (float(cdrsum) == float(row[0].replace("'",""))):
                        j=j+1
                        ealgdx = row[3]
                        debug_str = 'naccudsd=3 condition = true : ' + str(j)+ ':'  + str(k)+ ' cdrmatch=' + str(cdrsum) + ':' + str(row[0])
                        if (self.DEBUG): print debug_str
                    else:
                        if (self.DEBUG): print '[DEBUG] In else condition for naccudsd=3'
                        ealgdx = '[ERROR]'
                        debug_str = '[ERROR]: conflicting match for this in the algorithm. Params  \
                        cdrsum %s, normcog %s, naccudsd %s, nacctmci %s, demented %s ' % (cdrsum, normcog, naccudsd, nacctmci, demented)
                        if (self.DEBUG): print debug_str
            # naccudsd=4 and demented=1 are equivalents in this case
            # in the data we have as of 20170724 the ALWAYS appear together
            # so only need to test for one
            elif (int(demented)==1):
                if ("demented=1" in row[2].replace("'","")):
                    if (float(cdrsum) == float(row[0].replace("'",""))):
                        j=j+1
                        ealgdx = row[3]
                        debug_str = 'demented=1 condition = true : ' + str(j)+ ':' + str(k)+ ' cdrmatch=' + str(cdrsum) + ':' + str(row[0])
                        if (self.DEBUG): print debug_str
            elif (int(nacctmci)==3):
                if ("nacctmci=3" in row[2].replace("'","")):
                    if (float(cdrsum) == float(row[0].replace("'",""))):
                        j=j+1
                        ealgdx = row[3]
                        debug_str = 'nacctmci=3 condition = true : ' + str(j)+ ':' + str(k)+ ' cdrmatch=' + str(cdrsum) + ':' + str(row[0])
                        if (self.DEBUG): print debug_str
            elif (int(nacctmci)==4):
                if ("nacctmci=4" in row[2].replace("'","")):
                    if (float(cdrsum) == float(row[0].replace("'",""))):
                        j=j+1
                        ealgdx = row[3]
                        debug_str = 'nacctmci=4 condition = true : ' + str(j)+ ':' + str(k) + ' cdrmatch=' + str(cdrsum) + ':' + str(row[0])
                        if (self.DEBUG): print debug_str
            else:
                ealgdx = '[ERROR]'
                debug_str = "  [ERROR] else condition true. conflicting case for these params "
                if (self.DEBUG): print debug_str

        # for development the csv header is in the form [..., ealgdx, debug_string]
        ealgdx = ealgdx + ',' + debug_str


        return ealgdx


# this function will take the input data and loop through it line by line
# at each line it will do a lookup_algdx to find the correct algdx from the
# ealgdx ref data in list_ealgdx_file
# required inputs
# CDR sum of boxes (CDRSUM)
# NACCUDSD
# NORMCOG
# NACCTMCI
# DEMENTED
    def calc_algdx(self):

        #form the CSV output header
        output_str = 'naccid' + ',' + 'naccvnum' + ',' + 'cdrsum' + ',' + \
                    'naccudsd' + ',' + 'normcog' + ',' + 'nacctmci' + ',' + \
                    'demented' + ',' + 'ealgdx' + ',' + 'debug_string \n'

        with open(self.input_file) as csvfile:
            r = csv.reader(csvfile, delimiter=',')
            # skip the header row
            next(r, None)
            for row in r:
                #print(row)
                #print(row[0])

                # NACCID [1],
                # NACCVNUM [2]
                # CDR sum of boxes (CDRSUM) [173]
                # NACCUDSD [551]
                # NORMCOG [386]
                # NACCTMCI [396]
                # DEMENTED [387]
                #print(row[1],row[2],row[173],row[551],row[386],row[396],row[387])

                naccid=row[1]
                naccvnum=row[2]
                cdrsum=row[173]
                naccudsd=row[551]
                normcog=row[386]
                nacctmci=row[396]
                demented=row[387]
                # ealgdx output is in the form (ealgdx, debugstring)
                ealgdx = self.search_ealgdx(cdrsum,naccudsd,normcog,nacctmci,demented)
                #format the output for csv out,

                output_str = output_str + str(naccid) + ',' + str(naccvnum) + ',' + str(cdrsum) + ',' + \
                            str(naccudsd) + ',' + str(normcog) + ',' + str(nacctmci) + ',' + \
                            str(demented) + ',' + str(ealgdx) + '\n'
                #print(str(i) + ':' + naccid + ':cd=' + str(cdrsum) + ':cog=' + str(normcog) +  ':uds=' + str(naccudsd) +  ':dim=' + str(demented) + ':tmci=' + str(nacctmci) + ' || ealgdx_str:' + ealgdx)




        print(output_str)
        #return output_str

    #Sample Function for CLI args. REMOVE later
    def print_msg(self):
        print self.my_property
        print self.input_file
        print self.output_file
        print self.ealgdx_file

        #test load of the input file
        #input_values = self.load_list_input_file(self.input_file)
        #pprint.pprint(input_values)
        #test ealgdx load
        #ealgdx_values = self.load_list_ealgdx_file(self.ealgdx_file)
        #pprint.pprint(ealgdx_values)

if __name__ == '__main__':
    args = docopt(__doc__)


    dxster = Dxster(
        my_property=args['--property_here'],
        input_file=args['--input_file'],
        output_file=args['--output_file'],
        ealgdx_file=args['--ealgdx_file']

    )

    # sample usage output for ali args form docopt. REMOVE later
    #print args
    # sample call to class fucntion
    #dxster.print_msg()

    dxster.calc_algdx()
    #dxster.search_ealgdx()
