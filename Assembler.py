import re
from sys import argv
import Parser as ps
import global_consts as gc


def assembler(path):
    unpacked_file = ps.parser(path)
    for line in unpacked_file:
        for seg_opp in gc.seg_opp:
            if seg_opp in line:
                for seg in gc.seg:
                    if seg in line:
                        int = re.findall("\d+", line)[0]
                        print(seg_opp + " " + seg + " " + str(int)) #TODO send seg + int to decoder seg method
        for opp in gc.opp:
            if opp in line:
                print(opp) #TODO send opp to decoder opp method
    print("bye")


def main(argv):
    assembler(argv[1])


if __name__ == "__main__":
    main(argv)
