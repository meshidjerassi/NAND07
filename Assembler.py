import glob
import os
from sys import argv
import ParserClass as ps
import CodeWriter as cw


def extension_cut(file_name):
    index = findLastIndex(file_name)
    return file_name[:index]


def findLastIndex(str):
    index = -1
    for i in range(0, len(str)):
        if str[i] == '.':
            index = i
    return index



def main(argv):
    """
    Creates parser object and code writer object, transfers the relevant commands to the relevant methods.
    :param argv: file path
    :return: void
    """
    file_name = extension_cut(argv[1])
    code_writer = cw.CodeWriter(file_name+".asm")
    if os.path.isdir(argv[1]):
        directory = glob.iglob(os.path.join(argv[1], "*.vm"))
    else:
        directory = [file_name]
    for file in directory:
        f = extension_cut(file)
        code_writer.setFileName(f)
        parser = ps.ParserClass(file)
        while parser.hasMoreCommands():
            cmd = parser.commandType()
            if cmd == "C_PUSH":
                code_writer.writePushPop("push", parser.arg1(), parser.arg2())
            if cmd == "C_POP":
                code_writer.writePushPop("pop", parser.arg1(), parser.arg2())
            if cmd == "C_ARITHMETIC":
                code_writer.writeArithmetic(parser.arg1)
            parser.advance()
        code_writer.close()
    return


if __name__ == "__main__":
    main(argv[1])