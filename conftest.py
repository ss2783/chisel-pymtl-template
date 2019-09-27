import pytest

def pytest_addoption(parser):
  parser.addoption( "--dump-vcd", action="store_true",
                    help="dump vcd for each test" )
  parser.addoption( "--dump-asm", action="store_true",
                    help="dump asm file for each test" )
  parser.addoption( "--dump-bin", action="store_true",
                    help="dump binary file for each test" )
  parser.addoption( "--test-verilog", action="store_true",
                    help="run verilog translation" )
@pytest.fixture
def dump_vcd(request):
  """Dump VCD for each test."""
  if request.config.option.dump_vcd:
    test_module = request.module.__name__
    test_name   = request.node.name
    return '{}.{}.vcd'.format( test_module, test_name )
  else:
    return ''

@pytest.fixture
def dump_asm(request):
  """Dump Assembly File for each test."""
  return request.config.option.dump_asm

@pytest.fixture
def dump_bin(request):
  """Dump Binary File for each test."""
  return request.config.option.dump_bin

@pytest.fixture
def test_verilog(request):
  """Test Verilog translation rather than python."""
  return request.config.option.test_verilog

@pytest.fixture
def preparse(config, args):
  """Don't write *.pyc and __pycache__ files."""
  import sys
  sys.dont_write_bytecode = True

@pytest.fixture
def setup(item):
  test_verilog = item.config.option.test_verilog
  if test_verilog and 'test_verilog' not in item.funcargnames:
    pytest.skip("ignoring non-Verilog tests")
