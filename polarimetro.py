import serial 
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


porta = "COM4"  
baudrate = 9600  # Deve ser o mesmo do Arduino

# Abre a conexão com o Arduino
arduino = serial.Serial(porta, baudrate, timeout=1)
time.sleep(2)  # Aguarda o Arduino iniciar

print("Lendo dados do Arduino...\n")

# Criando uma figura e um eixo 3D
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Gerando as coordenadas da esfera
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v)) #x em coord esféricas com r = 1
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

# Plotando a esfera
ax.plot_surface(x, y, z, color = 'white',edgecolor='none', alpha=0.6)

# Ajustando limites para garantir que o vetor e a esfera caibam bem na visualização
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1]) 

# Ajustando o gráfico
ax.set_title("Esfera de Poincaré")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z") 

plt.ion() #O gráfico abre e atualiza dinamicamente sem precisar ser reaberto a cada iteração. se n tivesse isso, o grafico só ia atualizar qnd a gnt fechasse a guia ent n ia atualizar com nada dentro do loop
plt.show()
 
# Variável para armazenar o objeto do vetor
quiver_obj = None 

global janela_aberta = True
def fechar_figura(event):
    global janela_aberta
    janela_aberta = False  # Define a variável como False quando a janela for fechada
fig.canvas.mpl_connect("close_event", fechar_figura)

while janela_aberta:
    if not plt.fignum_exists(fig.number):  # Verifica se a janela foi fechada
        break
    linha = arduino.readline().decode().strip()  # Lê a linha e decodifica para string
    if linha:  # Garante que a linha não está vazia
        valores = linha.split(",")  # Separa os valores pela vírgula
        if len(valores) == 4:  # Certifica-se de que há 4 valores
            sensor1, sensor2, sensor3, sensor4 = map(int, valores)  # Converte para inteiros
            print(f"S1: {sensor1}, S2: {sensor2}, S3: {sensor3}, S4: {sensor4}")

            vector = np.array([sensor2,sensor3,sensor4])
            vector = vector / np.linalg.norm(vector)

            # Remove o vetor anterior, se existir
            if quiver_obj is not None:
                quiver_obj.remove()

            # Adiciona o novo vetor
            quiver_obj = ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], color='r', linewidth=2, arrow_length_ratio=0.1)
                
            # Atualiza o gráfico sem replotar a esfera
            plt.draw() #redesenha a figura atual
            plt.pause(0.1) # Dá um tempo para atualização do gráfico
                
print("\nEncerrando conexão...")
arduino.close()



