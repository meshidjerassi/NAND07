from sys import argv
import ParserClass as ps
import CodeWriter as cw


def main(argv):
    """
    Creates parser object and code writer object, transfers the relevant commands to the relevant methods.
    :param argv: file path
    :return: void
    """
    parser = ps.ParserClass(argv[1])
    code_writer = cw.CodeWriter(argv[1])
    code_writer.setFileName(code_writer.file_name)
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
    main(argv)
