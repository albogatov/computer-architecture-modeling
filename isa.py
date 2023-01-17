"""ISA"""
from enum import Enum
import json


class AsmOpcode(Enum):
    """ASM opcodes"""
    CMP = "CMP"
    JE = "JE"
    LD = "LD"
    WR = "WR"
    INC = "INC"
    JMP = "JMP"
    ADD = "ADD"
    HLT = "HLT"
    IN = "IN"
    OUT = "OUT"
    SH = "SH"
    JG = "JG"


class Opcode(Enum):
    """Opcodes"""
    CMP = "CMP"
    JE = "JE"
    LD_ABS = "LD_ABS"
    LD_REL = "LD_REL"
    IN = "IN"
    OUT = "OUT"
    INC = "INC"
    JMP = "JMP"
    ADD = "ADD"
    HLT = "HLT"
    WR = "WR"
    SH = "SH"
    JG = "JG"


opcode_args = {
    AsmOpcode.CMP.name: 1,
    AsmOpcode.JE.name: 1,
    AsmOpcode.LD.name: 1,
    AsmOpcode.WR.name: 1,
    AsmOpcode.INC.name: 0,
    AsmOpcode.JMP.name: 1,
    AsmOpcode.ADD.name: 1,
    AsmOpcode.HLT.name: 0,
    AsmOpcode.IN.name: 0,
    AsmOpcode.OUT.name: 0,
    AsmOpcode.SH.name: 0,
    AsmOpcode.JG.name: 1
}


def write_code(filename, code):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(code, indent=4))


def read_code(filename):
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())
    return code
