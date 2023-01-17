"""MC module"""
from enum import Enum
from isa import Opcode


class MC(Enum):
    """Microcode"""
    INSTRUCTION_FETCH = "IN_FETCH"

    ALU_RIGHT_MUX_ZERO = "ALU_RIGHT_MUX_ZERO"
    ALU_RIGHT_MUX_MEM = "ALU_RIGHT_MUX_MEM"

    ALU_LEFT_MUX_ZERO = "ALU_LEFT_MUX_ZERO"
    ALU_LEFT_MUX_ACC = "ALU_LEFT_MUX_ACC"

    ALU_SUB = "ALU_SUB"
    ALU_ADD = "ALU_ADD"
    ALU_INC = "ALU_INC"
    ALU_SH = "ALU_SH"

    ACC_MUX_ALU = "ACC_MUX_ALU"
    ACC_MUX_MEM = "ACC_MUX_MEM"
    ACC_MUX_INPUT = "ACC_MUX_INPUT"

    ACC_WRITE = "ACC_WRITE"

    IP_MUX_INC = "IP_MUX_INC"
    IP_MUX_INSTR_ADDR_PART = "IP_MUX_INSTR_ADDR_PART"

    ADDR_MUX_INSTR_ADDR_PART = "ADDR_MUX_INSTR_ADDR_PART"
    ADDR_MUX_ACC = "ADDR_MUX_ACC"

    ACC_OUTPUT = "ACC_OUTPUT"

    ACC_LATCH = "ACC_LATCH"
    IP_LATCH = "IP_LATCH"
    ADDR_LATCH = "ADDR_LATCH"

    Z_SET_GOTO = "Z_SET_GOTO"
    N_SET_GOTO = "N_SET_GOTO"
    GOTO = "GOTO"
    CMP_INSTR_NOT_EQ_GOTO = "CMP_INSTR_NOT_EQ_GOTO"
    CMP_INSTR_ARG_NOT_EQ_GOTO = "CMP_INSTR_ARG_NOT_EQ_GOTO"

    STOP = "STOP"
    DECODING_ERR = "DECODING_ERR"


default_mc_memory = [

    {"opcode": MC.INSTRUCTION_FETCH, "args": [], "tick_num": 0},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.CMP, 8], "tick_num": 1},

    {"opcode": MC.ADDR_MUX_INSTR_ADDR_PART, "args": [], "tick_num": 1},
    {"opcode": MC.ADDR_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.ALU_RIGHT_MUX_MEM, "args": [], "tick_num": 2},
    {"opcode": MC.ALU_LEFT_MUX_ACC, "args": [], "tick_num": 2},
    {"opcode": MC.ALU_SUB, "args": [], "tick_num": 2},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 2},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.JE, 11], "tick_num": 1},

    {"opcode": MC.Z_SET_GOTO, "args": [72], "tick_num": 1},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 1},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.LD_ABS, 14], "tick_num": 1},

    {"opcode": MC.ACC_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 1},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.LD_REL, 23], "tick_num": 1},

    {"opcode": MC.CMP_INSTR_ARG_NOT_EQ_GOTO, "args": ["AC", 18], "tick_num": 1},
    {"opcode": MC.ADDR_MUX_ACC, "args": [], "tick_num": 1},
    {"opcode": MC.GOTO, "args": [19], "tick_num": 1},
    {"opcode": MC.ADDR_MUX_INSTR_ADDR_PART, "args": [], "tick_num": 1},
    {"opcode": MC.ADDR_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.ACC_MUX_MEM, "args": [], "tick_num": 2},
    {"opcode": MC.ACC_LATCH, "args": [], "tick_num": 2},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 2},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.WR, 28], "tick_num": 1},

    {"opcode": MC.ADDR_MUX_INSTR_ADDR_PART, "args": [], "tick_num": 1},
    {"opcode": MC.ADDR_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.ACC_WRITE, "args": [], "tick_num": 2},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 2},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.INC, 35], "tick_num": 1},

    {"opcode": MC.ALU_LEFT_MUX_ACC, "args": [], "tick_num": 1},
    {"opcode": MC.ALU_RIGHT_MUX_ZERO, "args": [], "tick_num": 1},
    {"opcode": MC.ALU_INC, "args": [], "tick_num": 1},
    {"opcode": MC.ACC_MUX_ALU, "args": [], "tick_num": 1},
    {"opcode": MC.ACC_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 1},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.SH, 44], "tick_num": 1},

    {"opcode": MC.ADDR_MUX_INSTR_ADDR_PART, "args": [], "tick_num": 1},
    {"opcode": MC.ADDR_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.ALU_LEFT_MUX_ACC, "args": [], "tick_num": 2},
    {"opcode": MC.ALU_RIGHT_MUX_MEM, "args": [], "tick_num": 2},
    {"opcode": MC.ALU_SH, "args": [], "tick_num": 2},
    {"opcode": MC.ACC_MUX_ALU, "args": [], "tick_num": 2},
    {"opcode": MC.ACC_LATCH, "args": [], "tick_num": 2},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 2},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.JMP, 46], "tick_num": 1},

    {"opcode": MC.GOTO, "args": [72], "tick_num": 1},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.ADD, 55], "tick_num": 1},

    {"opcode": MC.ADDR_MUX_INSTR_ADDR_PART, "args": [], "tick_num": 1},
    {"opcode": MC.ADDR_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.ALU_LEFT_MUX_ACC, "args": [], "tick_num": 2},
    {"opcode": MC.ALU_RIGHT_MUX_MEM, "args": [], "tick_num": 2},
    {"opcode": MC.ALU_ADD, "args": [], "tick_num": 2},
    {"opcode": MC.ACC_MUX_ALU, "args": [], "tick_num": 2},
    {"opcode": MC.ACC_LATCH, "args": [], "tick_num": 2},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 2},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.OUT, 60], "tick_num": 1},

    {"opcode": MC.ADDR_MUX_INSTR_ADDR_PART, "args": [], "tick_num": 1},
    {"opcode": MC.ADDR_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.ACC_OUTPUT, "args": [], "tick_num": 2},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 2},


    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.IN, 64], "tick_num": 1},

    {"opcode": MC.ACC_MUX_INPUT, "args": [], "tick_num": 1},
    {"opcode": MC.ACC_LATCH, "args": [], "tick_num": 1},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 1},


    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.JG, 67], "tick_num": 1},

    {"opcode": MC.N_SET_GOTO, "args": [72], "tick_num": 1},
    {"opcode": MC.GOTO, "args": [69], "tick_num": 1},

    {"opcode": MC.CMP_INSTR_NOT_EQ_GOTO, "args": [Opcode.HLT, 70], "tick_num": 1},

    {"opcode": MC.GOTO, "args": [76], "tick_num": 1},

    {"opcode": MC.IP_MUX_INC, "args": [], "tick_num": 3},
    {"opcode": MC.IP_LATCH, "args": [], "tick_num": 3},

    {"opcode": MC.GOTO, "args": [0], "tick_num": 3},

    {"opcode": MC.IP_MUX_INSTR_ADDR_PART, "args": [], "tick_num": 3},
    {"opcode": MC.IP_LATCH, "args": [], "tick_num": 3},

    {"opcode": MC.GOTO, "args": [0], "tick_num": 3},

    {"opcode": MC.DECODING_ERR, "args": [], "tick_num": 3},
    {"opcode": MC.STOP, "args": [], "tick_num": 3},

]
