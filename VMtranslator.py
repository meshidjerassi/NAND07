import glob
import os
from sys import argv
import Parser as ps
import CodeWriter as cw
import GlobalConsts as gc


def main(path):
    """
    Creates parser object and code writer object, transfers the relevant commands to the relevant methods.
    :param path: file path
    :return: void
    """
    directory = []
    if os.path.isdir(path):
        code_writer = cw.CodeWriter(os.path.join(path, os.path.basename(path))+".asm")
        directory = glob.iglob(os.path.join(path, "*.vm"))
    else:
        file_name = path[:-3]
        code_writer = cw.CodeWriter(file_name + ".asm")
        directory.append(path)

    for file in directory:
        # removing the file extension and send it to the setFileName
        f = os.path.basename(file)[:-3]
        code_writer.setFileName(f)
        # creating a relevant parser object
        parser = ps.Parser(file)
        while parser.hasMoreCommands():
            cmd = parser.commandType()
            if cmd == gc.C_PUSH or cmd == gc.C_POP:
                code_writer.writePushPop(cmd, parser.arg1(), parser.arg2())
            if cmd == gc.C_ARITHMETIC:
                code_writer.writeArithmetic(parser.arg1())
            parser.advance()
    code_writer.close()


if __name__ == "__main__":
    main(argv[1])
