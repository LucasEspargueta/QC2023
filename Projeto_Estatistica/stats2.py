soma = 0
num = 0
numbers=[]

def media():
    return(soma/num)

def variancia():
    somatorio=0
    for i in numbers:
        somatorio += (i - media())**2
    return(somatorio/len(numbers))
    
def desviop():
    return(round(variancia()**(1/2),2))

def mediana():
    numbers.sort()
    if len(numbers)%2==0:
        return((numbers[int(len(numbers)/2)-1] + numbers[int(len(numbers)/2)])/2)
    else:
        return(numbers[int((len(numbers)+1)/2)])

while True:
    x=input('Introduza os valores: ') 
    if x=='q':
        break
    soma += int(x)
    num += 1
    numbers.append(int(x))

print('A média é : ',media(),'\nA variância é : ',variancia(), '\nO desvio padrão é : ',desviop(),'\nA mediana é: ', mediana())