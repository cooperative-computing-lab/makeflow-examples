#!/usr/bin/env python
"""
@summary: This script should do anything necessary to transform the CSV points
             for consumption into Maxent or openModeller
@note: This is a dummy version and just writes the same points to the new 
          location
"""

import argparse

# .............................................................................
if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('in_file', type=str, help='The original raw points')
   parser.add_argument('out_file', type=str, help='The new processed points')
   
   args = parser.parse_args()
   
   with open(args.in_file) as inF:
      with open(args.out_file, 'w') as outF:
         for line in inF:
            outF.write(line)
            
            
