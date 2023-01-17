"""ISA"""
from enum import Enum
import json


class AsmCmd(Enum):
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
    AsmCmd.CMP.name: 1,
    AsmCmd.JE.name: 1,
    AsmCmd.LD.name: 1,
    AsmCmd.WR.name: 1,
    AsmCmd.INC.name: 0,
    AsmCmd.JMP.name: 1,
    AsmCmd.ADD.name: 1,
    AsmCmd.HLT.name: 0,
    AsmCmd.IN.name: 0,
    AsmCmd.OUT.name: 0,
    AsmCmd.SH.name: 0,
    AsmCmd.JG.name: 1
}


def write_code(filename, code):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(code, indent=4))


def read_code(filename):
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())
    return code
