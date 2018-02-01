#!/usr/bin/env python

'''
nyctea.py
'''

# **************************************** #


#############
#  IMPORTS  #
#############
# standard python packages
import inspect, itertools, logging, os, sqlite3, string, sys, time

# ------------------------------------------------------ #
# import sibling packages HERE!!!
if not os.path.abspath( __file__ + "/../../../lib/iapyx/src" ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../../../lib/iapyx/src" ) )

from dedt           import dedt, dedalusParser
from utils          import parseCommandLineInput, tools
from evaluators     import c4_evaluator

# **************************************** #


####################
#  CLASS #
####################
