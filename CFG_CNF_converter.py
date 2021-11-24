import string as st
from copy import deepcopy as dc

#untuk menampilkan grammar, berfungsi untuk membantu tracking perubahan pada grammar
def checkGrammar(dictionary):
    for var in dictionary:
        print(var,"->",end="")
        products = dictionary[var]
        for i in range(len(products)):
            if i == len(products) - 1 :
                print(products[i])
            else :
                print(products[i], "|", end = "")

def writeGrammar(dictionary, filename):
    file = open(filename, "w")
    for var in dictionary:
        file.write(var)
        file.write(" -> ")
        products = dictionary[var]
        for i in range(len(products)):
            for j in range(len(products[i])):
                if i == len(products) - 1 :
                    if products[i][j] == " ":
                        file.write("spaci")
                        file.write(" ")
                    elif products[i][j] == "|":
                        file.write("or_bit")
                        file.write(" ")
                    elif products[i][j] == "\n":
                        file.write("endl")
                        file.write(" ")
                    else:
                        file.write(products[i][j])
                        file.write(" ")
                    if j == len(products[i]) - 1:
                        file.write("\n")                    
                else :
                    if products[i][j] == " ":
                        file.write("spaci")
                        file.write(" ")
                    elif products[i][j] == "|":
                        file.write("or_bit")
                        file.write(" ")
                    elif products[i][j] == "\n":
                        file.write("endl")
                        file.write(" ")
                    else:
                        file.write(products[i][j])
                        file.write(" ")
                    if j == len(products[i]) - 1:
                        file.write(" | ")     
#membaca CFG dari file
def getCFG(cfgpath) :
    CFG = {}
    with open(cfgpath) as file:
        readfile = file.read()
        rawlines = readfile.split('\n')
        lines = []
        for rawline in rawlines:
            if len(rawline.split("->")) == 2:
                lines.append(rawline.split("->"))
        for line in lines:
            var = line[0].replace(" ","")
            rawLineProducts = line[1].split("|")
            rawProducts = []
            for rawLineProduct in rawLineProducts:
                rawProducts.append(rawLineProduct.split())
            products = []
            for rawProduct in rawProducts:
                grammarTemp = []
                for grammar in rawProduct:
                    if grammar == "or_bit":
                        grammarTemp.append("|")
                    elif grammar == "spasi":
                        grammarTemp.append(" ")
                    elif grammar == "endl":
                        grammarTemp.append("\n")
                    else :
                        grammarTemp.append(grammar)
                products.append(grammarTemp)
            CFG.update({var:products})
    return CFG

#mengecek apakah unit satuan yang ada termasuk kedalam terminal atau bukan
def isVar(grammar):
    if len(grammar) == 1:
        return False
    else:
        for character in grammar:
            if character not in (st.ascii_uppercase + "_"):
                return False
        return True

#untuk menghapis unit production CFG
def deleteUnitProduction(CFG):
    temp = dc(CFG)
    for var in CFG:
        products = CFG[var]
        clear = False
        while not clear:
            clear = True
            for product in products:
                if len(product) == 1:
                    grammar = product[0]
                    if isVar(grammar):
                        products.remove(product)
                        newProduct = []
                        for product in temp[grammar]:
                            if product not in products:
                                newProduct.append(product)
                        products.extend(newProduct)
                        clear = False
                        break
    return CFG

#tahap terakhir mengubah CFG to CNG yaitu mengubah bentuknya
def changeForm(CFG):
    tempRules = {}
    for var in CFG:
        tempTerminals = []
        products = CFG[var]
        #mencari letak terminal
        findTerminal = []
        for product in products:
            if len(product) > 1:
                findTerminal.append(product)
        for terminal in findTerminal:
            for grammar in terminal:
                if not(isVar(grammar)) and grammar not in tempTerminals:
                    tempTerminals.append(grammar)
        #membuat kerangka aturan baru
        idx = 1
        for tempTerminal in tempTerminals:
            tempRules.update({str(var)+"_MAIN_RULE(s)_"+str(idx):[[tempTerminal]]})
            for i in range(len(products)):
                count = len(products[i])
                if count > 1:
                    for j in range(count):
                        if products[i][j] == tempTerminal:
                            products[i][j] = products[i][j].replace(tempTerminal, str(var)+"_MAIN_RULE(s)_"+str(idx))
            idx += 1
        #mengubah nonTerminal AB -> C atau A -> terminal
        idx = 1
        for i in range(len(products)):
            count = len(products[i])
            while count > 2:
                tempRules.update({str(var)+"_EXTRA_RULE(s)_"+str(idx):[[products[i][0],products[i][1]]]})
                products[i] = products[i][1:]
                products[i][0] = str(var)+"_EXTRA_RULE(s)_"+str(idx)
                idx += 1
                count = len(products[i])
    CFG.update(tempRules)       
    return CFG

def convertCFGtoCNF(CFG):
    #rules2
    CFGnonUnit = deleteUnitProduction(CFG)
    #rules4
    CNF = changeForm(CFGnonUnit)
    return CNF

def convertCFGtoCNGwithTimeLapse(CFG):
    #base
    checkGrammar(CFG)
    print("===============================================================================================================")
    #rule 2    
    CFGnonUnit = deleteUnitProduction(CFG)
    checkGrammar(CFGnonUnit)
    print("===============================================================================================================")
    #rule 4
    CNF = changeForm(CFGnonUnit)
    checkGrammar(CNF)
    print("===============================================================================================================")


if __name__ == "__main__":
    CFG = getCFG("cfg.txt")
    CNF = convertCFGtoCNG(CFG)
    checkGrammar(CNF)
    writeGrammar(CNF,"cnf_converted.txt")
