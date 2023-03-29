"""main.py: Main file for bingo-card-generator"""

# Imports
import numpy as np
import os
import argparse
import time
import random
random.seed(time.time())

# Constants
_EXPECTEDVALS = 24

# Default arguments
INPUTFILENAME = "bingo-card-generator/exampleInput.txt"
OUTPUTFILENAME = "bingo-card-generator/exampleOutput.txt"
NUMREPEATS = 2


def parseArgs():
    """Parses the arguments provided by the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputFile", help="Input .txt file, containing 24 lines of the various elements for the Bingo board")
    parser.add_argument("--outputFile", help="Output .csv file, into which the Bingo board will be stored")
    parser.add_argument("--numRepeats", help="The integer number of unique boards to generate")
    args = parser.parse_args()
    if args.inputFile:
        if not os.path.isfile(args.inputFile):
            print("Warning: input file of {0} not found".format(args.inputFile))
        INPUTFILENAME = args.inputFile
    if args.outputFile:
        if not os.path.splitext(args.outputFile)[1].lower() == ".csv":
            print("Warning: output file of {0} is not a .csv".format(args.outputFile))
        OUTPUTFILENAME = args.outputFile
    if args.numRepeats:
        if type(args.numRepeats) is not int:
            print("Warning: numRepeats value of '{0}' is not an integer".format(args.numRepeats))
        NUMREPEATS = args.numRepeats
    return


def parseTextFileInput(textFile: str) -> list:
    """Return a list of text elements from the provided text file"""

    output = None

    # Parse the file
    if os.path.isfile(textFile):
        with open(textFile, 'r') as f:
            output = [line.replace("\n", "") for line in f]

    # Handle funkiness
    if output:
        assert len(output) == _EXPECTEDVALS, "Parsed txt file did not have expected values"
    else:
        print("Warning: provided text file was unable to be found")

    return output


def convertListToBingoArray(inputList: list) -> np.array:
    """Returns a dataframe in the form of a bingo card from the input list."""
    # Pre-check the provided list
    assert len(inputList) == 24, "Provided list is not of the proper length, 24 elements."
    inputList.insert(12, "FREE") # Bingo has a "FREE" space in the middle
    arr = np.array(inputList)
    arr = np.reshape(arr, (5,5))
    return arr


def main():
    """Bingo Card Generator main function"""
    parseArgs() # Sets global variables
    for i in range(NUMREPEATS):
        boardItems = parseTextFileInput(INPUTFILENAME)
        random.shuffle(boardItems)
        board = convertListToBingoArray(boardItems)
        realFilename = "{0}-{1}.csv".format(os.path.splitext(OUTPUTFILENAME)[0], i)
        np.savetxt(realFilename, board, fmt="%s", delimiter=',')

    return


if __name__ == "__main__":
    main()