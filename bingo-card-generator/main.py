"""main.py: Main file for bingo-card-generator"""

# Imports
import pandas as pd
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


def main():
    """Bingo Card Generator main function"""
    print("Hello world")
    print(parseTextFileInput("bingo-card-generator/exampleInput.txt"))
    return


if __name__ == "__main__":
    main()