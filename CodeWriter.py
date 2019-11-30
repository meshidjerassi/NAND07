import GlobalConsts as gc


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
        self.counter = 0

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
        res = "//{}:\n".format(cmd) + gc.STCK_ACCESS_STR
        if cmd in gc.BIN_MATH_OPS:
            res += gc.BIN_MATH_STR + gc.BIN_MATH_OPS[cmd] + "\n"
        elif cmd in gc.UNI_MATH_OPS:
            res += gc.UNI_MATH_STR.format(gc.UNI_MATH_OPS[cmd])
        else:
            res += gc.LOGIC_STR.format(*gc.LOGIC_OPS[cmd]).replace("#", str(self.counter))
            self.counter = self.counter + 1
        self.output.write(res + "\n")

    def writePushPop(self, cmd, seg, i):
        """
        writes push/pop command to output
        :param cmd: type of command - "push"/"pop"
        :param seg: memory segment to work on
        :param i: location within segment/constant value
        """
        res = "//" + " ".join((cmd, seg, str(i))) + "\n"
        res += gc.POP_STR_1 if cmd == gc.C_POP else ""
        if seg in gc.HEAP or seg in gc.CONST_RAM:
            if seg in gc.HEAP:
                seg_str = gc.HEAP[seg]
                dest = "M"
            else:
                seg_str = gc.CONST_RAM[seg]
                dest = "A"
            res += (gc.HEAP_CRAM_POP_STR if cmd == gc.C_POP else gc.HEAP_CRAM_PUSH_STR).format(seg_str, dest, i)
        elif cmd == gc.C_POP:
            res += gc.STATIC_POP_STR.format(self.file_name, i)
        else:
            res += gc.STATIC_PUSH_STR.format(self.file_name, i) if seg == "static" else "@{}\n".format(i)
        if cmd == gc.C_POP:
            res += gc.POP_STR_2
        else:
            dest2 = "A" if seg == "constant" else "M"
            res += gc.PUSH_STR.format(dest2)
        self.output.write(res + "\n")

    def close(self):
        """
        close output file after writing
        """
        self.output.close()
