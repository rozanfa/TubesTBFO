import sys
import re


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

terminal ={
    "from" : "P",
    "import" : "Q",
    "as" : "R",
    "for" : "F",
    "while" : "W",
    "in" : "G",
    "if" : "I",
    "elif" : "J",
    "else" : "K",
    "pass" : "Z",
    "continue" : "C",
    "break" : "B",
    "NONE" : "X",
    "True" : "n",
    "False" : "o",
    "not" : "p",
    "is" : "q",
    "in" : "r",
    "or" : "s",
    "and" : "t",
    "class" : "u",
    "def" : "v",
    "return" : "w"
}

def findNumberBeforeLetter(string):
    highlightedString = ""
    while string:
        notAcc = re.search("[0-9]+[A-Za-z_]+", string)
        if notAcc == None :
            highlightedString += string
            string = ""
        else :
            l, r = notAcc.span()
            highlightedString += string[:l] + colors.FAIL + "E" + colors.ENDC
            string = string[r:]
    return highlightedString


def convertCodeInput(codeInput):
    
    convertedCodeInput = ""

    global terminal

    while codeInput:
        regex = re.search("[A-Za-z_][A-Za-z0-9_]*", codeInput)
        if regex == None:
            convertedCodeInput += codeInput
            codeInput = ""
        else :
            l, r = regex.span()
            convertedCodeInput += codeInput[:l]
            if regex.group() not in terminal:
                convertedCodeInput += "z"
            else :
                convertedCodeInput += terminal[regex.group()]
            codeInput = codeInput[r:]


    convertedCodeInput = re.sub("#.*", "", convertedCodeInput)
    convertedCodeInput = re.sub("[0-9]+", "y", convertedCodeInput)
    convertedCodeInput = re.sub("[0-9]+[A-Za-z_]+", "R", convertedCodeInput)


    comments =  re.findall(r'([\'\"])\1\1(.*?)\1{3}', convertedCodeInput, re.DOTALL)
    for i in range(len(comments)):
        cmts = comments[i][0]*3 + comments[i][1] + comments[i][0]*3
        convertedCodeInput = convertedCodeInput.replace(cmts, "x\n" * convertedCodeInput[i][1].count("\n"))
    
    strings = re.findall(r'([\'\"])(.*?)\1{1}', convertedCodeInput, re.DOTALL)
    for i in range(len(strings)):
        strs = str[i][0] + str[i][1] + str[1][0]
        convertedCodeInput = convertedCodeInput.replace(strs, "x")

    convertedCodeInput = convertedCodeInput.replace(" ", "")
    convertedCodeInput = re.sub("xzy{1}:[xyz]{1},","", convertedCodeInput)
    convertedCodeInput = convertedCodeInput +"\n"

    return convertedCodeInput

if __name__ == "__main__":
    
    filePath = sys.argv[1] if len(sys.argv) >= 2 else "testCode.py"

    try :
        f = open(filePath, "r")
        codeInput = f.read()
    except Exception as e:
        print(str(e))
        exit(0)
    
    print(findNumberBeforeLetter(codeInput))

    markedCodeInput = findNumberBeforeLetter(codeInput)

    convertedCodeInput = convertCodeInput(codeInput)
    

    print("Checking your code!")
    print("Please wait..")

    print(convertedCodeInput)

    print("\n")
    if (len(convertedCodeInput) == 0):
        print("Congratulations! Your code is accepted")
        print("Your code :")
        print("-----------------------------------------")
        for i, line in enumerate(markedCodeInput.split("\n")):
            if len(line.replace(" ", "")) != 0:
                print(str(i+1) + "| " + line)
        print("-----------------------------------------")
    else :
        pass
        