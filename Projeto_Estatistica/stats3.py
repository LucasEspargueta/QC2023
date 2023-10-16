import numpy as np

list=[]

while True:
    x=input('Introduza os valores: ') 
    if x=='q':
        break
    list.append(int(x))

print("media", np.mean(list))
print("variancia", np.var(list))
print("desvio padrao", round(np.std(list),2))
print("mediana", np.median(list))