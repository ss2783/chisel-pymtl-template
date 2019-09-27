Chisel-PyMTL Project Template
=============================

This is an example project that shows how to use Chisel for RTL generation
and PyMTL for testing.

[Chisel](https://github.com/freechipsproject/chisel3) is a DSL in Scala
that is used for describing hardware circuits.
[Rocket-Chip](https://github.com/chipsalliance/rocket-chip) and
[BOOM](https://github.com/riscv-boom/riscv-boom) are two popular examples
of projects that use Chisel.


[PyMTL](https://github.com/cornell-brg/pymtl) is a Python-based framework
for multi-level hardware modeling. PyMTL can be used to model hardware at
function-level (FL), [cycle-level
(CL)](https://github.com/cornell-ece5745/ece5745-sec-pymtl-cl/blob/master/README.md),
and register-transfer-level (RTL). PyMTL can be used with [HLS
frameworks](https://github.com/cornell-brg/pymtl-tut-hls/blob/master/README.md)
and with [ASIC
flows.](http://www.csl.cornell.edu/courses/ece5745/handouts/ece5745-tut-asic-new.pdf)

## Why a Chisel-PyMTL Project Template?

PyMTL is incredibly useful for incremental refinement of a hardware model.
For example, to develop a simple inorder processor pipeline one can start
with an FL model, add loose-timing to the pipeline refining it to a CL
model, and finally implement the RTL model. While the processor pipeline is
in development the processor model be it FL/CL/RTL can interact with
cache/main-memory that is entirely in FL/CL. This aids in the agile
development of the processor pipeline. Further, writing test harnesses in
Python is easy, productive, and fun!

Chisel generated hardware circuits can be imported in PyMTL thereby
allowing designers to productively verify the generated hardware. A
designer can implement an FL or CL model of a hardware circuit, develop
tests, and explore the design-space in PyMTL and use the developed tests to
Chisel RTL. Another opportunity arises in developing cosimulation
frameworks where the reference models can be in Python whereas the RTL is
derived from Chisel.

## Show me how this works

This project shows two examples of verifying Chisel generated circuits
using the PyMTL framework. The first example covers a simple GCD circuit
and the second example shows how to verify a simple 5-stage incrementer
pipeline. The incrementer pipeline shows how to import Chisel-generated
control-logic and processes transactions by incrementing them as they pass
a 5-stage pipeline that can either stall or squash based on the injected
transactions.

### Installing PyMTL

Follow the steps below to first PyMTL using a virtualenv.

NOTE: This project currently uses PyMTLv2 which is an older and stable
version of PyMTL. Follow this [page](https://github.com/cornell-brg/pymtl) for PyMTL prerequisites.
For the latest version of PyMTL checkout [Mamba](https://github.com/cornell-brg/pymtl3)

```sh
mkdir -p $HOME/venvs/pymtl
virtualenv --python=python2.7 $HOME/venvs/pymtl
source $HOME/venvs/pymtl/bin/activate
```
Clone PyMTL to some location of your choice

```sh
git clone https://github.com/cornell-brg/pymtl
cd pymtl
pip install --editable .[pymtl]
pip install --upgrade pytest
```

### Trying the GCD example

Execute the script below and follow the steps listed in the output

```sh
./scripts/build-gcd -h
./scripts/build-gcd -b
```

Fix the error for the simple GCD test!

NOTE: Admittedly, I can improve this with a build system and also, I need
to figure out the sbt-style organization for the PyMTL scripts.

## Development/Bug Fixes

If you have bug fixes or changes you would like to see incorporated in this
repo, please checkout the master branch and submit pull requests against
it.

Following things are missing:

  - Use make/scons/doit to automate the builds
  - Improve coding conventions
  - More documentation!

## License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
