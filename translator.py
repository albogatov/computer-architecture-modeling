"""Translator"""
import logging
import sys
from isa import AsmOpcode, opcode_args, write_code


class IllegalSyntaxException(Exception):
    """Invalid asm exception"""
    def __init__(self, message="Parsing error"):
        self.message = "Invalid asm! " + message
        super().__init__(self.message)


def translate(text):
    data_flag = -1
    labels_searched = {}
    labels_present = {}
    variables_present = {}
    final_code = []

    line_number = 0
    line_number_code = 0

    for line in text.split("\n"):

        terms = line.strip().split(maxsplit=2)
        if len(terms) == 0:
            continue

        command_var_or_label = terms[0].strip()

        if command_var_or_label[-1] == ":":
            if len(terms) != 1:
                raise IllegalSyntaxException("Invalid label usage!")

            if command_var_or_label == ".text:":
                data_flag = 0
            elif command_var_or_label == ".data:":
                data_flag = 1
            else:
                if data_flag == -1:
                    raise IllegalSyntaxException("Section is not set")
                if data_flag == 1:
                    raise IllegalSyntaxException("Label in data section")

                if command_var_or_label in labels_present:
                    raise IllegalSyntaxException("Label duplication")

                label_name = command_var_or_label[:-1]
                labels_present[label_name] = line_number_code
                if label_name in labels_searched:
                    for resolved_line_num in labels_searched[label_name]:
                        ind = final_code[resolved_line_num]["args"].index(label_name)
                        final_code[resolved_line_num]["args"] = \
                            final_code[resolved_line_num]["args"][:ind] \
                            + [line_number_code] \
                            + final_code[resolved_line_num]["args"][
                            ind + 1:]
                    labels_searched.pop(label_name)
        else:
            if data_flag == 1:
                if len(terms) < 3:
                    raise IllegalSyntaxException("Invalid data section")
                variables_present[command_var_or_label] = line_number
                data_type = terms[1].strip()
                data = terms[2].strip()
                if data_type.upper() == "STRING":
                    data = data[1:-1]
                    for i in range(len(data)):
                        final_code.append(data[i])
                    final_code.append("\0")
                    line_number += len(data) + 1
                elif data_type.upper() == "NUM":
                    final_code.append(int(data))
                    line_number += 1
                elif data_type.upper() == "CHAR":
                    if data[0] == "\"" or data[0] == "'":
                        data = data[1:-1]
                    else:
                        data = chr(int(data))
                    final_code.append(data)
                    line_number += 1
                else:
                    raise IllegalSyntaxException("Unknown data type!")

            elif data_flag == 0:

                found = -1
                opcodes = list(AsmOpcode)
                for o in opcodes:

                    command_name = o.value

                    if command_var_or_label.upper() == command_name:
                        if len(terms) != opcode_args[command_name] + 1:
                            raise IllegalSyntaxException("Invalid arg num")
                        args = []
                        found = 1
                        braces = -1

                        if opcode_args[command_name] == 1:
                            arg = terms[1]
                            if arg[0] == "[":
                                arg = arg[1:-1]
                                braces = 1

                            if arg.lower() == "ac":
                                args.append(arg.upper())
                            elif arg in variables_present:
                                args.append(variables_present[arg])
                            elif arg in labels_present:
                                args.append(labels_present[arg])
                            elif arg in labels_searched:
                                labels_searched[arg].append(line_number)
                                args.append(arg)
                            else:
                                labels_searched[arg] = [line_number]
                                args.append(arg)

                        if command_name != "LD" and braces != -1:
                            raise IllegalSyntaxException("Wrong braces usage")

                        if command_name == "OUT":
                            command_name = "OUT"
                            args = [-1]
                        elif command_name == "IN":
                            command_name = "IN"
                            args = [-1]
                        elif command_name == "LD":
                            if braces == -1:
                                command_name = "LD_ABS"
                            else:
                                command_name = "LD_REL"

                        if command_name == "SH":
                            args = [0]

                        if command_name == "LD_ABS" and braces == -1 and args[0] == "AC":
                            raise IllegalSyntaxException("Wrong ac usage in ld command")
                        line_number += 1
                        line_number_code += 1
                        command_binding = {"opcode": command_name, "args": args}
                        final_code.append(command_binding)
                        break
                if found == -1:
                    raise IllegalSyntaxException(f"Unknown command! {command_var_or_label}")
            else:
                raise IllegalSyntaxException("Section is not set")
    if not isinstance(final_code[-1], dict):
        raise IllegalSyntaxException("Code section missed or empty!")
    if len(labels_searched.keys()) != 0:
        raise IllegalSyntaxException("Some labels not found!")
    return final_code


def main(args):
    assert len(args) == 2, \
        "Wrong arguments: translator.py <input_file> <target_file>"
    source, target = args

    with open(source, "rt", encoding="utf-8") as f:
        source = f.read()
    try:
        code = translate(source)
        print("source LoC:", len(source.split("\n")), "code instr:", len(code))
        write_code(target, code)
    except IllegalSyntaxException as e:
        logging.error(e.message)


if __name__ == '__main__':
    main(sys.argv[1:])
