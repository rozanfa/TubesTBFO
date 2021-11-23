from printcolors import colors

def CYKAlgorithm(convertedCodeInput,codeInput,CNF):
    m = len(CNF)
    n = len(convertedCodeInput)
    listLines = codeInput.split('\n')
    endLines = {}
    ctr = 0
    #mengambil data baris
    for i in range (n):
        if (convertedCodeInput[i] == '\n'):
            ctr += 1
            endLines[i] = ctr
    #membuat tabel
    table = [[[0 for i in range(m + 1)] for j in range(n + 1)] for k in range(n + 1)]
    keyword = {}
    data = [None] * (m + 1)
    # Set dictionary convertedCodeInput dan mengambil data dari CNF
    count=0
    for key in CNF:
        data[count + 1] = CNF[key]
        keyword[key] = count + 1
        count+=1
    # Algoritmanya
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            for element in data[j]:
                if (element[0] == convertedCodeInput[i - 1]):
                    table[1][i][j] = True #input terminal awal pada tabel
                    break
                

    for i in range(2, n + 1):
        for j in range(1, (n - i + 2)):
            for k in range(1, i):
                for l in range(1, m + 1):
                    for element in data[l]:
                        if (len(element)!=1): #jika elemen merupakan variabel
                            var1 = keyword[element[0]]
                            var2 = keyword[element[1]]
                            if (table[k][j][var1] and table[i - k][j + k][var2]):
                                table[i][j][l] = True
                                break


    #hasil CYK
    if (table[n][1][1]): #jika tabel akhir bernilai True
        print("Congratulations! Your code is accepted\n")
        print(colors.HEADER + "Your code :")
        print(colors.HEADER + "-------------------------------------------------------------------" + colors.HEADER )
        print(colors.OKGREEN, end = "")
        for i in range(len(listLines)):
            print(colors.HEADER + str(i+1).rjust(3) + ' | ' + colors.OKGREEN + listLines[i])
        print(colors.OKGREEN, end = "")
        print(colors.HEADER + "-------------------------------------------------------------------" + colors.HEADER )
        print(colors.OKCYAN + "ACCEPTED" + colors.ENDC)
    else :
        index = 1
        for i in range(n, 0, -1):
            if (table[i][1][1]):
                break
            elif (convertedCodeInput[i - 1] == '\n'):
                index = endLines[i - 1]
        print("Sorry, your code is not accepted\n")
        print(colors.HEADER + "Your code :")
        print(colors.HEADER + "-------------------------------------------------------------------" + colors.HEADER )
        print(colors.WARNING, end = "")
        errorline = []
        for i in range(len(listLines)):
            if (i==index-1):
                print(colors.HEADER + str(i+1).rjust(3) + ' | ' + colors.WARNING + listLines[i]+ colors.FAIL + "    <-- Error here" + colors.WARNING)
                errorline += [i+1]
            else:
                print(colors.HEADER + str(i+1).rjust(3) + ' | ' + colors.WARNING + listLines[i])
        print(colors.ENDC, end = "")
        print(colors.HEADER + "-------------------------------------------------------------------" + colors.HEADER )
        print(colors.FAIL + "Syntax Error in Line " + str(errorline[0]) + colors.ENDC)
