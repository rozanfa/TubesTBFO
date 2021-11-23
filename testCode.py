#NIM/Nama  : 16621251/Hana Nadia Iskandar
#Tanggal   : 5 November 2021
#Deskripsi : Problem 2

#KAMUS
#N, P, i, p, o: integer
#arr: array of integers range N

#ALGORTIMA
#inisiasi
N=int(input("Masukkan jumlah hari (N): "))
arr=[0 for i in range (N)]

#Input array
for i in range (N):
    arr[i]=int(input("Masukkan elemen ke "+str(i+1)+": "))

#input pergeseran P
P=int(input("Masukkan P: "))

#proses dan output
for p in range(N-P,N-1): 
    print("Array setelah digeser adalah [",arr[p], end=" ")
for o in range(-1, N-P):
    print(arr[o], end=" ")
print("].")