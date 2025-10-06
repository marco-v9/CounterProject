# SPDX-FileCopyrightText: © 2025 Marco
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # 100 kHz clock (period = 10 µs, matches TinyTapeout template)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # reset
    dut.ena.value   = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # load 0x05 into the counter 
    # ui_in[3:0] = 0b0100 → drive_out=0, do_load=1, up=0, count_en=0
    dut.uio_in.value = 0x05
    dut.ui_in.value  = 0b0100
    await ClockCycles(dut.clk, 1)

    # stop loading + make output visible: ui_in[3:0] = 0b1000
    dut.ui_in.value = 0b1000
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 0x05, "load failed"

    # count up by one ----------
    # ui_in[3:0] = 0b1011 → drive_out=1, do_load=0, up=1, count_en=1
    dut.ui_in.value = 0b1011
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 0x05, "count up failed"

    # ---------- float the tri-state bus ----------
    # drive_out=0 so OE should be low
    dut.ui_in.value = 0b0011  # drive_out=0, still counting just for fun
    await ClockCycles(dut.clk, 1)
    assert int(dut.uio_oe.value) == 0x00, "bus should be high-Z now"

    dut._log.info("PASS")
