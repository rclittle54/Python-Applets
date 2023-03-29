# Bingo Card Generator

This program creates bingo cards from a given list of elements, in a text file.

Example input:
```txt
 1 | item1
 2 | item2
 ...
24 | item24
```

From the command line, call:

```cmd
python bingo-card-generator/main.py --inputFile bingo-card-generator/exampleInput.txt --outputFile bingo-card-generator/output/exampleOutput.csv --numRepeats 15
```

You can expect the output to be of the form:
```
item1,  item2,  item3,  item4,  item5,
item6,  item7,  item8,  item9,  item10,
item11, item12, FREE,   item13, item14,
item15, item16, item17, item18, item19,
item20, item21, item22, item23, item24,
```
*Note: The output will be shuffled.*