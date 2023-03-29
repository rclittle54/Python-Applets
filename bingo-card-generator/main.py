"""main.py: Main file for bingo-card-generator"""

# Imports
import numpy as np
import os

_EXPECTEDVALS = 24

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
    print("Hello world")
    usrInput = parseTextFileInput("bingo-card-generator/exampleInput.txt")
    arr = convertListToBingoArray(usrInput)
    np.savetxt("bingo-card-generator/testOut.csv", arr, fmt="%s", delimiter=',')
    return


if __name__ == "__main__":
    main()