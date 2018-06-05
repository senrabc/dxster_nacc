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
# Copyright 2017 Shanna Burke <sburke@fiu.edu>
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

Usage: dxster_v2.py [options] written and tested for python 2.7x

#time python dxster_v2.py -i ../temp/top100_nacc_dataset_0302217.csv -e ../docs/ealgdx_algorithm_table.csv


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
from datetime import datetime
import csv
import sqlite3
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

    if (DEBUG): print('[DEBUG] Debug on... Will now print all debug statements to stdout.')

    def __init__(self, **kwargs):

        # optional properties
        # using kwargs.pop will return '' if no arg present
        self.input_file = kwargs.pop('input_file','')
        self.output_file = kwargs.pop('output_file','')
        self.ealgdx_file = kwargs.pop('ealgdx_file','')


        # get the reference table
        self.f = open(self.ealgdx_file,'rt')
        self.ealgdx_values = csv.reader(self.f, delimiter=',')

        # startup the db
        self.db = sqlite3.connect(":memory:")
        self.c = self.db.cursor()

    def search_ealgdx(self,cdrsum,naccudsd,normcog,nacctmci,demented):
        # these are the default fields. This will break if the csv changes
        # TODO: read csv header, maybe... this is the ref data and needs to not chg.

        # # for some reason you need to make sure you drop the table or the cache
        # # will come back to bite you and create duplicates.
        # self.c.execute("drop table if not exists ealgdx_algorithm_table")
        self.c.execute("create table if not exists ealgdx_algorithm_table (physdx_cdrsb,\
            npdx,npdx_nacc_uds_equivalent,algdx,ref_uri)")

        # skip the header row
        next(self.ealgdx_values, None)

        # load the alog lookup data from the input file
        for row in self.ealgdx_values:
            values_list = '"' + row[0] + '","' + row[1] + '","' + row[2] + '","' \
                + row[3] + '","' + row[4] + '"'
            #print(values_list)
            sql_stmt = 'INSERT INTO ealgdx_algorithm_table (physdx_cdrsb,npdx,\
            npdx_nacc_uds_equivalent,algdx,ref_uri) VALUES ('+ values_list + ')'
            if (self.DEBUG): print '[DEBUG] In search_algdx. sql_stmt=' + \
            sql_stmt
            self.c.execute(sql_stmt)

        # search query. Most cases return only one result
        # a few I have tested return 2 for naccudsd >=3 and a nacctmci >=2
        # in this case the science team decided that naccudsd >= 3 ealgdx
        # will take precedence. Need to trap multiples.

        # example query
        # SELECT algdx FROM ealgdx_algorithm_table
        # Where physdx_cdrsb = '1.5' AND
        # (
            # npdx_nacc_uds_equivalent ='demented=0' or
            # npdx_nacc_uds_equivalent ='nacctmci=2' or
            # npdx_nacc_uds_equivalent ='normcog=0' or
            # npdx_nacc_uds_equivalent ='naccudsd=3'
        # )

        # This first case handles disagrement between nacctmci with a normal
        # but same cdrsum with naccudsd yielding `mild-moderate mci`
        if ( int(naccudsd)==3 and 1.0<=float(cdrsum)<=1.5 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # handle case where normcog = 1 and naccudsd =1 ALWAYS equivalents
        # both return `normal`
        elif ( int(naccudsd)==1 and int(normcog)==1 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # handle case where both naccudsd=3 and nacctmci=2 return `dementia`
        # for the given range of cdrsb
        elif ( int(naccudsd)==3 and int(nacctmci)==2 and 4.5<=float(cdrsum)<=9.5 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # handle case where both naccudsd=3 and nacctmci=1 return `mci`
        # for the given range of cdrsb
        elif ( int(naccudsd)==3 and int(nacctmci)==1 and 2.5<=float(cdrsum)<=4.0 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # handle case where both naccudsd=3 and nacctmci=2 return `mci`
        # for the given range of cdrsb
        elif ( int(naccudsd)==3 and int(nacctmci)==2 and 2.5<=float(cdrsum)<=2.5 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # Capture this case from
        #https://www.alz.washington.edu/WEB/rdd_uds.pdf
        #
        # Clinicians are asked to designate the type of cognitive impairment for
        # subjects who do not have normal cognition and who are not demented. If
        # the subject had normal cognition or dementia, or was diagnosed as
        # impaired, not MCI, then nacctmci=8.
        # handle case where both naccudsd=2 and nacctmci=8 return `impaired not mci`
        # for the given range of cdrsb

        # this obvisouly needs to be refactored. Here we are forcing the correct
        # value to return and return only once row so ealgdx will be set to the
        # right value in this case.
        elif ( int(naccudsd)==2 and int(nacctmci)==8 and 0.0<=float(cdrsum)<=0.5 ):
            sql_stmt2 = "SELECT 'impaired not mci' FROM ealgdx_algorithm_table Limit 1"

        else:
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s" or \
                npdx_nacc_uds_equivalent ="normcog=%s" or \
                npdx_nacc_uds_equivalent ="nacctmci=%s" or \
                npdx_nacc_uds_equivalent ="demented=%s" )' % (cdrsum, naccudsd, \
                normcog, nacctmci, demented)

        #print(sql_stmt2)
        if (self.DEBUG): print '[DEBUG] In search_algdx. sql_stmt2=' + sql_stmt2

        # need to error out for now if 2 rows returned
        # Most cases return only one result
        # a few I have tested return 2 for naccudsd >=3 and a nacctmci >=2
        # in this case the science team decided that naccudsd >= 3 ealgdx
        # will take precedence. Need to trap multiples.
        #print(sql_stmt2)

        i = 0
        #recset = self.c.execute('select * from ealgdx_algorithm_table')
        recset = self.c.execute(sql_stmt2)
        #print(recset)
        for row in recset:
            i=i+1

            # set on the first run through so you can check to see if its the
            # same every time. This happens with mci so if all duplicates are
            # the same return the value. Example, if all row conditions return
            # mci then the ealgdx should be mci otherwise if they disagree
            # throw an error

            local_ealgdx = row[0]

            # Here there's only one row so thats the value we want.
            if (i==1):
                ealgdx = local_ealgdx
            # this is where we are checking to see if each rec returned is
            # the same
            elif (local_ealgdx == row[0]):
                    ealgdx = local_ealgdx
            else:
                    ealgdx = '[ERROR]: Multiple Values Returned for params. CNT=%s , SQL: %s ' % (str(i), sql_stmt2)
        # no rows returned is another problem. We always expect at least one
        # row. This means that this record has no existing classification. call
        # it unclassified
        if i==0:
                ealgdx = 'unclassified'

        return ealgdx

    def search_ealgdx_naccudsd(self,cdrsum,naccudsd,normcog,nacctmci,demented):
        # THIS IS A VERSION THAT ONLY USES NACCUDSD
        # TODO: read csv header, maybe... this is the ref data and needs to not chg.
        # TODO: REFACTOR ALL LOADING OF EALGDX REF DATA TO ANOTHER place
        #       THIS ONLY NEEEDS TO GET PROCESSED ONCE PER RUN NOT EVERY search.
        # # for some reason you need to make sure you drop the table or the cache
        # # will come back to bite you and create duplicates.
        # self.c.execute("drop table if not exists ealgdx_algorithm_table")
        self.c.execute("create table if not exists ealgdx_algorithm_table (physdx_cdrsb,\
            npdx,npdx_nacc_uds_equivalent,algdx,ref_uri)")

        # skip the header row
        next(self.ealgdx_values, None)

        # load the alog lookup data from the input file
        for row in self.ealgdx_values:
            values_list = '"' + row[0] + '","' + row[1] + '","' + row[2] + '","' \
                + row[3] + '","' + row[4] + '"'
            #print(values_list)
            sql_stmt = 'INSERT INTO ealgdx_algorithm_table (physdx_cdrsb,npdx,\
            npdx_nacc_uds_equivalent,algdx,ref_uri) VALUES ('+ values_list + ')'
            if (self.DEBUG): print '[DEBUG] In search_algdx. sql_stmt=' + \
            sql_stmt
            self.c.execute(sql_stmt)

        # search query. Most cases return only one result
        # a few I have tested return 2 for naccudsd >=3 and a nacctmci >=2
        # in this case the science team decided that naccudsd >= 3 ealgdx
        # will take precedence. Need to trap multiples.

        # example query
        # SELECT algdx FROM ealgdx_algorithm_table
        # Where physdx_cdrsb = '1.5' AND
        # (
            # npdx_nacc_uds_equivalent ='demented=0' or
            # npdx_nacc_uds_equivalent ='nacctmci=2' or
            # npdx_nacc_uds_equivalent ='normcog=0' or
            # npdx_nacc_uds_equivalent ='naccudsd=3'
        # )

        # This first case handles disagrement between nacctmci with a normal
        # but same cdrsum with naccudsd yielding `mild-moderate mci`
        if ( int(naccudsd)==3 and 1.0<=float(cdrsum)<=1.5 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # handle case where naccudsd =1
        #  return `normal`
        elif ( int(naccudsd)==1 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # handle case where both naccudsd=3 and nacctmci=2 return `dementia`
        # for the given range of cdrsb
        elif ( int(naccudsd)==3  and 4.5<=float(cdrsum)<=9.5 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # handle case where both naccudsd=3 and nacctmci=1 return `mci`
        # for the given range of cdrsb
        elif ( int(naccudsd)==3  and 2.5<=float(cdrsum)<=4.0 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # handle case where both naccudsd=3 and nacctmci=2 return `mci`
        # for the given range of cdrsb
        elif ( int(naccudsd)==3  and 2.5<=float(cdrsum)<=2.5 ):
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s")' % (cdrsum,naccudsd)
        # Capture this case from
        #https://www.alz.washington.edu/WEB/rdd_uds.pdf
        #
        # Clinicians are asked to designate the type of cognitive impairment for
        # subjects who do not have normal cognition and who are not demented. If
        # the subject had normal cognition or dementia, or was diagnosed as
        # impaired, not MCI, then nacctmci=8.
        # handle case where both naccudsd=2 and nacctmci=8 return `impaired not mci`
        # for the given range of cdrsb

        # this obvisouly needs to be refactored. Here we are forcing the correct
        # value to return and return only once row so ealgdx will be set to the
        # right value in this case.
        elif ( int(naccudsd)==2  and 0.0<=float(cdrsum)<=0.5 ):
            sql_stmt2 = "SELECT 'impaired not mci' FROM ealgdx_algorithm_table Limit 1"

        else:
            sql_stmt2 = 'SELECT algdx FROM ealgdx_algorithm_table \
                WHERE physdx_cdrsb = "%s" AND \
                (npdx_nacc_uds_equivalent ="naccudsd=%s" or \
                npdx_nacc_uds_equivalent ="normcog=%s" or \
                npdx_nacc_uds_equivalent ="nacctmci=%s" or \
                npdx_nacc_uds_equivalent ="demented=%s" )' % (cdrsum, naccudsd, \
                normcog, nacctmci, demented)

        #print(sql_stmt2)
        if (self.DEBUG): print '[DEBUG] In search_algdx. sql_stmt2=' + sql_stmt2

        # need to error out for now if 2 rows returned
        # Most cases return only one result
        # a few I have tested return 2 for naccudsd >=3 and a nacctmci >=2
        # in this case the science team decided that naccudsd >= 3 ealgdx
        # will take precedence. Need to trap multiples.
        #print(sql_stmt2)

        i = 0
        #recset = self.c.execute('select * from ealgdx_algorithm_table')
        recset = self.c.execute(sql_stmt2)
        #print(recset)
        for row in recset:
            i=i+1

            # set on the first run through so you can check to see if its the
            # same every time. This happens with mci so if all duplicates are
            # the same return the value. Example, if all row conditions return
            # mci then the ealgdx should be mci otherwise if they disagree
            # throw an error

            local_ealgdx = row[0]

            # Here there's only one row so thats the value we want.
            if (i==1):
                ealgdx = local_ealgdx
            # this is where we are checking to see if each rec returned is
            # the same
            elif (local_ealgdx == row[0]):
                    ealgdx = local_ealgdx
            else:
                    ealgdx = '[ERROR]: Multiple Values Returned for params. CNT=%s , SQL: %s ' % (str(i), sql_stmt2)
        # no rows returned is another problem. We always expect at least one
        # row. This means that this record has no existing classification. call
        # it unclassified
        if i==0:
                ealgdx = 'unclassified'

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

    def calc_algdx_csv(self):
        f = open(self.input_file)

        # handle output file settings. If one wasn't passed in as an argument
        # then make one
        if self.output_file:
            out = self.output_file
        else:
            out = datetime.now().strftime("%Y%m%d_%H%M%S") + '_output_file.csv'
        print(out)

        r = csv.reader(f, delimiter=',')
        row_0 = r.next()
        row_0.append('ealgdx')
        row_0.append('debug_string')

        #print(row_0)
        # this needs to be fixed to pass in the output file path info from
        # the args. this goes in 12 seconds versus calc-algdx not completeing
        # as a string operation when run with 100k input rows
        with open(out, 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            writer.writerow(row_0)


            for item in r:
                naccid=item[1]
                naccvnum=item[2]
                cdrsum=item[173]
                naccudsd=item[551]
                normcog=item[386]
                nacctmci=item[396]
                demented=item[387]


                # ealgdx output is in the form (ealgdx, debugstring)
                ealgdx = self.search_ealgdx(cdrsum,naccudsd,normcog,nacctmci,demented)
                debug_string = ('debug_string=naccid=' + str(naccid) + \
                                ':naccvnum=' + str(naccvnum) + \
                                ':cdrsum=' + str(cdrsum) + \
                                ':normcog=' + str(normcog) +  \
                                ':naccudsd=' + str(naccudsd) +  \
                                ':demented=' + str(demented) + \
                                ':nacctmci=' + str(nacctmci) + \
                                ':ealgdx=' + ealgdx)
                item.append(ealgdx)
                item.append(debug_string)


                writer.writerow(item)
            #print(item)


        #return

    ## THIS IS A VERSION THAT ONLY USES NACCUDSD AS THE neuropscyhDX

    def calc_algdx_csv_naccudsd(self):
        f = open(self.input_file)

        # handle output file settings. If one wasn't passed in as an argument
        # then make one
        if self.output_file:
            out = self.output_file
        else:
            out = datetime.now().strftime("%Y%m%d_%H%M%S") + '_output_file.csv'
        print(out)

        r = csv.reader(f, delimiter=',')
        row_0 = r.next()
        row_0.append('ealgdx')
        row_0.append('debug_string')

        #print(row_0)
        # this needs to be fixed to pass in the output file path info from
        # the args. this goes in 12 seconds versus calc-algdx not completeing
        # as a string operation when run with 100k input rows
        with open(out, 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            writer.writerow(row_0)


            for item in r:
                naccid=item[1]
                naccvnum=item[2]
                cdrsum=item[173]
                naccudsd=item[551]
                normcog=item[386]
                nacctmci=item[396]
                demented=item[387]


                # ealgdx output is in the form (ealgdx, debugstring)
                ealgdx = self.search_ealgdx_naccudsd(cdrsum,naccudsd,normcog,nacctmci,demented)
                debug_string = ('debug_string=naccid=' + str(naccid) + \
                                ':naccvnum=' + str(naccvnum) + \
                                ':cdrsum=' + str(cdrsum) + \
                                ':normcog=' + str(normcog) +  \
                                ':naccudsd=' + str(naccudsd) +  \
                                ':demented=' + str(demented) + \
                                ':nacctmci=' + str(nacctmci) + \
                                ':ealgdx=' + ealgdx)
                item.append(ealgdx)
                item.append(debug_string)


                writer.writerow(item)
        #return True

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

    #dxster.calc_algdx()
    #print('-----------------------------------')
    # use this call for old version pre 20180306
    #dxster.calc_algdx_csv()

    #use this version for calc that only uses NACCUDSD
    dxster.calc_algdx_csv_naccudsd()
