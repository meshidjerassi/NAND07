STCK_ACCESS_STR = "@SP\nA=M-1\n"

BIN_MATH_OPS = {"and": "M=D&M", "or": "M=D|M", "add": "M=D+M", "sub": "D=-D\nM=D+M"}
UNI_MATH_OPS = {"not": "!", "neg": "-"}
LOGIC_OPS = {"eq": ("FALSE", "FALSE", "EQ"), "lt": ("FALSE", "TRUE", "LT"), "gt": ("TRUE", "FALSE", "GT")}

BIN_MATH_STR = "D=M\n@SP\nM=M-1\nA=M-1\n"
UNI_MATH_STR = "M = {}M\n"
LOGIC_STR = "D=M\n@R13//y\nM=D\n@SP\nM=M-1\nA=M-1\nD=M\n@R14//x\nM=D\n\n" \
            "@NEG_X\nD;JLT\n@R13\nD=M\n@{0}\nD;JLT\n@COMPARE\n0;JMP\n\n" \
            "(NEG_X)\n@R13\nD=M\n@{1}\nD;JGT\n@COMPARE\n0;JMP\n\n" \
            "(COMPARE)\n@R14\nD=M\n@R13\nD=D-M\n@TRUE\nD;J{2}\n@FALSE\n0;JMP\n\n" \
            "(FALSE)\n@SP\nA=M-1\nM=0\n@END\n0;JMP\n(TRUE)\n@SP\nA=M-1\nM=-1\n(END)\n"

HEAP = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
CONST_RAM = {"pointer": 3, "temp": 5}

POP_STR_1 = STCK_ACCESS_STR + "D=M\n@R13\nM=D\n@SP\nM=M-1\n"
POP_STR_2 = "@R14\nM=D\n@R13\nD=M\n@R14\nA=M\nM=D\n"
HEAP_CRAM_POP_STR = "@{}\nD={}\n@{}\nD=A+D\n"
STATIC_POP_STR = "@{}.{}\nD=A\n"

PUSH_STR = "D={}\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
HEAP_CRAM_PUSH_STR = "@{}\nD={}\n@{}\nA=A+D\n"
STATIC_PUSH_STR = "@{}.{}\n"


class CodeWriter:
    """
    Translates VM code to ASM, and writes translation to output file
    """

    def __init__(self, output):
        """
        :param output: name of output file ("*.asm")
        """
        self.output = open(output, 'w')
        self.file_name = None

    def setFileName(self, name):
        """
        :param name: name of current .vm file to be translated, used when switching between files in dir.
            file_name is used when pushing/popping static vars
        """
        self.file_name = name
        self.output.write("//translating {}.vm".format(name) + "\n")

    def writeArithmetic(self, cmd):
        """
        writes arithmetic command to output
        :param cmd: vm command
        """
        res = "//{}:\n".format(cmd) + STCK_ACCESS_STR
        if cmd in BIN_MATH_OPS:
            res += BIN_MATH_STR + BIN_MATH_OPS[cmd] + "\n"
        elif cmd in UNI_MATH_OPS:
            res += UNI_MATH_STR.format(UNI_MATH_OPS[cmd])
        else:
            res += LOGIC_STR.format(*LOGIC_OPS[cmd])
        self.output.write(res)

    def writePushPop(self, cmd, seg, i):
        """
        writes push/pop command to output
        :param cmd: type of command - "push"/"pop"
        :param seg: memory segment to work on
        :param i: location within segment/constant value
        """
        res = "//" + " ".join((cmd, seg, str(i))) + "\n"
        res += POP_STR_1 if cmd == "POP" else ""
        if seg in HEAP or seg in CONST_RAM:
            if seg in HEAP:
                seg_str = HEAP[seg]
                dest = "M"
            else:
                seg_str = CONST_RAM[seg]
                dest = "A"
            res += (HEAP_CRAM_POP_STR if cmd == "pop" else HEAP_CRAM_PUSH_STR).format(seg_str, dest, i)
        elif cmd == "pop":
            res += STATIC_POP_STR.format(self.file_name, i)
        else:
            res += STATIC_PUSH_STR.format(self.file_name, i) if seg == "static" else "@{}\n".format(i)
        if cmd == "pop":
            res += POP_STR_2
        else:
            dest2 = "M" if seg == "static" else "A"
            res += PUSH_STR.format(dest2)
        self.output.write(res)

    def close(self):
        """
        close output file after writing
        """
        self.output.close()
