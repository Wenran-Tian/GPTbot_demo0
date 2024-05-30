import argparse
from datetime import datetime

cmd = " -i 10"
cmd = "   "

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type = int)

args = parser.parse_args(cmd.split())
print("input" in args)
# print(datetime.today().strftime("%m%d_%H%M%S%f"))

args.input = None

print(args.input)
# s = [1,2,3]
#
# print(s[-4:])