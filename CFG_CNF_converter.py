import string
from copy import deepcopy

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
def getCFG(grammarPath) :
    CFG_RULE = {}
    with open(grammarPath, 'r') as f:
        lines = [line.split('->')
                    for line in f.read().split('\n')
                    if len(line.split('->')) == 2]
        for line in lines:
            variable = line[0].replace(" ", "")
            rawProductions = [rawProduction.split() for rawProduction in line[1].split('|')]
            production = []
            for rawProduction in rawProductions:
                production.append(["|" if grammar == "or_bit" else " " if grammar == "spasi" else "\n" if grammar == "endl" else grammar for grammar in rawProduction])
            CFG_RULE.update({variable: production})
    return CFG_RULE

#mengecek apakah unit satuan yang ada termasuk kedalam terminal atau bukan
def isVariable(item):
    if len(item) == 1:
        return False
    for char in item:
        if char not in (string.ascii_uppercase + '_' + string.digits):
            return False
    return True

#untuk menghapis unit production CFG
def removeUnitProduction(CFG):
    for variable in CFG:
        productions = CFG[variable]
        repeat = True
        while repeat:
            repeat = False
            for production in productions:
                if len(production) == 1 and isVariable(production[0]):
                    productions.remove(production)
                    newProduction = deepcopy([production for production in CFG[production[0]]
                                        if production not in productions])
                    productions.extend(newProduction)
                    repeat = True
                    break
    return CFG

#tahap terakhir mengubah CFG to CNG yaitu mengubah bentuknya
def updateToCNF(CFG):
    newRule = {}
    for variable in CFG:
        terminals = []
        productions = CFG[variable]
        # Search terminals
        processProduction = [production for production in productions if len(production) > 1]
        for production in processProduction:
            for item in production:
                if not(isVariable(item)) and item not in terminals:
                    terminals.append(item)
        # Create new rule and update production
        for i, terminal in enumerate(terminals):
            newRule.update({f"{variable}_TERM_{i + 1}": [[terminal]]})
            for idx, j in enumerate(productions):
                if len(j) > 1:
                    for k in range(len(j)):
                        if len(productions[idx][k]) == len(terminal):
                            productions[idx][k] = productions[idx][k].replace(terminal, f"{variable}_TERM_{i + 1}")
        # Update productions so match A -> BC or A -> terminal
        idx = 1
        for i in range(len(productions)):
            while len(productions[i]) > 2:
                newRule.update({f"{variable}_EXT_{idx}": [[productions[i][0], productions[i][1]]]})
                productions[i] = productions[i][1:]
                productions[i][0] = f"{variable}_EXT_{idx}"
                idx += 1
    CFG.update(newRule)
    return CFG

def convertCFGtoCNG(CFG):
    CFG = removeUnitProduction(CFG)
    CNF = updateToCNF(CFG)
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




