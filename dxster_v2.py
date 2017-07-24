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
"""

from docopt import docopt
import csv
import sys
import pprint
import numpy as np
import re

#TODO: take inputs from a config file so you don't have to enumerate all args
#       on command line


class Dxster(object):
    #create dicts here to hold ref data files
    list_input_file=[]
    list_output_file=[]
    list_ealgdx_file=[]




    def __init__(self, **kwargs):


        # optional properties
        # using kwargs.pop will return '' if no arg present
        self.input_file = kwargs.pop('input_file','')
        self.output_file = kwargs.pop('output_file','')
        self.ealgdx_file = kwargs.pop('ealgdx_file','')
        # get the reference table
        self.ealgdx_values = np.genfromtxt(self.ealgdx_file, delimiter=',', names=True, dtype=None)




    # def load_list_input_file(self, input_file):
    #     # This function should read the CSV file and load it into the class
    #     # dict called 'dict_input_file' that will hold the data to be processed
    #     reader = csv.DictReader(open(input_file, 'rb'))
    #     for line in reader:
    #         self.list_input_file.append(line)
    #     return  self.list_input_file

    # def load_list_ealgdx_file(self,ealgdx_file):
    #     # This function should read the CSV file and load it into the class
    #     # dict called 'dict_ealgdx_file' that will hold the reference algo data
    #     reader = csv.DictReader(open(ealgdx_file, 'rb'))
    #     for line in reader:
    #         self.list_ealgdx_file.append(line)
    #     return  self.list_ealgdx_file

    def search_ealgdx(self,cdrsum,naccudsd,normcog,nacctmci,demented):
        # required inputs
        # CDR sum of boxes (CDRSUM)
        # NACCUDSD
        # NORMCOG
        # NACCTMCI
        # DEMENTED
        # output
        # ealgdx
        ealgdx=''
        # print('search_ealgdx ...')
        # print(cdrsum)
        # print(naccudsd)
        # print(normcog)
        # print(nacctmci)
        # print(demented)
        # #pprint.pprint(ealgdx_values)
        # physdx_cdrsb = ealgdx_values['physdx_cdrsb'][0]
        # physdx_cdrsb = physdx_cdrsb.replace("'","")
        # physdx_cdrsb = float(physdx_cdrsb)
        # pprint.pprint(physdx_cdrsb)
        normcog=normcog
        naccudsd=naccudsd
        nacctmci=nacctmci
        demented=demented

        k=0
        j=0
        for i,r in enumerate(self.ealgdx_values):
            k=k+1
            # naccudsd=1 and normcog=1 are equivalents in this case
            # in the data we have as of 20170724 the ALWAYS appear together
            # so only need to test for one
            if (normcog==1):
                if ("normcog=1" in r[2].replace("'","")):
                    if (float(cdrsum) == float(r[0].replace("'",""))):
                        j=j+1
                        ealgdx = 'normcog=1 condition = true : ' + str(j) + ':'  + str(k)
            elif (naccudsd==2):
               if (float(cdrsum) == float(r[0].replace("'",""))):
                   if ("naccudsd=2" in r[2].replace("'","")):
                       j=j+1
                       ealgdx = 'naccudsd=2 condition = true : ' + str(j)+ ':'  + str(k)
            elif (naccudsd==3):
                if ("naccudsd=3" in r[2].replace("'","")):
                    if (float(cdrsum) == float(r[0].replace("'",""))):
                        j=j+1
                        ealgdx = 'naccudsd=3 condition = true : ' + str(j)+ ':'  + str(k)
                        #ealgdx = (str(cdrsum) + ':' + r[0].replace("'","") +':' + r[2] +':' + r[3]+':' + 'ealgdx=' + r[3])
                    else:

                        ealgdx = '[ERROR]: Non case for this in the algorithm. Params  \
                        cdrsum %s, normcog %s, naccudsd %s, nacctmci %s, demented %s ' % (cdrsum, normcog, naccudsd, nacctmci, demented)

            # naccudsd=4 and demented=1 are equivalents in this case
            # in the data we have as of 20170724 the ALWAYS appear together
            # so only need to test for one
            elif (demented==1):
                if ("demented=1" in r[2].replace("'","")):
                    if (float(cdrsum) == float(r[0].replace("'",""))):
                        j=j+1
                        ealgdx = 'demented=1 condition = true : ' + str(j)+ ':' + str(k)
                        #ealgdx = (str(cdrsum) + ':' + r[0].replace("'","") +':' + r[2] +':' + r[3]+':' + 'ealgdx=' + r[3])
            elif (nacctmci==3):
                if ("nacctmci=3" in r[2].replace("'","")):
                    if (float(cdrsum) == float(r[0].replace("'",""))):
                        j=j+1
                        ealgdx = 'nacctmci=3 condition = true : ' + str(j)+ ':' + str(k)
                        #ealgdx = (str(cdrsum) + ':' + r[0].replace("'","") +':' + r[2] +':' + r[3]+':' + 'ealgdx=' + r[3])
            elif (nacctmci==4):
                if ("nacctmci=4" in r[2].replace("'","")):
                    if (float(cdrsum) == float(r[0].replace("'",""))):
                        j=j+1
                        ealgdx = 'nacctmci=4 condition = true : ' + str(j)+ ':' + str(k)
                        #ealgdx = (str(cdrsum) + ':' + r[0].replace("'","") +':' + r[2] +':' + r[3]+':' + 'ealgdx=' + r[3])
            else:
                 ealgdx="  else condition true "
                # ealgdx = '[ERROR]: Non case for this in the algorithm. Params  \
                # cdrsum %s, normcog %s, naccudsd %s, nacctmci %s, demented %s ' % (cdrsum, normcog, naccudsd, nacctmci, demented)

        return ealgdx


# this function will take the input data and loop through it line by line
# at each line it will do a lookup_algdx to find the correct algdx from the
# ealgdx ref data in list_ealgdx_file
    def calc_algdx(self):

        # required inputs
        # CDR sum of boxes (CDRSUM)
        # NACCUDSD
        # NORMCOG
        # NACCTMCI
        # DEMENTED


        #input_values = self.load_list_input_file(self.input_file)
        #pprint.pprint(input_values)
        input_data = np.genfromtxt(self.input_file, delimiter=',', names=True, dtype=None)
        for i,r in enumerate(input_data):

            naccid = input_data['NACCID'][i]
            naccvnum = input_data['NACCVNUM'][i]
            cdrsum = input_data['CDRSUM'][i]
            naccudsd = input_data['NACCUDSD'][i]
            normcog = input_data['NORMCOG'][i]
            nacctmci = input_data['NACCTMCI'][i]
            demented = input_data['DEMENTED'][i]
            # this will return the algdx from the lookup

            ealgdx = self.search_ealgdx(cdrsum,naccudsd,normcog,nacctmci,demented)
            print(str(i) + ':' + naccid + ':cd=' + str(cdrsum) + ':cog=' + str(normcog) +  ':uds=' + str(naccudsd) +  ':dim=' + str(demented) + ':tmci=' + str(nacctmci) + ' || ealgdx_str:' + ealgdx)

            # print(input_data['NACCID'][i])
            # for n in r.dtype.names:
            #     print(r[n])



        # pprint.pprint(input_data['NACCID'][0])
        # pprint.pprint(input_data['NACCVNUM'][0])
        # pprint.pprint(input_data['CDRSUM'][0])
        # pprint.pprint(input_data['NACCUDSD'][0])
        # pprint.pprint(input_data['NORMCOG'][0])
        # pprint.pprint(input_data['NACCTMCI'][0])
        # pprint.pprint(input_data['DEMENTED'][0])
        # pprint.pprint(len(input_data))



        # print(naccid)
        # print(naccvnum)
        # print(cdrsum)
        # print(naccudsd)
        # print(normcog)
        # print(nacctmci)
        # print(demented)





        # Loop through the inpu values list and then search the ealgdx_values to see if
        # you can find the matching algdx and then write out to outpu_list
        # for val in input_values:
        #     #pprint.pprint(val)
        #     for a_item in val:
        #         pprint.pprint(a_item)

        # return pprint.pprint(ealgdx_values)

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
