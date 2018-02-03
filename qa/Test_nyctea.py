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

from nyctea import Nyctea

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

  #logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.DEBUG )
  logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.INFO )
  #logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.WARNING )

  PRINT_STOP = False

  ###############
  #  EXAMPLE 1  #
  ###############
  def test_nyctea_example_1( self ) :

    test_id = "_nyctea_example_1_"

    # --------------------------------------------------------------- #
    # testing set up.

    testDB = "./IR" + test_id + ".db"

    if os.path.exists( testDB ) :
      os.remove( testDB )

    IRDB   = sqlite3.connect( testDB )
    cursor = IRDB.cursor()

    # --------------------------------------------------------------- #
    #dependency

    #dedt.createDedalusIRTables(cursor)
    dedt.globalCounterReset()

    # --------------------------------------------------------------- #

    # specify input file path
    inputfile = "./testFiles/example_1.ded"

    # get argDict
    argDict = self.getArgDict( inputfile )

    # specify settings file
    argDict[ "settings" ] = "./settingsFiles/settings.ini"

    # instantiate nyctea object
    n = Nyctea.Nyctea( argDict, cursor )

    # run translator
    programData, factMeta, ruleMeta = n.run()

    # portray actual output program lines as a single string
    actual_results = self.getActualResults( programData[0] )

    if self.PRINT_STOP :
      print actual_results
      sys.exit( "print stop." )

    # grab expected output results as a string
    expected_results_path = "./testFiles/example_1.olg"
    expected_results      = None
    with open( expected_results_path, 'r' ) as expectedFile :
      expected_results = expectedFile.read()

    self.assertEqual( actual_results, expected_results )

    # --------------------------------------------------------------- #
    #clean up testing

    IRDB.close()

    if os.path.exists( testDB ) :
      os.remove( testDB )


  ########################
  #  NYCTEA CONSTRUCTOR  #
  ########################
  def test_nyctea_constructor( self ) :

    test_id = "_test_nyctea_constructor_"

    # --------------------------------------------------------------- #
    # testing set up.
    testDB = "./IR" + test_id + ".db"
    IRDB   = sqlite3.connect( testDB )
    cursor = IRDB.cursor()

    # --------------------------------------------------------------- #
    #dependency
    #dedt.createDedalusIRTables(cursor)
    dedt.globalCounterReset()

    # --------------------------------------------------------------- #

    # specify input file path
    inputfile = "./testFiles/empty.ded"

    # get argDict
    argDict = self.getArgDict( inputfile )

    # instantiate nyctea object
    n = Nyctea.Nyctea( argDict, cursor )

    expected_prov_diagrams            = False
    expected_use_symmetry             = False
    expected_crashes                  = 0
    expected_solver                   = None
    expected_disable_dot_rendering    = False
    expected_settings                 = "./settingsFiles/settings.ini"
    expected_negative_support         = False
    expected_strategy                 = None
    expected_file                     = inputfile
    expected_EOT                      = 4
    expected_find_all_counterexamples = False
    expected_nodes                    = [ "a", "b", "c" ]
    expected_evaluator                = "c4"
    expected_EFF                      = 2

    self.assertEqual( argDict[ "prov_diagrams" ],            expected_prov_diagrams            )
    self.assertEqual( argDict[ "use_symmetry" ],             expected_use_symmetry             )
    self.assertEqual( argDict[ "crashes" ],                  expected_crashes                  )
    self.assertEqual( argDict[ "solver" ],                   expected_solver                   )
    self.assertEqual( argDict[ "disable_dot_rendering" ],    expected_disable_dot_rendering    )
    self.assertEqual( argDict[ "settings" ],                 expected_settings                 )
    self.assertEqual( argDict[ "negative_support" ],         expected_negative_support         )
    self.assertEqual( argDict[ "strategy" ],                 expected_strategy                 )
    self.assertEqual( argDict[ "file" ],                     expected_file                     )
    self.assertEqual( argDict[ "EOT" ],                      expected_EOT                      )
    self.assertEqual( argDict[ "find_all_counterexamples" ], expected_find_all_counterexamples )
    self.assertEqual( argDict[ "nodes" ],                    expected_nodes                    )
    self.assertEqual( argDict[ "evaluator" ],                expected_evaluator                )
    self.assertEqual( argDict[ "EFF" ],                      expected_EFF                      )

    # --------------------------------------------------------------- #
    #clean up testing
    IRDB.close()
    os.remove( testDB )


  # ////////////////////////////// #
  #          HELPER TOOLS          #
  # ////////////////////////////// #

  ###############
  #  GET ERROR  #
  ###############
  # extract error message from system info
  def getError( self, sysInfo ) :
    return str( sysInfo[1] )


  ########################
  #  GET ACTUAL RESULTS  #
  ########################
  def getActualResults( self, programLines ) :
    program_string  = "\n".join( programLines )
    program_string += "\n" # add extra newline to align with read() parsing
    return program_string


  ##################
  #  GET ARG DICT  #
  ##################
  def getArgDict( self, inputfile ) :

    # initialize
    argDict = {}

    # populate with unit test defaults
    argDict[ 'prov_diagrams' ]            = False
    argDict[ 'use_symmetry' ]             = False
    argDict[ 'crashes' ]                  = 0
    argDict[ 'solver' ]                   = None
    argDict[ 'disable_dot_rendering' ]    = False
    argDict[ 'settings' ]                 = "./settingsFiles/settings.ini"
    argDict[ 'negative_support' ]         = False
    argDict[ 'strategy' ]                 = None
    argDict[ 'file' ]                     = inputfile
    argDict[ 'EOT' ]                      = 4
    argDict[ 'find_all_counterexamples' ] = False
    argDict[ 'nodes' ]                    = [ "a", "b", "c" ]
    argDict[ 'evaluator' ]                = "c4"
    argDict[ 'EFF' ]                      = 2

    return argDict


if __name__ == "__main__":
  unittest.main()
  if os.path.exists( "./IR*.db*" ) :
    os.remove( "./IR*.db*" )


#########
#  EOF  #
#########
