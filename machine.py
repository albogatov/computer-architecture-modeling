"""CPU emulation"""
import logging
import re
import sys
from isa import read_code
from mc import MC, default_mc_memory

logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


class CommandMemory:
    """Command memory"""

    def __init__(self, sz):
        assert sz > 0, "Memory size should be non-zero"
        self.mem = [0 for _ in range(sz)]
        self.size = sz
        self.input_mapping_addr = sz - 2
        self.output_mapping_addr = sz - 1
        self.available_memory_end_excluded = sz - 2

    def read(self, addr):
        assert 0 <= addr < self.size, "Invalid address"
        return self.mem[addr]


class DataMemory:
    """Data memory"""

    def __init__(self, sz, input_buffer):
        assert sz > 0, "Memory size should be non-zero"
        self.mem = [0 for _ in range(sz)]
        self.size = sz
        self.input_buffer = input_buffer
        self.output_buffer = []
        self.input_mapping_addr = sz - 2
        self.output_mapping_addr = sz - 1
        self.available_memory_end_excluded = sz - 2

    def write(self, value, addr):
        assert 0 <= addr < self.size, "Invalid address"
        self.mem[addr] = value

    def read(self, addr):
        assert 0 <= addr < self.size, "Invalid address"
        return self.mem[addr]


acc_mux_sigs = {
    MC.ACC_MUX_ALU: 0,
    MC.ACC_MUX_MEM: 1,
    MC.ACC_MUX_INPUT: 2
}

ip_mux_sigs = {
    MC.IP_MUX_INC: 0,
    MC.IP_MUX_INSTR_ADDR_PART: 1
}

addr_mux_sigs = {
    MC.ADDR_MUX_ACC: 0,
    MC.ADDR_MUX_INSTR_ADDR_PART: 1
}

alu_left_mux_sigs = {
    MC.ALU_LEFT_MUX_ZERO: 0,
    MC.ALU_LEFT_MUX_ACC: 1
}

alu_right_mux_sigs = {
    MC.ALU_RIGHT_MUX_ZERO: 0,
    MC.ALU_RIGHT_MUX_MEM: 1
}


class DataPath:
    """Data path"""

    def __init__(self, code_memory, data_memory):
        self.allowed_max = 2 ** 31 - 1
        self.allowed_min = -2 ** 31

        self.code_memory = code_memory
        self.data_memory = data_memory

        self.acc = 0
        self.addr = 0
        self.ip = 0
        self.instr = {"opcode": "NO_INSTR", "args": []}

        self.alu = 0
        self.z = 0
        self.n = 0

        self.alu_right_mux = 0
        self.alu_left_mux = 0
        self.acc_mux = 0
        self.ip_mux = 0
        self.addr_mux = 0
        self.mem_mux = 0

    def output(self):
        symbol = self.acc
        self.data_memory.output_buffer.append(symbol)

    def fetch_instr(self):
        self.instr = self.code_memory.read(self.ip)

    def write_acc_into_mem(self):
        self.data_memory.write(self.acc, self.addr)

    def acc_output(self):
        self.output()

    def acc_mux_sig(self, mc):
        self.acc_mux = acc_mux_sigs[mc]

    def ip_mux_sig(self, mc):
        self.ip_mux = ip_mux_sigs[mc]

    def addr_mux_sig(self, mc):
        self.addr_mux = addr_mux_sigs[mc]

    def acc_latch(self):
        if self.acc_mux == acc_mux_sigs[MC.ACC_MUX_ALU]:
            self.acc = self.alu
        elif self.acc_mux == acc_mux_sigs[MC.ACC_MUX_MEM]:
            self.acc = self.data_memory.read(self.addr)
        elif self.acc_mux == acc_mux_sigs[MC.ACC_MUX_INPUT]:
            if len(self.data_memory.input_buffer) == 0:
                raise EOFError()
            symbol = self.data_memory.input_buffer.pop(0)
            symbol_code = ord(symbol)
            assert 0 <= symbol_code <= 127, \
                "input character is out of bound: {}".format(symbol_code)
            self.acc = symbol

    def ip_latch(self):
        if self.ip_mux == ip_mux_sigs[MC.IP_MUX_INC]:
            self.ip = self.ip + 1
        elif self.ip_mux == ip_mux_sigs[MC.IP_MUX_INSTR_ADDR_PART]:
            self.ip = self.instr["args"][0]

    def addr_latch(self):
        if self.addr_mux == addr_mux_sigs[MC.ADDR_MUX_ACC]:
            self.addr = self.acc
        if self.addr_mux == addr_mux_sigs[MC.ADDR_MUX_INSTR_ADDR_PART]:
            self.addr = self.instr["args"][0]

    def register_latch(self, mc):
        if mc == MC.ACC_LATCH:
            self.acc_latch()
        elif mc == MC.IP_LATCH:
            self.ip_latch()
        elif mc == MC.ADDR_LATCH:
            self.addr_latch()

    def alu_mux_sig(self, mc):
        if mc in {MC.ALU_RIGHT_MUX_ZERO, MC.ALU_RIGHT_MUX_MEM}:
            self.alu_right_mux = alu_right_mux_sigs[mc]
        elif mc in {MC.ALU_LEFT_MUX_ZERO, MC.ALU_LEFT_MUX_ACC}:
            self.alu_left_mux = alu_left_mux_sigs[mc]

    def alu_overflow_process(self, operand):
        if operand > self.allowed_max or operand < self.allowed_min:
            operand = self.allowed_max & operand
        return operand

    def alu_calc(self, mc):
        left_op = 0 if self.alu_left_mux == 0 else self.acc
        if isinstance(left_op, str):
            left_op = ord(left_op[0])
        right_op = 0 if self.alu_right_mux == 0 else self.data_memory.read(self.addr)
        if isinstance(right_op, str):
            right_op = ord(right_op[0])
        res = left_op | right_op
        if mc == MC.ALU_SUB:
            res = left_op - right_op
        elif mc == MC.ALU_ADD:
            res = left_op + right_op
        elif mc == MC.ALU_INC:
            res = left_op + 1
        elif mc == MC.ALU_SH:
            res = left_op << 0x01
        res = self.alu_overflow_process(res)
        self.alu = res
        self.z = 1 if (res == 0) else 0
        self.n = 1 if (res > 0) else 0


class ControlUnit:
    """Control unit"""

    def __init__(self, mc_memory, data_path, code, data):
        assert len(code) < data_path.code_memory.available_memory_end_excluded, \
            "Prog & data is too big"
        assert len(mc_memory) > 1, "Invalid mc mem initialization"
        self.data_path = data_path
        self.mc_memory = mc_memory
        self.mc_pointer = 0
        self.program_entry = self.load_module(code, self.data_path.code_memory)
        self.data_entry = self.load_module(data, self.data_path.data_memory)
        self.data_path.ip = self.program_entry
        self._tick = 0

    def load_module(self, code, mem):
        sz = len(code)
        assert sz <= mem.size - 2, "Not enough memory"
        program_entry = -1
        for i in range(len(code)):
            if program_entry == -1:
                if isinstance(code[i], dict):
                    program_entry = i
            mem.mem[i] = code[i]
        return program_entry

    def inc_mc_pointer(self):
        self.mc_pointer += 1

    def try_set_mc_pointer(self, new_pos, cond):
        if cond:
            self.mc_pointer = new_pos
        else:
            self.inc_mc_pointer()

    def mc_process(self):
        mc = self.mc_memory[self.mc_pointer]

        if mc["opcode"] in {MC.Z_SET_GOTO, MC.GOTO,
                            MC.CMP_INSTR_NOT_EQ_GOTO, MC.CMP_INSTR_ARG_NOT_EQ_GOTO, MC.N_SET_GOTO}:
            cond = False
            if mc["opcode"] is MC.Z_SET_GOTO:
                cond = self.data_path.z == 1
            elif mc["opcode"] is MC.N_SET_GOTO:
                cond = self.data_path.n == 1
            elif mc["opcode"] is MC.GOTO:
                cond = True
            elif mc["opcode"] is MC.CMP_INSTR_NOT_EQ_GOTO:
                cond = mc["args"][0].name != self.data_path.instr["opcode"]
            elif mc["opcode"] is MC.CMP_INSTR_ARG_NOT_EQ_GOTO:
                cond = mc["args"][0] != self.data_path.instr["args"][0]
            self.try_set_mc_pointer(mc["args"][-1], cond)
        else:
            if mc["opcode"] is MC.INSTRUCTION_FETCH:
                self.data_path.fetch_instr()
            elif mc["opcode"] in {MC.ALU_RIGHT_MUX_ZERO, MC.ALU_RIGHT_MUX_MEM,
                                  MC.ALU_LEFT_MUX_ZERO, MC.ALU_LEFT_MUX_ACC}:
                self.data_path.alu_mux_sig(mc["opcode"])
            elif mc["opcode"] in {MC.ALU_SUB, MC.ALU_ADD, MC.ALU_INC, MC.ALU_SH}:
                self.data_path.alu_calc(mc["opcode"])
            elif mc["opcode"] in {MC.ACC_MUX_ALU, MC.ACC_MUX_MEM, MC.ACC_MUX_INPUT}:
                self.data_path.acc_mux_sig(mc["opcode"])
            elif mc["opcode"] is MC.ACC_WRITE:
                self.data_path.write_acc_into_mem()
            elif mc["opcode"] is MC.ACC_OUTPUT:
                self.data_path.acc_output()
            elif mc["opcode"] in {MC.IP_MUX_INC, MC.IP_MUX_INSTR_ADDR_PART}:
                self.data_path.ip_mux_sig(mc["opcode"])
            elif mc["opcode"] in {MC.ADDR_MUX_ACC, MC.ADDR_MUX_INSTR_ADDR_PART}:
                self.data_path.addr_mux_sig(mc["opcode"])
            elif mc["opcode"] in {MC.ACC_LATCH, MC.IP_LATCH, MC.ADDR_LATCH}:
                self.data_path.register_latch(mc["opcode"])
            elif mc["opcode"] is MC.STOP:
                return -1
            elif mc["opcode"] is MC.DECODING_ERR:
                return -2
            self.inc_mc_pointer()
            return mc["tick_num"]

        return mc["tick_num"]

    def decode_and_execute_instruction(self):
        self.mc_pointer = 0
        tick_num = self.mc_process()
        ticks = [tick_num]
        self.tick()
        while tick_num >= 0 and self.mc_pointer > 0:
            tick_num = self.mc_process()
            if tick_num != ticks[-1]:
                logging.debug('%s', self)
                ticks.append(tick_num)
                self.tick()
        if tick_num == -1:
            raise StopIteration()
        if tick_num == -2:
            raise StopIteration("Decoding error occurred")

    def tick(self):
        self._tick += 1

    def current_tick(self):
        return self._tick

    def __repr__(self):
        state = f"{{TICK: {self._tick}, ADDR: {self.data_path.addr}, " \
                f"IP: {self.data_path.ip}, ACC: {self.data_path.acc}, " \
                f"Z: {self.data_path.z}, " \
                f"N: {self.data_path.n}}}"

        instr = self.data_path.instr
        opcode = instr["opcode"]
        arg = instr["args"][0] if len(instr["args"]) > 0 else "no arg"
        action = f"{opcode} {arg}"
        return f"{state} {action}"


def simulation(code, data, input_tokens, data_memory_size, limit):
    command_memory = CommandMemory(data_memory_size)
    data_memory = DataMemory(data_memory_size, input_tokens)
    data_path = DataPath(command_memory, data_memory)
    control_unit = ControlUnit(default_mc_memory, data_path, code, data)
    instr_counter = 0

    try:
        while True:
            assert limit > instr_counter, "too long execution, increase limit!"
            control_unit.decode_and_execute_instruction()
            instr_counter += 1
            logger.debug('%s', control_unit)

    except EOFError:
        logger.debug('%s', control_unit)
        logger.info('Input buffer is empty!')
    except StopIteration:
        instr_counter += 1
        logger.debug('%s', control_unit)
        logger.debug('Iteration stopped by HLT')
    data_memory.output_buffer = [str(i) for i in data_memory.output_buffer]
    return ''.join(data_memory.output_buffer), instr_counter, control_unit.current_tick()


def main(args):
    assert len(args) == 2, "Wrong arguments: machine.py <code_file> <input_file>"
    code_file, input_file = args

    translated_asm = read_code(code_file)
    with open(input_file, encoding="utf-8") as file:
        input_text = file.read()
        input_token = []
        for char in input_text:
            input_token.append(char)
    input_token.append("\0")

    i = 0
    data = []
    while not re.match("{.*", str(translated_asm[i])):
        data.append(translated_asm[i])
        translated_asm[i] = 0
        i += 1
    while translated_asm[0] == 0:
        translated_asm.pop(translated_asm[0])

    output, instr_counter, ticks = simulation(translated_asm, data, input_tokens=input_token,
                                              data_memory_size=100, limit=1000)
    print(output)
    print("instr_counter:", instr_counter, "ticks:", ticks)
    return output


if __name__ == '__main__':
    main(sys.argv[1:])
