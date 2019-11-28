import glob
import os
import global_consts as gb


class ParserClass:
    """

    """

    def __init__(self, file):
        """

        :param file:
        """
        self.path = file
        self.parsed_lines = []
        self.parser()

    def parser(self):
        """

        :param path:
        :return: an array of cleaned lines from all required files
        """
        if os.path.isfile(self.path):
            self.fileReader(self.path)
        elif os.path.isdir(self.path):
            self.dirHandler()

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
        line = line.strip(gb.NEW_LINE)
        line = line.strip(gb.TAB)
        for i in range(len(line) - 1):
            if line[i] + line[i + 1] == gb.COMMENT:
                line = line[:i]
                break
        if len(line) == 0:
            return
        self.parsed_lines.append(line)
        return
