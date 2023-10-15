import random
import math
import matplotlib.pyplot as plt

#Esta função calcula e a atualiza a lista de energia para as 1000 partículas
def colisions(particles): 
    p1 = random.randint(a=0, b=999)
    p2 = random.randint(a=0, b=999)
    particles[p1] += 1
    particles[p2] -= 1
    return(particles)

#Lista de partículas todas com 10 de energia
particles = [10] * 1000

#For loop que usa o input do utilizador para os cálculos
user_input = int(input("Número de colisões (entre 0 e 65536): "))
if user_input <= 65536:
    for i in range(user_input):
        particles = colisions(particles)
else: 
    exit()

#Imprime a lista de partículas de modo a mostrar as suas energias/nivél energético
print(particles)

#Faz o cálculo da equção de Maxwell-Boltzman
i_input = int(input('Nível energético: '))
def maxboltz():
    i = particles.count(i_input)
    a = int(math.factorial(1000) * (1**i)//math.factorial(i))
    return(f"O valor de WMB é {math.log(a, math.e)} e a quantidade de partículas no nivél energético {i_input} é de {i}")

print(maxboltz())

#Desenha um gráfico de modo a ver se a energia das partículas obdece à distribuição normal
fig, ax = plt.subplots()
ax.hist(particles, rwidth=0.5)
plt.xlabel("Nivél energético")
plt.ylabel("Quantidade de partículas")
plt.show()