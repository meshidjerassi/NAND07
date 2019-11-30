import glob
import os
from sys import argv
import parser as ps
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



def main(path):
    """
    Creates parser object and code writer object, transfers the relevant commands to the relevant methods.
    :param argv: file path
    :return: void
    """
    file_name = extension_cut(path)
    code_writer = cw.CodeWriter(file_name+".asm")
    directory = []
    if os.path.isdir(path):
        directory = glob.iglob(os.path.join(path, "*.vm"))
    else:
        directory.append(path)
    for file in directory:
        # removing the file extension and send it to the setFileName
        f = extension_cut(file)
        code_writer.setFileName(f)
        # creating a relevant parser object
        parser = ps.ParserClass(file)
        print(len(parser.parsed_lines))
        while parser.hasMoreCommands():
            cmd = parser.commandType()
            if cmd == "C_PUSH":
                code_writer.writePushPop("push", parser.arg1(), parser.arg2())
            if cmd == "C_POP":
                code_writer.writePushPop("pop", parser.arg1(), parser.arg2())
            if cmd == "C_ARITHMETIC":
                code_writer.writeArithmetic(parser.arg1())
            parser.advance()
        code_writer.close()
    return


if __name__ == "__main__":
    main(argv[1])