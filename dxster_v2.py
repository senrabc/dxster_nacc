#!/usr/bin/env python                                                            
"""                                                                                
  _____        _____ _                                                             
 |  __ \      / ____| |                                                            
 | |  | |_  __ (___ | |_ ___ _ __                                                  
 | |  | \ \/ /\___ \| __/ _ \ '__|                                                 
 | |__| |>  < ____) | |_  __/ |                                                    
 |_____//_/\_\_____/ \__\___|_|V2                                                    
                                                                                   
Copyright 2017 Christopher P. Barnes <senrabc@gmail.com>                           
Copyright 2017 Kevin Hanson <kshanson@ufl.edu>                                     
                                                                                   
Licensed under the Apache License, Version 2.0 (the "License");                    
you may not use this file except in compliance with the License.                   
You may obtain a copy of the License at                                            
                                                                                   
   http://www.apache.org/licenses/LICENSE-2.0                                      
                                                                                   
Unless required by applicable law or agreed to in writing, software                
distributed under the License is distributed on an "AS IS" BASIS,                  
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.           
See the License for the specific language governing permissions and                
limitations under the License.                                                     


DxSter V2.0.
Usage:
  dxster_v2.py [options] (<EFILE> <DFILE> <OFILE>)

Arguments:
  EFILE  Pass in the ealgdx alogrithm lookup table csv file.                     
  DFILE  Pass in the properly formatted csv file you want to process.            
  OFILE  Pass in the name and path of the output csv file for the results.

Options:
  -h, --help    	Show this screen.
  --version    		Show version.
  -c, --cmd_option  	Example commandline option to pass in [default: 'no']

"""
from docopt import docopt


# Enhanced Algorithmic Diagnosis class
class Ealgdx(object):
    def __init__(self, efile, dfile, ofile, **kwargs):
        self.efile = efile
        self.dfile = dfile
        self.ofile = ofile
 	# self.cmd_option = cmd_option
    
    def print_msg(self):
        print self.efile
        print self.dfile
        print self.ofile
        # print self.cmd_option

if __name__ == '__main__':
    args = docopt(__doc__, version='DxSter v2')
    print args
    run_dxster = Ealgdx(efile=args['<EFILE>'],
			dfile=args['<DFILE>'],
			ofile=args['<OFILE>'])


    run_dxster.print_msg()

                                                                                 
