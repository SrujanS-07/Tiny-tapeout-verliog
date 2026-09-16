# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1

    dut._log.info("Test Full Adder behavior")

    # Loop through all 8 possible combinations of A, B, and Cin
    for a in range(2):
        for b in range(2):
            for cin in range(2):
                # Map inputs: ui_in[0] = A, ui_in[1] = B, ui_in[2] = Cin
                dut.ui_in.value = (cin << 2) | (b << 1) | a

                # Wait for one clock cycle
                await ClockCycles(dut.clk, 1)

                # Calculate expected outputs
                expected_sum = a ^ b ^ cin
                expected_cout = (a & b) | (cin & (a ^ b))
                expected_uo_out = (expected_cout << 1) | expected_sum

                # Log and assert
                dut._log.info(f"Testing A={a}, B={b}, Cin={cin} -> Expected [Cout, Sum]: {expected_uo_out}, Got: {dut.uo_out.value.integer}")
                assert dut.uo_out.value == expected_uo_out, \
                    f"Mismatch! A={a}, B={b}, Cin={cin} -> Expected {expected_uo_out}, got {dut.uo_out.value.integer}"

    dut._log.info("All Full Adder test cases passed successfully!")
