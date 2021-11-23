import sys
import re
from CYKAlgorithm import CYKAlgorithm
from CFG_CNF_converter import getCFG, convertCFGtoCNG
from printcolors import colors


terminal ={
    "from" : "B",#
    "import" : "Q",#
    "as" : "R",#
    "for" : "F",#
    "while" : "W",#
    "in" : "G",#
    "if" : "I",#
    "elif" : "J",#
    "else" : "K",#
    "pass" : "Z",#
    "continue" : "C",#
    "break" : "B",#
    "NONE" : "X",#
    "True" : "n",#
    "False" : "o",#
    "not" : "A",#
    "is" : "q",#
    "or" : "s",#
    "and" : "t",#
    "class" : "u",#
    "def" : "v",#
    "return" : "w",
    "raise" : "a",#
    "with" : "b"#
}


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

    # Hapus single line komentar
    convertedCodeInput = re.sub("#.*", "", convertedCodeInput)

    # Ubah angka jadi p
    convertedCodeInput = re.sub("[0-9]+", "p", convertedCodeInput)

    # Ubah unaccepted variable jadi R
    convertedCodeInput = re.sub("[0-9]+[A-Za-z_]+", "R", convertedCodeInput)

    # Ubah multiline comments jadi x\n
    comments =  re.findall(r'([\'\"])\1\1(.*?)\1{3}', convertedCodeInput, re.DOTALL)
    for i in range(len(comments)):
        cmts = comments[i][0]*3 + comments[i][1] + comments[i][0]*3
        convertedCodeInput = convertedCodeInput.replace(cmts, "x\n" * comments[i][1].count("\n"))
    
    # Ubah string jadi x
    strings = re.findall(r'([\'\"])(.*?)\1{1}', convertedCodeInput, re.DOTALL)
    for i in range(len(strings)):
        strs = strings[i][0] + strings[i][1] + strings[i][0]
        convertedCodeInput = convertedCodeInput.replace(strs, "x")

    # Ngilangin spasi
    convertedCodeInput = convertedCodeInput.replace(" ", "")
    convertedCodeInput = re.sub("xzy{1}:[xyz]{1},","", convertedCodeInput)

    # Tambah endline di akhir
    convertedCodeInput = convertedCodeInput +"\n"

    return convertedCodeInput

def print_banner():
    print("                                 ")
    print("                             /&@@@@&/                         ")
    print("                         &@@@@@@@@@@@@@@@                                        ")
    print("                       @@@@///&@@@@@@@@@@@@                              ")
    print("                      @@@@@@@///@@@&//@@@@@@                            ")
    print("                     @@@@@@@@/////(@@@@@@@@@      ")
    print("                   (@@@@@@@@@@@@@@@@@@@@@@@#         ")
    print("               &&@@@@@@@@@@@@@@@@@@@@@@@@@@                      ")
    print("                     @@@@@@@@@@@@@@@@@@@@@@%             ")
    print("                     *@@@@@@@@@@@@@@@@@@@ @@&(            ")
    print("                      /@@@@@@@@@@@@@@@@@*    (/(       ")
    print("                        @@@@@@@@@@@@@@@@/                  ")
    print(" "+colors.LIGHTRED+"  |_|| |  ~|~ /|/\  "+colors.ENDC+"    /@@@@@@@@@@@@@@@                 ")
    print(" "+colors.LIGHTRED+"  | ||_|   | /-|\/  "+colors.ENDC+"       @@@@@@@@@@@@@/           ")      
    print("                              @@@@@@@@@@@@@   ")       
    print(" "+colors.LIGHTRED+"  /`/\|\/||)|| [~|) "+colors.ENDC+"            &@@@@@@@@@@&#  ")        
    print(" "+colors.LIGHTRED+"  \,\/|  || ||_[_|\ "+colors.ENDC+"                &&&&&&&&&&&&*")      
    print("                                        *&&&&&&&&&&&&&&&&&&&&")
      

if __name__ == "__main__":
    print_banner()
    CFG= getCFG("cfg_copy.txt")
    CNF= convertCFGtoCNG(CFG)

    filePath = sys.argv[1] if len(sys.argv) >= 2 else input("Input file name: ")

    try :
        f = open(filePath, "r")
        codeInput = f.read()
    except Exception as e:
        print(str(e))
        exit(0)

    convertedCodeInput = convertCodeInput(codeInput)
    #print(convertedCodeInput)
    

    print("Checking your code!")
    print("Please wait..\n")

    if (len(convertedCodeInput.replace(" ", "").replace("\n", "")) == 0):
        print("Congratulations! Your code is accepted")
        print(colors.HEADER + "Your code :")
        print("-------------------------------------------------------------------")
        for i, line in enumerate(codeInput.split("\n")):
            if len(line.replace(" ", "")) != 0:
                print(colors.HEADER + str(i+1)  + "| " + colors.OKGREEN + line)
        print(colors.HEADER + "-------------------------------------------------------------------")
        print(colors.OKCYAN + "ACCEPTED" + colors.ENDC)
    else :
        CYKAlgorithm(convertedCodeInput, codeInput, CNF)
        