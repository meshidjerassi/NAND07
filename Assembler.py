import re
from sys import argv
import ParserClass as ps
import global_consts as gc
import CodeWriter as cw


def assembler(path):
    parser = ps.ParserClass(path)
    codeWriter = cw.CodeWriter(path)
    for line in parser.parsed_lines:
        for cmd in gc.cmd:
            if cmd in line:
                for seg in gc.seg:
                    if seg in line:
                        int = re.findall("\d+", line)[0]
                        codeWriter.writePushPop(cmd, seg, int)
        for opp in gc.opp:
            if opp in line:
                codeWriter.writeArithmetic(opp)


def main(argv):
    assembler(argv[1])


if __name__ == "__main__":
    main(argv)
