from pymtl import *

class PipeCtrl( VerilogModel ):
  def __init__( s ):
    s.pvalid      = InPort ( 1 )
    s.nstall      = InPort ( 1 )
    s.nsquash     = InPort ( 1 )
    s.ostall      = InPort ( 1 )
    s.osquash     = InPort ( 1 )
    s.nvalid      = OutPort ( 1 )
    s.pstall      = OutPort ( 1 )
    s.psquash     = OutPort ( 1 )
    s.pipereg_en  = OutPort ( 1 )
    s.pipereg_val = OutPort ( 1 )
    s.pipe_go     = OutPort ( 1 )

    s.set_ports({
      'clock'             : s.clk,
      'reset'             : s.reset,
      'io_pvalid'         : s.pvalid,
      'io_nstall'         : s.nstall,
      'io_nsquash'        : s.nsquash,
      'io_ostall'         : s.ostall,
      'io_osquash'        : s.osquash,
      'io_nvalid'         : s.nvalid,
      'io_pstall'         : s.pstall,
      'io_psquash'        : s.psquash,
      'io_pipereg_en'     : s.pipereg_en,
      'io_pipereg_val'    : s.pipereg_val,
      'io_pipe_go'        : s.pipe_go
    })


