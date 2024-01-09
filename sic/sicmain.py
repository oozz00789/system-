import SIC_Instruction
from collections import defaultdict

def strip_comment(line: str) -> str:
    return line.split('.')[0].strip() if '.' in line else line.strip()

def parse_byte(third: str) -> tuple:
    mode, data = third[0], ""

    if mode == "C":
        data += ''.join([hex(ord(c))[2:] for c in third[2:-1]]).upper()
    elif mode == "X":
        data += third[2:-1]
    else:
        raise ValueError("ERROR BYTE")

    return len(data) // 2, data

def parse_word(third: str) -> tuple:
    value, data = int(third), ""

    if value >= 0:
        data = hex(value)[2:].upper().zfill(6)
    else:
        HEX = "1000000"
        data = hex(int(HEX, 16) + value)[2:].upper().zfill(6)

    return len(data) // 2, data

def parse_resb(third: str) -> tuple:
    return int(third), ""

def parse_resw(third: str) -> tuple:
    return int(third) * 3, ""

def assemble() -> None:
    location, add = 0, 0
    result, func_loc = [], defaultdict(int)

    with open("input.txt", "r", encoding="UTF-8") as inp:
        lines = inp.readlines()

        for line in lines:
            line = strip_comment(line).strip()
            first, second, third, obj_code = "", "", "", ""

            if not line:
                continue

            if location == 0:
                if line.split()[-1] == "START":
                    print("ERROR START")
                    exit()

                location = int(line.split()[-1], 16)
                first, second, third = line.split()[0], line.split()[1], ""

                result.append(["", first, second, third, obj_code])
                continue

            else:
                if len(line.split()) == 1:
                    second = line.split()[0]
                    obj_code = SIC_Instruction.instruction.get(second, "ERROR") + "0000"
                else:
                    tokens = line.split()
                    second = tokens[0] if len(tokens) == 2 else tokens[1]

                    if second in SIC_Instruction.instruction:
                        third = tokens[-1]
                        add = 3

                        if len(tokens) == 3:
                            first = tokens[0]
                            func_loc[first] = location
                    else:
                        if second == "END":
                            add = 0
                            third = tokens[-1]
                        else:
                            first, second, third = tokens[0], tokens[1], tokens[2]
                            func_loc[first] = location

                            if second == "BYTE":
                                add, obj_code = parse_byte(third)
                            elif second == "WORD":
                                add, obj_code = parse_word(third)
                            elif second == "RESB":
                                add, obj_code = parse_resb(third)
                            elif second == "RESW":
                                add, obj_code = parse_resw(third)

            result.append([hex(location)[2:].upper(), first, second, third, obj_code])
            location += add

        for idx in range(len(result)):
            if result[idx][0] == "":
                continue
            elif result[idx][2] in ["END", "BYTE", "WORD", "RESB", "RESW"]:
                continue
            else:
                if not result[idx][4]:
                    if ",X" in result[idx][3]:
                        result[idx][4] = SIC_Instruction.instruction.get(result[idx][2], "ERROR") + hex(func_loc[result[idx][3]] + int("8000", 16))[2:].upper().zfill(4)
                    else:
                        result[idx][4] = SIC_Instruction.instruction.get(result[idx][2], "ERROR") + hex(func_loc[result[idx][3]])[2:].upper()

    with open("output.txt", "w", encoding="UTF-8") as fi:
        for i in range(len(result)):
            fi.write(f"{(i + 1) * 5:<10}{result[i][0].zfill(6):<10}{result[i][1]:<10}{result[i][2]:<10}{result[i][3]:<10}{result[i][4].zfill(6):<10}\n")

if __name__ == "__main__":
    assemble()
