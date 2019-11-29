import glob
import os

import global_consts as gb

parsed_lines = []


def parser(path):
    """

    :param path:
    :return: an array of cleaned lines from all required files
    """
    if os.path.isfile(path):
        fileReader(path)
    elif os.path.isdir(path):
        dirHandler(path)
    return parsed_lines


def fileReader(file):
    """
    Opens the given file, reads line after line and sends it to lineHandler method
    :param file: the path of the given file from argv[1]
    :return: void
    """
    with open(file) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            lineHandler(line)
            line = fp.readline()
            cnt += 1
        fp.close()


def dirHandler(dir):
    """

    :param dir:
    :return:
    """
    files = glob.iglob(os.path.join(dir, "*.vm"))
    for f in files:
        fileReader(f)
    return


def lineHandler(line):
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
    parsed_lines.append(line)
    return


