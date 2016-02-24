
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
    for line in sys.stdin:
        inputList.append(line)
    return inputList

################################################################################
# adds the labels to a map corresponding to line number
# starting at 0
def firstPassParser(inputList):
    global labels
    currLine = 0
    inputLine = 0
    for line in inputList:
        inputLine += 1
        entry = line.split()
        segPos = 0
        for seg in entry: #removes all comments from the input for convenience
            if seg[0] == '#':
                entry = entry[0:segPos]
            segPos += 1
        if len(entry) != 0:
            endEntry = len(entry[0])-1
            if entry[0][endEntry] == ':':
                label = entry[0][0:endEntry]
                if label in labels.keys():
                    print("Label already exists. Error on line: " + inputLine,
                          file=sys.stderr)
                elif label in encoding.keys():
                    print("Label cannot be same name as microprogram. Error on line: " +
                          inputLine, file=sys.stderr)
                else:
                    if currLine < 16: 
                        labels.update({label:"{:0>4}".format("{0:b}".format(currLine))})
                    else:
                        labels.update({label:"{:0>8}".format("{0:b}".format(currLine))})
            currLine += 1
            if currLine >= 16:
                i = 0
                for seg in entry:
                    endSeg = len(seg)-1
                    if seg in encoding.keys() or seg == "DAT":
                        print("Program is too long for the SCRAM. Error on line: " +
                              inputLine, file=sys.stderr)
                    elif seg[endSeg] != ':' or (seg[endSeg] == ':' and i != 0):
                        print("Invalid entry on line: " + inputLine, file=sys.stderr)
                    i += 1
        inputList[inputLine-1] = entry
        inputList[inputLine-1].insert(0, inputLine) #save input line for error checking later
    i = 0
    length = len(inputList)
    while i < length:
        if len(inputList[i]) == 1:
            inputList.remove(inputList[i])
            length -= 1
        else:
            i += 1
    return inputList
    
def secondPassParser(inputList):
    global labels
    output = ""
    for line in inputList:
        if len(line) != 0:
            endEntry = len(line[1])-1
            if line[1][endEntry] == ':' and len(line) > 3:
                output = subparser(2, line, output)
            elif line[1][endEntry] == ':' and (len(line) == 3 or len(line) > 4):
                print("Illegal number of arguments in line: " + line[0],
                      file=sys.stderr)
            elif (line[1] in encoding.keys() or line[1] == "DAT") and len(line) == 3:
                output = subparser(1, line, output)
            else:
                print("Illegal number of arguments in line: " + line[0],
                      file=sys.stderr)
    return output
    
def subparser(i, line, output):
    if line[i] in encoding.keys():
        output += encoding[line[i]]
        if line[i+1].isdigit():
            if int(line[i+1]) >= 0 and int(line[i+1]) <= 15 and type(line[i+1]) is not float:
                output += "{:0>5}".format("{0:b}".format(int(line[i+1])) + " ")
            else:
                print("Invalid address format. Error on line: " +
                      line[0], file=sys.stderr)
        else:
            if line[i+1] in labels.keys():
                output += labels[line[i+1]] + " "
            else:
                print("Undefined label. Error on line: " + line[0],
                      file=sys.stderr)
    elif line[i] == "DAT":
        if line[i+1].isdigit():
            if int(line[i+1]) >= 0 and int(line[i+1]) <= 255 and type(line[i+1]) is not float:
                output += "{:0>9}".format("{0:b}".format(int(line[i+1])) + " ")
            else:
                print("Invalid address format. Error on line: " +
                      line[0], file=sys.stderr)
        else:
            if line[i+1] in labels.keys():
                output += labels[line[i+1]] + " "
            else:
                print("Undefined label. Error on line: " + line[0],
                      file=sys.stderr)
    else:
        print("Improper microinstruction. Error on line: " + line[0],
              file=sys.stderr)
    return output


def main():
    global labels
    inputList = readInput()
    inputList = firstPassParser(inputList)
    output = secondPassParser(inputList).split()
    out = ""
    for byte in output:
        out += chr(int(byte, 2))
    sys.stdout.write(out)
    
if __name__ == "__main__":
    main()
