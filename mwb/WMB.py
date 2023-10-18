import random
import math
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

# Esta função calcula e a atualiza a lista de energia para as 1000 partículas
def colisions(particles): 
    p1 = random.randint(a=0, b=999)
    p2 = random.randint(a=0, b=999)
    if particles[p1]<100 and particles[p2]>1:
        particles[p1] += 1
        particles[p2] -= 1
    return(particles)

# Lista de partículas todas com 10 de energia
particles = [10] * 1000

# For loop que usa o input do utilizador para os cálculos
user_input = int(input("Número de colisões: "))
for i in range(user_input):
    particles = colisions(particles)

# Imprime a lista de partículas de modo a mostrar as suas energias/nivél energético
print(particles)

# getcontext() é usado para aumentar a precisão dos cálculos, neste caso para 2000 casas decimais
getcontext().prec = 2000

# Faz o cálculo da equção de Maxwell-Boltzman
def maxboltz():
    counter = 1
    # Este for loop calcula o produtório de cada nivél energético, dividindo 1 (degenerescência) pelo fatorial do número de partículas com esse nivél energético
    for i in range(1,101):
        particles_count = particles.count(i)
        if particles_count != 0:
            counter *= Decimal((1)/math.factorial(particles_count))
        else: continue
    soma = 0
    # Este for loop calcula o ln de WMB, para isso separa a multiplicação do logaritmo de 1000! em soma de logaritmos de 1 a 1000
    for i in range(1, len(particles)+1):
        soma += Decimal(math.log(i))
    # soma é o ln de WMB
    soma += Decimal.ln(counter)
    return(f"O valor de ln(WMB) é {soma.__round__(2)}.")

print(maxboltz())

# Desenha um gráfico de modo a ver se a energia das partículas obdece à distribuição
fig, ax = plt.subplots()
ax.hist(particles, rwidth=0.8, bins=100)
plt.xticks(range(0, 101, 10))
plt.title("Distribuição de energia das partículas")
plt.xlabel("Nível energético")
plt.ylabel("Quantidade de partículas")
plt.show()