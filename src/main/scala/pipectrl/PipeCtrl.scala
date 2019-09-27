//======================================================================
// PipeCtrl
//======================================================================
//
// A generic pipeline control-unit that manages the stall and squash
// control signals for a single pipeline stage.
//
//   Inputs
//   ------
//
//   pvalid  : Valid bit coming from the previous stage
//   nstall  : Stall signal originating from the next stage
//   nsquash : Squash signal originating from the next stage
//   ostall  : Stall signal originating from the current pipeline stage
//   osquash : Squash signal originating from the current pipeline stage
//
//   Outputs
//   -------
//
//   nvalid      : Valid bit calculation for the next stage
//   pstall      : Aggregate stall signal for the previous stage
//   psquash     : Aggregate squash signal for the previous stage
//   pipereg_en  : Enable Signal for all the pipeline registers at the
//                 begining of current pipeline stage
//   pipereg_val : Combinational valid bit value of the current stage
//   pipe_go     : Go signal to perform the current pipeline stage
//                 transaction
//
// NOTE: This is inspired from earlier implementations in Verilog/PyMTL
//
// Author : Shreesha Srinath
// Date   : September 26th, 2019


package pipectrl

import chisel3._
import chisel3.util._

class PipeCtrl extends Module {
  val io = IO(new Bundle {
    val pvalid      = Input(Bool())
    val nstall      = Input(Bool())
    val nsquash     = Input(Bool())
    val ostall      = Input(Bool())
    val osquash     = Input(Bool())
    val nvalid      = Output(Bool())
    val pstall      = Output(Bool())
    val psquash     = Output(Bool())
    val pipereg_en  = Output(Bool())
    val pipereg_val = Output(Bool())
    val pipe_go     = Output(Bool())
  })

  // current pipeline stage valid register
  val val_reg_en = Wire(Bool())
  val val_reg = RegEnable(io.pvalid, false.B, val_reg_en)

  // combinationally output the valid-bit register to the datapath
  io.pipereg_val := val_reg

  // Insert 'nop' into the pipeline when current stage is either:
  // (a) squashed by the next stage
  // (b) stalled by the next stage
  // (c) stalled originated in the current stage
  // Else pipeline the valid-bit
  when(io.nsquash || io.nstall || io.ostall) {
    io.nvalid := false.B
  }.otherwise {
    io.nvalid := val_reg
  }

  // Enable the pipeline registers when current stage is squashed
  // by the previous stage or when the current stage is not stalling
  io.pipereg_en := io.nsquash || !(io.nstall || io.ostall)
  val_reg_en := io.nsquash || !(io.nstall || io.ostall)

  // Set pipego to be true when the current stage is valid and
  // is not squashed by the next stage and is not stalled
  io.pipe_go := val_reg && !io.nsquash && !io.nstall && !io.ostall

  // Accumulate the stall and squash signals
  io.pstall  := (io.nstall  || io.ostall)
  io.psquash := (io.nsquash || io.osquash)
}

object PipeCtrlMain extends App {
  chisel3.Driver.execute(args, () => new PipeCtrl)
}
