from pymtl import *

class GCD( VerilogModel ):

  def __init__( s ):
    s.in_value1         = InPort ( 16 )
    s.in_value2         = InPort ( 16 )
    s.in_loading_values = InPort ( 1  )
    s.out_value         = OutPort( 16 )
    s.out_valid         = OutPort( 1  )

    s.set_ports({
      'clock'             : s.clk,
      'reset'             : s.reset,
      'io_value1'         : s.in_value1,
      'io_value2'         : s.in_value2,
      'io_loadingValues'  : s.in_loading_values,
      'io_outputGCD'      : s.out_value,
      'io_outputValid'    : s.out_valid
    })


