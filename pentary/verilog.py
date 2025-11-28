"""
Verilog simulation helpers for PNPU architecture.

Provides Python wrappers and utilities for simulating the PNPU
shift-add MAC operations described in the whitepaper.
"""

from typing import List, Tuple
from .pnpu import ShiftAddMAC, PNPUCore


def generate_verilog_mac_module(data_width: int = 16) -> str:
    """
    Generate Verilog code for the PNPU shift-add MAC module.
    
    This matches the Verilog code from the whitepaper.
    
    Args:
        data_width: Bit width for activation data
    
    Returns:
        Verilog module code as string
    """
    verilog_code = f"""module pentary_mac #(
    parameter DATA_WIDTH = {data_width}
)(
    input clk,
    input rst,
    input signed [DATA_WIDTH-1:0] activation_in,
    input signed [2:0] weight_in, // Values: 010(+2), 001(+1), 000(0), 111(-1), 110(-2)
    output reg signed [31:0] accumulator_out
);

    reg signed [DATA_WIDTH:0] product;

    always @(*) begin
        case (weight_in)
            3'sb000: product = 0;                   // Multiply by 0
            3'sb001: product = activation_in;       // Multiply by 1
            3'sb010: product = activation_in <<< 1; // Multiply by 2 (Shift)
            3'sb111: product = -activation_in;      // Multiply by -1
            3'sb110: product = -(activation_in <<< 1); // Multiply by -2
            default: product = 0;
        endcase
    end

    always @(posedge clk or posedge rst) begin
        if (rst) accumulator_out <= 0;
        else accumulator_out <= accumulator_out + product;
    end
endmodule
"""
    return verilog_code


def simulate_verilog_mac(activations: List[int], weights: List[int]) -> List[int]:
    """
    Simulate the Verilog MAC module behavior in Python.
    
    Args:
        activations: List of activation values
        weights: List of weight values (-2, -1, 0, 1, or 2)
    
    Returns:
        List of accumulator outputs
    """
    if len(activations) != len(weights):
        raise ValueError("Activations and weights must have same length")
    
    mac = ShiftAddMAC()
    outputs = []
    
    for activation, weight in zip(activations, weights):
        mac.mac(activation, weight)
        outputs.append(mac.get_accumulator())
    
    return outputs


def generate_testbench(module_name: str = "pentary_mac", data_width: int = 16) -> str:
    """
    Generate a Verilog testbench for the PNPU MAC module.
    
    Args:
        module_name: Name of the module to test
        data_width: Bit width for activation data
    
    Returns:
        Verilog testbench code as string
    """
    testbench = f"""`timescale 1ns / 1ps

module {module_name}_tb;

    // Parameters
    parameter DATA_WIDTH = {data_width};
    parameter CLK_PERIOD = 10;

    // Signals
    reg clk;
    reg rst;
    reg signed [DATA_WIDTH-1:0] activation_in;
    reg signed [2:0] weight_in;
    wire signed [31:0] accumulator_out;

    // Instantiate DUT
    {module_name} #(
        .DATA_WIDTH(DATA_WIDTH)
    ) dut (
        .clk(clk),
        .rst(rst),
        .activation_in(activation_in),
        .weight_in(weight_in),
        .accumulator_out(accumulator_out)
    );

    // Clock generation
    always #(CLK_PERIOD/2) clk = ~clk;

    // Test sequence
    initial begin
        $dumpfile("{module_name}_tb.vcd");
        $dumpvars(0, {module_name}_tb);
        
        // Initialize
        clk = 0;
        rst = 1;
        activation_in = 0;
        weight_in = 0;
        
        // Reset
        #(CLK_PERIOD * 2);
        rst = 0;
        
        // Test cases
        // Test 1: Multiply by +2 (shift left)
        activation_in = 10;
        weight_in = 3'sb010; // +2
        #CLK_PERIOD;
        $display("Test 1: 10 * +2 = %d", accumulator_out);
        
        // Test 2: Multiply by -1
        activation_in = 20;
        weight_in = 3'sb111; // -1
        #CLK_PERIOD;
        $display("Test 2: 20 * -1 = %d", accumulator_out);
        
        // Test 3: Multiply by 0
        activation_in = 30;
        weight_in = 3'sb000; // 0
        #CLK_PERIOD;
        $display("Test 3: 30 * 0 = %d", accumulator_out);
        
        // Test 4: Sequence of operations
        activation_in = 5;
        weight_in = 3'sb001; // +1
        #CLK_PERIOD;
        $display("Test 4a: 5 * +1 = %d", accumulator_out);
        
        activation_in = 10;
        weight_in = 3'sb010; // +2
        #CLK_PERIOD;
        $display("Test 4b: 10 * +2, acc = %d", accumulator_out);
        
        activation_in = 15;
        weight_in = 3'sb110; // -2
        #CLK_PERIOD;
        $display("Test 4c: 15 * -2, acc = %d", accumulator_out);
        
        #(CLK_PERIOD * 2);
        $finish;
    end

endmodule
"""
    return testbench


def weight_to_verilog_code(weight: int) -> str:
    """
    Convert a weight value to Verilog 3-bit signed code.
    
    Args:
        weight: Weight value (-2, -1, 0, 1, or 2)
    
    Returns:
        Verilog code string (e.g., "3'sb010")
    """
    weight_map = {
        2: "3'sb010",   # +2
        1: "3'sb001",   # +1
        0: "3'sb000",   # 0
        -1: "3'sb111",  # -1
        -2: "3'sb110",  # -2
    }
    
    if weight not in weight_map:
        raise ValueError(f"Invalid weight value: {weight}. Must be -2, -1, 0, 1, or 2")
    
    return weight_map[weight]
