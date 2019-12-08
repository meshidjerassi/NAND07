STCK_ACCESS_STR = "@SP\nA=M-1\n"

BIN_MATH_OPS = {"and": "M=D&M", "or": "M=D|M", "add": "M=D+M", "sub": "D=-D\nM=D+M"}
UNI_MATH_OPS = {"not": "!", "neg": "-"}
LOGIC_OPS = {"eq": ("FALSE", "FALSE", "EQ"), "lt": ("FALSE", "TRUE", "LT"), "gt": ("TRUE", "FALSE", "GT")}

BIN_MATH_STR = "D=M\n@SP\nM=M-1\nA=M-1\n"
UNI_MATH_STR = "M = {}M\n"
LOGIC_STR = "D=M\n@R13//y\nM=D\n@SP\nM=M-1\nA=M-1\nD=M\n@R14//x\nM=D\n\n" \
            "@NEG_X#\nD;JLT\n@R13\nD=M\n@{0}#\nD;JLT\n@COMPARE#\n0;JMP\n\n" \
            "(NEG_X#)\n@R13\nD=M\n@{1}#\nD;JGT\n@COMPARE#\n0;JMP\n\n" \
            "(COMPARE#)\n@R14\nD=M\n@R13\nD=D-M\n@TRUE#\nD;J{2}\n@FALSE#\n0;JMP\n\n" \
            "(FALSE#)\n@SP\nA=M-1\nM=0\n@END#\n0;JMP\n(TRUE#)\n@SP\nA=M-1\nM=-1\n(END#)\n"

HEAP = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
CONST_RAM = {"pointer": 3, "temp": 5}

POP_STR_1 = STCK_ACCESS_STR + "D=M\n@R13\nM=D\n@SP\nM=M-1\n"
POP_STR_2 = "@R14\nM=D\n@R13\nD=M\n@R14\nA=M\nM=D\n"
HEAP_CRAM_POP_STR = "@{}\nD={}\n@{}\nD=A+D\n"
STATIC_POP_STR = "@{}.{}\nD=A\n"

PUSH_STR = "D={}\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
HEAP_CRAM_PUSH_STR = "@{}\nD={}\n@{}\nA=A+D\n"
STATIC_PUSH_STR = "@{}.{}\n"

COMMENT = "//"
NEW_LINE = "\n"
TAB = "\t"

C_PUSH = "push"
C_POP = "pop"
C_ARITHMETIC = "arithmetic"
STACK_CMD = (C_PUSH, C_POP)
MATH_CMD = {*BIN_MATH_OPS, *UNI_MATH_OPS, *LOGIC_OPS}
SEG = {*HEAP, *CONST_RAM, "constant", "static"}

