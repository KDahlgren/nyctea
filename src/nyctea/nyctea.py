#!/usr/bin/env python

'''
Nyctea.py
'''

# **************************************** #


#############
#  IMPORTS  #
#############
# standard python packages
import copy, inspect, itertools, logging, os, sqlite3, string, sys, time, random
import ConfigParser

# ------------------------------------------------------ #
# import sibling packages HERE!!!
if not os.path.abspath( __file__ + "/../../../lib/iapyx/src" ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../../../lib/iapyx/src" ) )

from dedt           import Fact, dedt, dedalusParser
from utils          import parseCommandLineInput, tools
from evaluators     import c4_evaluator

if not os.path.abspath( __file__ + "/../translators" ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../translators" ) )

from translators import c4_translator, dumpers_c4

# **************************************** #


class Nyctea( object ) :

  #################
  #  CONSTRUCTOR  #
  #################
  # argDict := the dictionary of input arguments
  # cursor  := the pointer to the database instance

  def __init__( self, argDict, cursor ) :

    self.argDict       = argDict
    self.cursor        = cursor
    self.settings_path = self.argDict[ "settings" ]

    logging.debug( "  NYCTEA CONSTRUCTOR : running nyctea with argDict :" )
    for key in argDict :
      logging.debug( "    argDict[ '" + key + "' = " + str( argDict[ key ] )  )

    # ----------------------------------------------------------------- #
    # adjust run parameters given inputs
    # EOT, EFF, crashes

    self.num_random_facts, self.num_random_edbs, self.random_edb_arity = self.adjust_params()

    logging.debug( "  NYCTEA CONSTRUCTOR : self.num_random_facts = " + str( self.num_random_facts ) )
    logging.debug( "  NYCTEA CONSTRUCTOR : self.num_random_edbs  = " + str( self.num_random_edbs ) )
    logging.debug( "  NYCTEA CONSTRUCTOR : self.random_edb_arity = " + str( self.random_edb_arity) )


  #########
  #  RUN  #
  #########
  # translate the input ded file into c4 datalog while adding 
  # additional input

  def run( self ) :

    logging.debug( "  NYCTEA RUN : running process..." )

    # ----------------------------------------------------------------- #
    # create IR tables

    dedt.createDedalusIRTables( self.cursor )

    # ----------------------------------------------------------------- #
    # get all input files

    starterFile        = self.argDict[ 'file' ]
    fileList           = tools.get_all_include_file_paths( starterFile )
    complete_file_path = tools.compile_full_program_and_save( fileList )

    logging.debug( "  NYCTEA RUN : fileList           = " + str( fileList ) )
    logging.debug( "  NYCTEA RUN : complete_file_path = " + str( complete_file_path ) )

    # ----------------------------------------------------------------- #
    # ded to IR

    meta     = dedt.dedToIR( complete_file_path, self.cursor, self.argDict[ "settings" ] )
    factMeta = meta[0]
    ruleMeta = meta[1]

    # ------------------------------------------------------------- #
    # generate the first clock
  
    dedt.starterClock( self.cursor, self.argDict )

    # ------------------------------------------------------------- #
    # generate additional input

    factMeta.extend( self.add_random_facts( factMeta ) )
    factMeta.extend( self.add_random_edbs()  )
  
    # ------------------------------------------------------------- #
    # apply rewrites to generate the corresponding datalog program
    # in the IR database

    allMeta = dedt.rewrite_to_datalog( self.argDict, factMeta, ruleMeta, self.cursor )

    # ------------------------------------------------------------- #
    # translate IR into c4 datalog

    # programData[ 0 ] := all the c4 datalog lines
    # programData[ 1 ] := program table list
    programData = c4_translator.c4datalog( self.argDict, self.cursor )

    logging.debug( "  NYCTEA RUN : programLData[0] :" )
    for line in programData[ 0 ] :
      logging.debug( "    " + line )
    logging.debug( "  NYCTEA RUN : programData[1] : " )
    for table in programData[ 1 ] :
      logging.debug( "    " + table )

    # ------------------------------------------------------------- #
    # save all program lines to file

    try :
      if self.argDict[ "data_save_path" ] :
        logging.debug( "  NYCTEA RUN : using data_save_path '" + self.argDict[ "data_save_path" ] + "'" )
        fo = open( self.argDict[ "data_save_path" ] + "final_initial_program.olg", "w" )
        for line in program[0] :
          fo.write( line + "\n" )
        fo.close()

    except KeyError :
      logging.debug( "  NYCTEA RUN : no data_save_path specified. skipping writing final olg program to file." )

 
    logging.debug( "  NYCTEA RUN : ...done." )

    return [ programData, factMeta, ruleMeta ]


  ######################
  #  ADD RANDOM FACTS  #
  ######################
  # add random acts to existing edbs
  def add_random_facts( self, factMeta ) :

    new_facts_meta = []

    for fact in factMeta :

      # get fact arity
      arity = len( fact.factData[ 'dataList' ] )

      # get types
      type_list = []
      for d in fact.factData[ 'dataList' ] :
        if d.startswith( "'" ) and d.endswith( "'" ) :
          type_list.append( "string" )
        elif d.startswith( '"' ) and d.endswith( '"' ) :
          type_list.append( "string" )
        elif d.isdigit() :
          type_list.append( "int" )
        else :
          raise ValueError( "  FATAL ERROR : unknown data type for '" + d + "' in fact '" + str( fact.factData ) + "'" )

      for j in range( 0, self.num_random_facts ) :
        relationName = fact.relationName
        dataList     = []
        factTimeArg  = "1"

        for k in range( 0, arity ) :
          int_att = random.randint( 0, 100 )
          str_att = '"randomatt' + str( int_att ) + '"'
          if type_list[ k ] == "int" :
            dataList.append( int_att )
          else :
            dataList.append( str_att )

        # save fact
        factData = {}
        factData[ 'relationName' ] = relationName
        factData[ 'dataList' ]     = dataList
        factData[ 'factTimeArg' ]  = factTimeArg
  
        fid            = tools.getIDFromCounters( "fid" )
        newFact        = copy.deepcopy( Fact.Fact( fid, factData, self.cursor ) )
        newFact.cursor = self.cursor
        new_facts_meta.append( newFact )

    return new_facts_meta


  #####################
  #  ADD RANDOM EDBS  #
  #####################
  # factData = { relationName:'relationNameStr', dataList:[ data1, ... , dataN ], factTimeArg:<anInteger> }
  def add_random_edbs( self ) :

    new_facts_meta = []

    for i in range( 0, self.num_random_edbs ) :
      relationName = "random_edb_number_" + str( i )
      dataList     = []
      factTimeArg  = "1"

      # generate random data list
      for j in range( 0, self.random_edb_arity ) :
        int_att = random.randint( 0, 100 )
        str_att = '"randomatt' + str( int_att ) + '"'
        if random.random() > 0.5 :
          dataList.append( int_att )
        else :
          dataList.append( str_att )

      # save fact
      factData = {}
      factData[ 'relationName' ] = relationName
      factData[ 'dataList' ]     = dataList
      factData[ 'factTimeArg' ]  = factTimeArg

      fid            = tools.getIDFromCounters( "fid" )
      newFact        = copy.deepcopy( Fact.Fact( fid, factData, self.cursor ) )
      newFact.cursor = self.cursor
      new_facts_meta.append( newFact )

    return new_facts_meta


  ###################
  #  ADJUST PARAMS  #
  ###################
  # adjust run parameters given nyctea configurations inputs for EOT, EFF, crashes
  # in the settings file
  def adjust_params( self ) :

    # defaults
    num_random_facts = 10
    num_random_edbs = 10
    random_edb_arity = 5

    # num_random_facts
    try :
      num_random_facts = tools.getConfig( self.settings_path, "NYCTEA", "NUM_RANDOM_FACTS", int )
    except ConfigParser.NoOptionError :
      logging.warning( "  WARNING : no 'NUM_RANDOM_FACTS' defined in 'NYCTEA' section of settings file " + self.argDict[ "settings" ] + " ...running with default : num_random_facts = " + str( num_random_facts ) )
      pass

    # num_random_edbs
    try :
      num_random_edbs = tools.getConfig( self.settings_path, "NYCTEA", "NUM_RANDOM_EDBS", int )
    except ConfigParser.NoOptionError :
      logging.warning( "  WARNING : no 'NUM_RANDOM_EDBS' defined in 'NYCTEA' section of settings file " + self.argDict[ "settings" ] + " ...running with default : num_random_facts = " + str( num_random_edbs ) )
      pass

    # random_edb_arity
    try :
      random_edb_arity = tools.getConfig( self.settings_path, "NYCTEA", "RANDOM_EDB_ARITY", int )
    except ConfigParser.NoOptionError :
      logging.warning( "  WARNING : no 'RANDOM_EDB_ARITY' defined in 'NYCTEA' section of settings file " + self.argDict[ "settings" ] + " ...running with default : random_edb_arity = " + str( random_edb_arity ) )
      pass

    return [ num_random_facts, num_random_edbs, random_edb_arity ]


#########
#  EOF  #
#########
