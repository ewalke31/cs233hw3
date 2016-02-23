# Eric Walker & Derek Reitz
# ewalke31@jhu.edu & dreitz5@jhu.edu
# CS233 Computer System Fundamentals HW #3

import sys


# the hex pattern for each SCRAM instruction
encoding = {
    "HLT": 0, "LDA": 1, "LDI": 2,
    "STA": 3, "STI": 4, "ADD": 5,
    "SUB": 6, "JMP": 7, "JMZ": 8
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
            if seg[0] = '#':
                entry = entry[0:segPos]
            segPos += 1
        if len(entry) != 0:
            endEntry = len(entry[0])-1
            if entry[0][endEntry] == ':':
                label = entry[0][0:endEntry]
                if label in labels.keys():
                    print("Label already exists. Error on line: " + inputLine,
                          file=sys.stderr)
                else:
                    labels.update({label:hex(currLine)})
            currLine += 1
            if currLine >= 16:
                print("Program is too long for the SCRAM. Error on line: " +
                      inputLine, file=sys.stderr)
        line = entry
        line.insert(0, inputLine) #save input line for error checking later
    return inputList
    
def secondPassParser(inputList):
    global labels
    output = ""
    for line in inputList:
        if len(line) != 0:
            endEntry = len(line[1])-1
            if line[1][endEntry] == ':' and len(line) > 3:
                if line[2] in encoding.keys():
                    output += encoding[entry[1]]
                    if line[3].isdigit():
                        if line[3] >= 0 and line[3] <= 15 and line[3] is not
                        type float:
                            output += hex(int(line[3]))
                        else:
                            print("Invalid address format. Error on line: " +
                                  line[0], file=sys.stderr)
                    else:
                        if line[3] in labels.keys():
                            output += labels[line[3]]
                        else:
                            print("Undefined label. Error on line: " + line[0],
                                  file=sys.stderr)
                elif line[2] == "DAT":
                    if line[3].isdigit():
                        if line[3] >= 0 and line[3] <= 255 and line[3] is not
                        type float:
                            output += hex(int(line[3]))
                        else:
                            print("Invalid address format. Error on line: " +
                                  line[0], file=sys.stderr)
                    else:
                        if line[3] in labels.keys():
                            output += labels[line[3]]
                        else:
                            print("Undefined label. Error on line: " + line[0],
                                  file=sys.stderr)
                else:
                    print("Improper microinstruction. Error on line: " + line[0],
                          file=sys.stderr)
            elif line[1][endEntry] == ':' and (len(line) == 3 or len(line) > 4):
                print("Illegal number of arguments in line: " + line[0],
                      file=sys.stderr)
            elif 
                    
                                
    return None
    

def main():
    global labels
    inputList = readInput()
    inputList = firstPassParser(inputList)
    print(labels)
    
if __name__ == "__main__":
    main()
