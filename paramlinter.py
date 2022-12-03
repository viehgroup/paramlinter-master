import argparse
from include import filterer
import datetime

banner = """\033[0;34;40m
         ___                          _     _        _             
        | _ \ __ _  _ _  __ _  _ __  | |   (_) _ _  | |_  ___  _ _ 
        |  _// _` || '_|/ _` || '  \ | |__ | || ' \ |  _|/ -_)| '_|
        |_|  \__/_||_|  \__/_||_|_|_||____||_||_||_| \__|\___||_|    \033[0;37;40m

                                        \033[1;32mby viehgroup\033[0;37m
"""
print(banner)

parser = argparse.ArgumentParser(description="ParamLinter")
parser.add_argument("-p","--path", help="Path to the file containing the urls to filter",required=True)
parser.add_argument("-f","--fuzz", help="fuzz text",required=True)
parser.add_argument("-hti","--htmli", help="[Y/N] filter possible html injections",default=False)
args = parser.parse_args()

file = open(args.path, "r")
success = []
for line in file:
    line = line.strip()
    if line.startswith("http"):
        # continue to checking
        if filterer.Filterer(line, fuzzText=args.fuzz).get_data():
            success.append(line)
    else:
        # add "http://" to the line and then send to the checking
        if filterer("http://" + line).get_data():
            success.append("http://" + line)

now = datetime.datetime.now()
if(success):
    outputFile = open(f"results/output_{now.strftime('%Y_%m_%d %H_%M_%S')}.txt", "a")
    for line in success:
        outputFile.write(line + "\n")

    file.close()
    outputFile.close()
    print(f"Results saved to results/output_{now.strftime('%Y_%m_%d %H_%M_%S')}.txt")
else :
    print("None of the parameters are up :/")
