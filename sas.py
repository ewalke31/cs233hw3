
# Eric Walker & Derek Reitz
# ewalke31@jhu.edu & dreitz5@jhu.edu
# CS233 Computer System Fundamentals HW #3

import sys


# the binary pattern for each SCRAM instruction
encoding = {
    "HLT": "0000", "LDA": "0001", "LDI": "0010",
    "STA": "0011", "STI": "0100", "ADD": "0101",
    "SUB": "0110", "JMP": "0111", "JMZ": "1000"
}

labels = {}


# reads in input from stdin and appends it to input list
def readInput():
    inputList = []
    for line in sys.stdin:  # every line from stin added to list
        inputList.append(line)
    return inputList


# adds the labels to a map corresponding to line number
# starting at 0
def firstPassParser(inputList):
    global labels
    currLine = 0  # keeps track of line number for labels
    inputLine = 0  # keeps track of input line number for reporting errors
    for line in inputList:
        inputLine += 1
        entry = line.split()
        segPos = 0
        for seg in entry:  # removes all comments from the input for
            if seg[0] == '#':  # the sake of convenience in further parsing
                entry = entry[0:segPos]
            segPos += 1
        if len(entry) != 0:  # if line is not empty
            endEntry = len(entry[0])-1
            if entry[0][endEntry] == ':':  # if first entry is a label
                label = entry[0][0:endEntry]  # assign it to "label"
                if label in labels.keys():  # if it exists, error
                    print("Label already exists. Error on line: " + inputLine,
                          file=sys.stderr)
                elif label in encoding.keys():  # if bad name, error
                    print("Label cannot be same name as microprogram. Error \
                          on line: " + inputLine, file=sys.stderr)
                else:
                    if currLine < 16:  # if < 16 add as 4 bit number
                        labels.update({label: "{:0>4}".format("{0:b}".format(
                            currLine))})  # formatting converts to binary then
                    else:                 # pads with leading 0's if necessary
                        labels.update({label: "{:0>8}".format("{0:b}".format(
                            currLine))})  # else if it's >= 16 then save as 8
            currLine += 1                 # bit number for DAT type labels
            if currLine >= 16:  # if current line is >= 16
                i = 0  # keeps track of segment number
                for seg in entry:
                    endSeg = len(seg)-1
                    # if giving a microinstruction, throw an error
                    if seg in encoding.keys() or seg == "DAT":
                        print("Program is too long for the SCRAM. Error \
                              on line: " + inputLine, file=sys.stderr)
                    # if not giving a label, or giving more than one label
                    elif seg[endSeg] != ':' or (seg[endSeg] == ':' and i != 0):
                        print("Invalid entry on line: " + inputLine,
                              file=sys.stderr)  # throw an error
                    i += 1  # increment segment count
        # update corresponding input list line with removed comment line
        inputList[inputLine-1] = entry
        # save input line for error checking during second parse
        inputList[inputLine-1].insert(0, inputLine)  # since we removed lines
    i = 0
    length = len(inputList)
    while i < length:
        if len(inputList[i]) == 1:  # if len=1 it will only be the input line
            inputList.remove(inputList[i])  # number saved just above this,
            length -= 1        # i.e. it was a blank line and we want to delete
        else:                  # it for convenience in future parse
            i += 1
    return inputList  # returns list without blank lines or comments


# Parses through a second time with the updated inputList, putting the
# necessary binary in a string
def secondPassParser(inputList):
    global labels
    output = ""  # initialize output to empty string
    for line in inputList:  # for every line in the input list
        endEntry = len(line[1])-1  # denotes last index
        # if first entry is a label and there are 2 arguments following
        # (remember that line[0] is the line number for error checking)
        if line[1][endEntry] == ':' and len(line) > 3:
            output = subparser(2, line, output)  # feed to subparser
        # if first entry is label and improper number of arguments, error
        elif line[1][endEntry] == ':' and (len(line) == 3 or len(line) > 4):
            print("Illegal number of arguments in line: " + line[0],
                  file=sys.stderr)
        # if no label and first entry is microinstruction/"DAT" and there
        # are 2 arguments (plus line number), which is only valid possibility
        elif (line[1] in encoding.keys() or line[1] == "DAT") \
                and len(line) == 3:
            output = subparser(1, line, output)  # feed to subparser
        else:  # else the line isn't formatted right so throw an error
            print("Illegal number of arguments in line: " + line[0],
                  file=sys.stderr)
    return output  # returns the binary output


# Subparser for second parse. Helps avoid repetitive code for cases when
# there is or is not a label as the first entry
def subparser(i, line, output):
    if line[i] in encoding.keys():  # if entry is microinstruction
        output += encoding[line[i]]  # add it to the output string
        if line[i+1].isdigit():  # if next entry is a digit
            # and if it's in the correct range and not a float
            if int(line[i+1]) >= 0 and int(line[i+1]) <= 15 \
                    and type(line[i+1]) is not float:
                # add to output, first converting to binary, then padding with
                # 0's, adding a space to make converting to ascii easier later
                output += "{:0>5}".format("{0:b}".format(int(line[i+1])) + " ")
            else:  # else invalid address so print error
                print("Invalid address format. Error on line: " +
                      line[0], file=sys.stderr)
        else:  # if not a digit, it should be a label
            if line[i+1] in labels.keys():  # check if it's a label
                output += labels[line[i+1]] + " "  # add to output with space
            else:  # else throw undefined label error
                print("Undefined label. Error on line: " + line[0],
                      file=sys.stderr)
    elif line[i] == "DAT":  # else if entry is a "DAT" instruction
        if line[i+1].isdigit():  # if next entry is a digit
            # and if it's in the valid DAT range and not a float
            if int(line[i+1]) >= 0 and int(line[i+1]) <= 255 \
                    and type(line[i+1]) is not float:
                # add to output, first converting to binary and padding with
                # necessary 0's (up to 8 characters) plus the space
                output += "{:0>9}".format("{0:b}".format(int(line[i+1])) + " ")
            else:  # else invalid number so print error
                print("Invalid address format. Error on line: " +
                      line[0], file=sys.stderr)
        else:  # else, this means next entry is not a digit
            if line[i+1] in labels.keys():  # check if it's a label
                output += labels[line[i+1]] + " "  # if so add to output
            else:  # else print an undefined label error
                print("Undefined label. Error on line: " + line[0],
                      file=sys.stderr)
    else:  # else, this means not a microinstruction or "DAT"
        print("Improper microinstruction. Error on line: " + line[0],
              file=sys.stderr)  # so print an error
    return output  # return the updated output to second parse


def main():
    global labels
    inputList = readInput()  # read the input
    inputList = firstPassParser(inputList)  # add labels to mapping and
    # remove all comments and blank lines
    output = secondPassParser(inputList).split()  # process the output
    # and split it based on the spaces added
    out = ""
    for byte in output:  # convert each 8 bit sequence to ascii character
        out += chr(int(byte, 2))
    sys.stdout.write(out)  # finally write it to stdout. done! yay :-)


if __name__ == "__main__":
    main()
