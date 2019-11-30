import glob
import os
from sys import argv
import Parser as ps
import CodeWriter as cw


def extension_cut(file_name):
    """
    removes the file extension
    :param file_name: file path
    :return: the file path with out it's extension
    """
    index = findLastIndex(file_name)
    return file_name[:index]


def findLastIndex(str):
    """
    finds last index of a dot '.' char in order to remove file path extension
    :param str: file path
    :return: the index of the last instance of a dot char
    """
    index = -1
    for i in range(0, len(str)):
        if str[i] == '.':
            index = i
    return index


def main(path):
    """
    Creates parser object and code writer object, transfers the relevant commands to the relevant methods.
    :param path: file path
    :return: void
    """
    directory = []
    if os.path.isdir(path):
        code_writer = cw.CodeWriter(path + ".asm")
        directory = glob.iglob(os.path.join(path, "*.vm"))
    else:
        file_name = extension_cut(path)
        code_writer = cw.CodeWriter(file_name + ".asm")
        directory.append(path)
    for file in directory:
        # removing the file extension and send it to the setFileName
        f = extension_cut(file)
        code_writer.setFileName(f)
        # creating a relevant parser object
        parser = ps.Parser(file)
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
