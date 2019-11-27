STCK_ACCESS_STR = "@SP\nA=M-1\n"
BIN_MATH_OPS = {"and": "M=D&M", "or": "M=D|M", "add": "M=D+M", "sub": "D=-D\nM=D+M"}
UNI_MATH_OPS = {"not": "!", "neg": "-"}
LOGIC_OPS = {"eq": ("FALSE", "FALSE", "EQ"), "lt": ("FALSE", "TRUE", "LT"), "gt": ("TRUE", "FALSE", "GT")}
BIN_MATH_STR = "D=M\n@SP\nM=M-1\nA=M-1\n"
UNI_MATH_STR = "M = {}M"
LOGIC_STR = "D=M\n@R13//y\nM=D\n@SP\nM=M-1\nA=M-1\nD=M\n@R14//x\nM=D\n\n" \
            "@NEG_X\nD;JLT\n@R13\nD=M\n@{0}\nD;JLT\n@COMPARE\n0;JMP\n\n" \
            "(NEG_X)\n@R13\nD=M\n@{1}\nD;JGT\n@COMPARE\n0;JMP\n\n" \
            "(COMPARE)\n@R14\nD=M\n@R13\nD=D-M\n@TRUE\nD;J{2}\n@FALSE\n0;JMP\n\n" \
            "(FALSE)\n@SP\nA=M-1\nM=0\n@END\n0;JMP\n(TRUE)\n@SP\nA=M-1\nM=-1\n(END)\n"

POP_STR_1 = STCK_ACCESS_STR + "D=M\n@R13\nM=D\n@SP\nM=M-1\n"
POP_STR_2 = "@R14\nM=D\n@R13\nD=M\n@R14\nA=M\nM=D"

HEAP = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
HEAP_CRAM_POP_STR = "@{}\nD={}\n@{}\nD=A+D\n"
CONST_RAM = {"pointer": 3, "temp": 5}
STATIC_POP_STR = "@{}.{}\nD=A"

PUSH_STR = "D={}\n@SP\nA=M\nM=D\n@SP\nM=M+1"
HEAP_CRAM_PUSH_STR = "@{}\nD={}\n@{}\nA=A+D\n"
STATIC_PUSH_STR = "@{}.{}\n"


class CodeWriter:

    def __init__(self, file_name):
        self.file_name = file_name

    def writeArithmetic(self, cmd):
        res = STCK_ACCESS_STR
        if cmd in BIN_MATH_OPS:
            res += BIN_MATH_STR + BIN_MATH_OPS[cmd] + "\n"
        elif cmd in UNI_MATH_OPS:
            res += UNI_MATH_STR.format(UNI_MATH_OPS[cmd])
        else:
            res += LOGIC_STR.format(*LOGIC_OPS[cmd])
        return res

    def writePushPop(self, cmd, seg, i):
        if cmd == "POP":
            res = POP_STR_1
            if seg in HEAP or seg in CONST_RAM:
                if seg in HEAP:
                    seg_str = HEAP[seg]
                    dest = "M"
                else:
                    seg_str = CONST_RAM[seg]
                    dest = "A"
                res += HEAP_CRAM_POP_STR.format(seg_str, dest, i)
            else:
                res += STATIC_POP_STR.format(self.file_name, i)
            res += POP_STR_2
        else:
            if seg in HEAP or seg in CONST_RAM:
                if seg in HEAP:
                    seg_str = HEAP[seg]
                    dest = "M"
                else:
                    seg_str = CONST_RAM[seg]
                    dest = "A"
                res = HEAP_CRAM_PUSH_STR.format(seg_str, dest, i)
                dest2 = "M"
            elif seg == "static":
                res = STATIC_PUSH_STR.format(self.file_name, i)
                dest2 = "M"
            else:
                res = "@" + i
                dest2 = "A"
            res += PUSH_STR.format(dest2)
        return res
