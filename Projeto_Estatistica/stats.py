soma = 0
num = 0
numbers=[]

def media():
    return(soma/num)

def variancia():
    somatorio=0
    for i in numbers:
        somatorio += (i - media())**2
    return(somatorio/num)
    
def desviop():
    return(round(variancia()**(1/2),2))

#Not currently working
def number(numbers):
    number_of_elements = 0
    for i in numbers:
        number_of_elements += 1
    return(number_of_elements)

#Not currently working
def sort_list(numbers):
    n = number(numbers)
    for i in range(num):
        for j in range(0, num-1-i):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return(numbers)

#Not currently working
def mediana(numbers):
    sorted_list = sort_list(numbers)
    n = number(numbers)
    if num%2==0:
        return((sorted_list[int(num/2)-1] + sorted_list[int(num/2)])/2)
    else:
        return(sorted_list[int((num+1)/2)])

while True:
    x=input('Introduza os valores: ') 
    if x=='q':
        break
    soma += int(x)
    num += 1
    numbers.append(int(x))

print('A média é : ',media(),'\nA variância é : ',variancia(), '\nO desvio padrão é : ',desviop(),'\nA mediana é: ', mediana(numbers))