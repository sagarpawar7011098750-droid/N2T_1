import sys
import os

COMP_TABLE = {
    "0": "0101010",   "1": "0111111",   "-1": "0111010",
    "D": "0001100",   "A": "0110000",   "M": "1110000",
    "!D": "0001101",  "!A": "0110001",  "!M": "1110001",
    "-D": "0001111",  "-A": "0110011",  "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "A+D": "0000010",
    "D+M": "1000010", "M+D": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "A&D": "0000000",
    "D&M": "1000000", "M&D": "1000000",
    "D|A": "0010101", "A|D": "0010101",
    "D|M": "1010101", "M|D": "1010101"
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def assemble(asm_path):
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }
    for i in range(16):
        symbols[f"R{i}"] = i

    labels = {}
    variables = {}

    # Read and strip comments and whitespace
    with open(asm_path, "r") as f:
        raw_lines = f.readlines()

    clean_lines = []
    for line in raw_lines:
        line = line.split("//")[0].strip()
        if line:
            clean_lines.append(line)

    # Pass 1: Record label ROM addresses
    rom_addr = 0
    instructions = []
    for line in clean_lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            symbols[label] = rom_addr
            labels[label] = rom_addr
        else:
            instructions.append(line)
            rom_addr += 1

    # Pass 2: Translate instructions and allocate variables starting at RAM 16
    next_ram = 16
    binary_lines = []

    for inst in instructions:
        if inst.startswith("@"):
            symbol = inst[1:].strip()
            if symbol.isdigit():
                addr = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_ram
                    variables[symbol] = next_ram
                    next_ram += 1
                addr = symbols[symbol]
            binary_lines.append(f"0{addr:015b}")
        else:
            dest, rest = ("", inst)
            if "=" in inst:
                dest, rest = inst.split("=", 1)
            comp, jump = (rest, "")
            if ";" in rest:
                comp, jump = rest.split(";", 1)

            c_bits = COMP_TABLE[comp.strip()]
            d_bits = DEST_TABLE[dest.strip()]
            j_bits = JUMP_TABLE[jump.strip()]
            binary_lines.append(f"111{c_bits}{d_bits}{j_bits}")

    # Write .hack output
    hack_path = os.path.splitext(asm_path)[0] + ".hack"
    with open(hack_path, "w") as f:
        f.write("\n".join(binary_lines) + "\n")

    # Extra Feature (K = 63, K mod 3 == 0): Save labels and variables to symbols.txt
    with open("symbols.txt", "w") as f:
        f.write("=== LABELS (ROM Addresses) ===\n")
        for k, v in labels.items():
            f.write(f"{k}: {v}\n")
        f.write("\n=== VARIABLES (RAM Addresses) ===\n")
        for k, v in variables.items():
            f.write(f"{k}: {v}\n")

    print(f"Assembled {hack_path} successfully and saved symbols.txt.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)
    assemble(sys.argv[1])