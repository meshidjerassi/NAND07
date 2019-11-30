from sys import argv
import ParserClass as ps
import CodeWriter as cw


def main(argv):
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


if __name__ == "__main__":
    main(argv)
