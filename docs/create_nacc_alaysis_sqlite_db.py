#!/usr/bin/env python


# define the paths to the input files

# path to ealgdx_algorithm

# path to nacc raw data

# log dir and file path

# Create a new sqlite db with a timestamp in the name

# desired sqlitedb name and path. NOTE: A timestamp in the form 
#  _20170627_1812.db  will be appended to the end o feach db file as its 
#  created.

# import the raw nacc data

# import the ealgdx alorithm table


# create table of just the vars needed by the ealgdx algo.

qry = 'CREATE TABLE tbl_naccid_with_algdx_vars as SELECT  NACCID, NACCUDSD,  \
       NORMCOG,NACCTMCI,DEMENTED FROM tbl_raw_nacc_20170322_sb'
