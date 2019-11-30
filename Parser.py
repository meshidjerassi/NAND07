import re

import GlobalConsts as gc


class Parser:
    """
    Handle one or multiple VM files, parses then and splits them into lines to send to the codeWriter obj
    """

    def __init__(self, path):
        """
        constructor, creates an array of parsed lines from the given path
        :param file:
        """
        self.parsed_lines = []
        self.cur_line = 0
        with open(path) as fp:
            line = fp.readline()
            while line:
                self.lineHandler(line)
                line = fp.readline()

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
        if len(line) > 0:
            self.parsed_lines.append(line)

    def hasMoreCommands(self):
        """
        Checks if there are any more lines to parse
        :return: True if there are and false if no more lines
        """
        return self.cur_line < len(self.parsed_lines)

    def advance(self):
        """
        Advances the line count in order to access the next parsed line in the file
        """
        self.cur_line += 1

    def commandType(self):
        line = self.parsed_lines[self.cur_line]
        for op in gc.MATH_CMD:
            if op in line:
                return gc.C_ARITHMETIC
        for cmd in gc.STACK_CMD:
            if cmd in line:
                return cmd

    def arg1(self):
        """
        Split the current line and returns the relevant arg
        :return: cmd
        """
        line = self.parsed_lines[self.cur_line]
        for cmd in gc.STACK_CMD:
            if cmd in line:
                for seg in gc.SEG:
                    if seg in line:
                        return seg
        for op in gc.MATH_CMD:
            if op in line:
                return op

    def arg2(self):
        """
        Split the current line and returns the relevant arg
        :return: int
        """
        line = self.parsed_lines[self.cur_line]
        return re.findall(r'\d+', line)[0]
