/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // Internal wires for Full Adder inputs
  wire a   = ui_in[0];
  wire b   = ui_in[1];
  wire cin = ui_in[2];

  // Full Adder logic (Combinational)
  wire sum  = a ^ b ^ cin;
  wire cout = (a & b) | (cin & (a ^ b));

  // All output pins must be assigned. Unused outputs are tied to 0.
  assign uo_out  = {6'b000000, cout, sum}; 
  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  // List all unused inputs to prevent synthesis warnings
  wire _unused = &{ena, clk, rst_n, ui_in[7:3], uio_in, 1'b0};

endmodule
