#!/usr/bin/env python

'''
Test_nyctea.py
'''

#############
#  IMPORTS  #
#############
# standard python packages
import copy, inspect, logging, os, sqlite3, sys, time, unittest

# ------------------------------------------------------ #
# import sibling packages HERE!!!

if not os.path.abspath( __file__ + "/../../src" ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../../src" ) )

#import nyctea

if not os.path.abspath( __file__ + "/../../lib/iapyx/src" ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../../lib/iapyx/src" ) )

from dedt       import dedt, dedalusParser, clockRelation, dedalusRewriter
from utils      import dumpers, globalCounters, tools
from evaluators import c4_evaluator

# ------------------------------------------------------ #


#################
#  TEST NYCTEA  #
#################
class Test_nyctea( unittest.TestCase ) :

  logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.DEBUG )
  #logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.INFO )
  #logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.WARNING )

  PRINT_STOP = False



if __name__ == "__main__":
  unittest.main()

#########
#  EOF  #
#########
