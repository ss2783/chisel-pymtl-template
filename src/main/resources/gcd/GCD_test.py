from GCD import GCD
from pymtl import *

if __name__ == "__main__":

  model = GCD()
  model.elaborate()
  model.vcd_file = "gcd.vcd"

  sim = SimulationTool( model )
  sim.reset()

  sim.cycle()

  model.in_value1.value         = 15
  model.in_value2.value         = 5
  model.in_loading_values.value = 1

  sim.cycle()

  model.in_loading_values.value = 0

  while not model.out_valid:
    sim.cycle()

  from fractions import gcd
  ## FIXME ##
  assert model.out_value.value == gcd( 15, 5 ) + 1
