import string as st
from copy import deepcopy as dc

#untuk menampilkan grammar, berfungsi untuk membantu tracking perubahan pada grammar
def checkGrammar(dictionary):
    for param in dictionary:
        print(param,"->",end="")
        product = dictionary[param]
        for i in range(len(product)):
            if i == len(product) - 1:
                print(product[i])
            else:
                print(product[i], "| ", end="") 

#membaca CFG dari file
def getCFG(cfgpath) :
    CFG = {}
    with open(cfgpath) as file:
        rawlines = file.read().split('\n')
        lines = [rawline.split("->") for rawline in rawlines if len(rawline.split("->")) == 2]
        for line in lines:
            param = line[0].replace(" ","")
            rawLineProducts = line[1].split("|")
            rawProducts = [rawLineProduct.split() for rawLineProduct in rawLineProducts]
            products = []
            for rawProduct in rawProducts:
                products.append(["|" if grammar == "or_bit" else " " if grammar == "spasi" else "\n" if grammar == "endl" else grammar for grammar in rawProduct])
            CFG.update({param:products})
    return CFG

#mengecek apakah unit satuan yang ada termasuk kedalam terminal atau bukan
def isParam(grammar):
    if len(grammar) == 1:
        return False
    for character in grammar:
        if character not in (st.ascii_uppercase + "_"):
            return False
    return True

#untuk menghapis unit production CFG
def deleteUnitProduction(CFG):
    for param in CFG:
        products = CFG[param]
        clear = False
        while not clear:
            clear = True
            for product in products:
                if len(product) == 1:
                    grammar = product[0]
                    if isParam(grammar):
                        products.remove(product)
                        newProduct = dc([product for product in CFG[product[0]] if product not in products])
                        products.extend(newProduct)
                        clear = False
                        break
    return CFG

#tahap terakhir mengubah CFG to CNG yaitu mengubah bentuknya
def changeForm(CFG):
    tempRules = {}
    for param in CFG:
        tempTerminals = []
        products = CFG[param]
        #mencari letak terminal
        findTerminal = [product for product in products if len(product) > 1]
        for terminal in findTerminal:
            for grammar in terminal:
                if not(isParam(grammar)) and grammar not in  tempTerminals:
                    tempTerminals.append(grammar)
        #membuat kerangka aturan baru
        idx = 1
        for tempTerminal in tempTerminals:
            tempRules.update({str(param)+"_MAIN_RULE(s)_"+str(idx):[[tempTerminal]]})
            i = 0
            for product in products:
                count = len(product)
                if count > 1:
                    for j in range(count):
                        if len(products[i][j]) == len(tempTerminal):
                            products[i][j] = products[i][j].replace(tempTerminal, str(param)+"_MAIN_RULE(s)_"+str(idx))
                i += 1
            idx += 1
        #mengubah nonTerminal AB -> C atau A -> terminal
        idx = 1
        for i in range(len(products)):
            while len(products[i]) > 2:
                tempRules.update({str(param)+"_EXTRA_RULE(s)_"+str(idx):[[products[i][0],products[i][1]]]})
                products[i] = products[i][1:]
                products[i][0] = str(param)+"_EXTRA_RULE(s)_"+str(idx)
                idx += 1
    CFG.update(tempRules)       
    return CFG

def convertCFGtoCNG(CFG):
    CFGnonUnit = deleteUnitProduction(CFG)
    CNF = changeForm(CFGnonUnit)
    return CNF

def convertCFGtoCNGwithTimeLapse(CFG):
    checkGrammar(CFG)
    print("===============================================================================================================")    
    CFGnonUnit = deleteUnitProduction(CFG)
    checkGrammar(CFGnonUnit)
    print("===============================================================================================================")
    CNF = changeForm(CFGnonUnit)
    checkGrammar(CNF)
    print("===============================================================================================================")


if __name__ == "__main__":
    CFG = getCFG("cfg.txt")
    convertCFGtoCNGwithTimeLapse(CFG)