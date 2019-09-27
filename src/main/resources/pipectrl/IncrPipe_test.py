#=======================================================================
# IncrPipe_test.py
#=======================================================================

import pytest

from pymtl       import *
from pclib.test  import TestSource, TestSink
from IncrPipe    import *

#-----------------------------------------------------------------------
# TestHarness
#-----------------------------------------------------------------------
class TestHarness( Model ):

  def __init__( s, ModelType, src_msgs, sink_msgs,
                src_delay, sink_delay, test_verilog, dump_vcd ):

    # Instantiate models

    s.src        = TestSource ( 17, src_msgs,  src_delay  )
    s.incr_pipe  = ModelType  ( 8 )
    s.sink       = TestSink   ( 8, sink_msgs, sink_delay )

    s.vcd_file           = dump_vcd
    s.incr_pipe.vcd_file = dump_vcd

    if test_verilog:
      s.incr_pipe = TranslationTool( s.incr_pipe )

    s.connect( s.incr_pipe.in_ , s.src.out )
    s.connect( s.incr_pipe.out , s.sink.in_ )

  def done( s ):
    return s.src.done and s.sink.done

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.incr_pipe.line_trace() \
           + " > " + s.sink.line_trace()

#-----------------------------------------------------------------------
# run_incr_pipe_test
#-----------------------------------------------------------------------
def run_incr_pipe_test( dump_vcd, src_msgs, sink_msgs,
                        ModelType, src_delay, sink_delay, test_verilog ):

  # Instantiate and elaborate the model

  model = TestHarness( ModelType, src_msgs, sink_msgs,
                       src_delay, sink_delay, test_verilog, dump_vcd
                     )
  model.elaborate()

  # Create a simulator using the simulation tool

  sim = SimulationTool( model )

  # Run the simulation

  print ""

  sim.reset()
  while not model.done():
    sim.print_line_trace()
    sim.cycle()

  # Add a couple extra ticks so that the VCD dump is nicer

  sim.cycle()
  sim.cycle()
  sim.cycle()

#-----------------------------------------------------------------------
# mk_req helper function
#-----------------------------------------------------------------------

def mk_req( st_stage, st_cycles, sq_stage, value ):
  bits = Bits( TRANSACTION_NBITS )
  bits[STALL_STAGE]  = st_stage
  bits[STALL_CYCLES] = st_cycles
  bits[SQUASH_STAGE] = sq_stage
  bits[VALUE]        = value
  return bits

#-----------------------------------------------------------------------
# Simple Pipeline Test - No stalls or squashes
#-----------------------------------------------------------------------
#
# Modeling;
#
# t0 A B C D E
# t1   A B C D E
# t2     A B C D E
# t3       A B C D E
# t4         A B C D E

src_simple_msgs = [
    mk_req( 0, 0, 0, 1 ),
    mk_req( 0, 0, 0, 2 ),
    mk_req( 0, 0, 0, 3 ),
    mk_req( 0, 0, 0, 4 ),
    mk_req( 0, 0, 0, 5 ),
  ]

sink_simple_msgs = [
    4,
    5,
    6,
    7,
    8,
  ]

@pytest.mark.parametrize( "src_delay,sink_delay", [
  ( 0, 0),
  ( 5, 0),
  ( 0, 5),
  ( 4, 9),
])
def test_simple_pipe( dump_vcd, test_verilog, src_delay, sink_delay ):
  run_incr_pipe_test( dump_vcd, src_simple_msgs, sink_simple_msgs,
                      IncrPipe, src_delay, sink_delay, test_verilog )

#-----------------------------------------------------------------------
# Stall Pipeline Test - no squashes
#-----------------------------------------------------------------------
# Note: For the current microarchitecture, can't stall in A or B stage
#
# Modeling;
#
# t0 A B C C D E
# t1   A B B C D D D E
# t2     A A B C C C D E E E E
# t3         A B B B C D D D D E E E
# t4           A A A B C C C C C C C D E

src_stall_msgs = [
    mk_req( STAGE_C, 1, 0, 1 ),
    mk_req( STAGE_D, 2, 0, 2 ),
    mk_req( STAGE_E, 3, 0, 3 ),
    mk_req( STAGE_E, 2, 0, 4 ),
    mk_req( STAGE_C, 1, 0, 5 ),
  ]

sink_stall_msgs = [
    4,
    5,
    6,
    7,
    8,
  ]

@pytest.mark.parametrize( "src_delay,sink_delay", [
  ( 0, 0),
  ( 5, 0),
  ( 0, 5),
  ( 4, 9),
])
def test_stall_pipe( dump_vcd, test_verilog, src_delay, sink_delay ):
  run_incr_pipe_test( dump_vcd, src_stall_msgs, sink_stall_msgs,
                      IncrPipe, src_delay, sink_delay, test_verilog )

#-----------------------------------------------------------------------
# Squash Pipeline Test - no stalls
#-----------------------------------------------------------------------
# Squash cannot be tested with random delays currently.
#
# Modeling;
#
# t0 A B C D E
# t1   A B - - -
# t2     A - - - -
# t3       A B C D E
# t4         A - - - -

src_squash_msgs = [
    mk_req( 0, 0, STAGE_C, 1 ),
    mk_req( 0, 0,       0, 2 ),
    mk_req( 0, 0,       0, 3 ),
    mk_req( 0, 0, STAGE_B, 4 ),
    mk_req( 0, 0,       0, 5 ),
  ]

sink_squash_msgs = [
    4,
    #5, squashed
    #6, squashed
    7,
    #8, squashed
  ]

def test_squash_pipe( dump_vcd, test_verilog ):
  run_incr_pipe_test( dump_vcd, src_squash_msgs, sink_squash_msgs,
                      IncrPipe, 0, 0, test_verilog )
