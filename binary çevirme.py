import numpy as np 

def convert_bin(a,b):
    c= a+b
    return bin(c)[2:]




def convert_bin_2(a, b):
    c = a + b
    arr = []
    i=0
    while c > 0:
        arr.append(c % 2)
        c = c // 2

    while (i<len(arr)):
        print(arr[i], end="")
        i+=1
    return""


a= input("sayi girin ")
b= input("sayi girin ")
a,b=int(a),int(b)
print (convert_bin_2(a,b))


     




    
     

