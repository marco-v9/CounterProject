/*
 * Copyright (c) 2024 Marco
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

    // map user controls onto wrapper pins
    wire count_en  = ui_in[0];     // 1 = count
    wire count_up  = ui_in[1];     // 1 = up, 0 = down
    wire do_load   = ui_in[2];     // 1 = load uio_in on next clock
    wire drive_out = ui_in[3];     // 1 = drive uo_out with counter; else 0s
    
    reg [7:0] count_q;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count_q <= 8'd0;
        end 

        else if (ena && do_load) begin
            count_q <= uio_in;
        end 
        
        else if (ena && count_en) begin
            if (count_up)
                count_q <= count_q + 8'd1;
            else
                count_q <= count_q - 8'd1;
        end
    end

    // tri-state outputs 
    assign uo_out = (ena && drive_out) ? count_q : 8'h00;
    
    // All output pins must be assigned. If not used, assign to 0.
    assign uio_out = 8'h00;
    assign uio_oe  = 8'h00;

  // List all unused inputs to prevent warnings
    wire _unused = &{1'b0};

endmodule
