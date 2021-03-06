#!/usr/bin/env python

import logging, os, sys, unittest
import Test_nyctea

#####################
#  UNITTEST DRIVER  #
#####################
def unittest_driver() :

  print
  print "***********************************"
  print "*  RUNNING TEST SUITE FOR NYCTEA  *"
  print "***********************************"
  print

  # make absolutely sure no leftover IR files exist.
  if os.path.exists( "./IR*.db*" ) :
    os.system( "rm ./IR*.db*" )
    logging.info( "  UNIT TEST DRIVER : deleted all rogue IR*.db* files." )

  # run Test_nyctea tests
  suite = unittest.TestLoader().loadTestsFromTestCase( Test_nyctea.Test_nyctea )
  unittest.TextTestRunner( verbosity=2, buffer=True ).run( suite )


#########################
#  THREAD OF EXECUTION  #
#########################
if __name__ == "__main__" :
  logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.INFO )
  unittest_driver()

# make absolutely sure no leftover IR files exist.
if os.path.exists( "./IR*.db*" ) :
  os.system( "rm ./IR*.db*" )
  logging.info( "  UNIT TEST DRIVER : deleted all rogue IR*.db* files." )



#########
#  EOF  #
#########
