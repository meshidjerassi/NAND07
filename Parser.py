import glob
import os
import re

import global_consts as gc


class Parser:
    """
    Handle one or multiple VM files, parses then and splits them into lines to send to the codeWriter obj
    """

    def __init__(self, file):
        """
        constructor, creates an array of parsed lines from the given path
        :param file:
        """
        self.path = file
        self.parsed_lines = []
        self.parser()
        self.line = 0

    def parser(self):
        """
        calls the relevant method according to path type
        :return: an array of cleaned lines from all required files
        """
        if os.path.isfile(self.path):
            self.fileReader(self.path)

    def fileReader(self, file):
        """
        Opens the given file, reads line after line and sends it to lineHandler method
        :param file: the path of the given file from argv[1]
        :return: void
        """
        with open(file) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                self.lineHandler(line)
                line = fp.readline()
                cnt += 1
            fp.close()

    def dirHandler(self):
        """

        :param dir:
        :return:
        """
        files = glob.iglob(os.path.join(self.path, "*.vm"))
        for f in files:
            self.fileReader(f)
        return

    def lineHandler(self, line):
        """
        receives a string, removes all white spaces
        :param line: a string of a line from the given vm file
        :return: void
        """
        line = line.strip(gc.NEW_LINE)
        line = line.strip(gc.TAB)
        for i in range(len(line) - 1):
            if line[i] + line[i + 1] == gc.COMMENT:
                line = line[:i]
                break
        if len(line) == 0:
            return
        self.parsed_lines.append(line)
        return

    def hasMoreCommands(self):
        """
        Checks if there are any more lines to parse
        :return: True if there are and false if no more lines
        """
        if self.line >= len(self.parsed_lines):
            return False
        return True

    def advance(self):
        """
        Advances the line count in order to access the next parsed line in the file
        """
        self.line += 1

    def commandType(self):
        line = self.parsed_lines[self.line]
        for opp in gc.opp:
            if opp in line:
                return "C_ARITHMETIC"
        for cmd in gc.cmd:
            if cmd in line:
                if cmd == gc.cmd[0]:
                    return "C_PUSH"
                else:
                    return "C_POP"
        return

    def arg1(self):
        """
        Split the current line and returns the relevant arg
        :return: cmd
        """
        line = self.parsed_lines[self.line]
        for cmd in gc.cmd:
            if cmd in line:
                for seg in gc.seg:
                    if seg in line:
                        return seg
        for opp in gc.opp:
            if opp in line:
                return opp
        return

    def arg2(self):
        """
        Split the current line and returns the relevant arg
        :return: int
        """
        line = self.parsed_lines[self.line]
        for cmd in gc.cmd:
            if cmd in line:
                for seg in gc.seg:
                    if seg in line:
                        command_int = re.findall("\d+", line)[0]
                        return command_int
        return
