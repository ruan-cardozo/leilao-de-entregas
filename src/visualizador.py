import matplotlib.pyplot as plt

def plotar_grafico_tempo_lucro(tempos, lucros):
    """
    Plota um gráfico do lucro em relação ao tempo de execução.
    """
    plt.plot(tempos, lucros, marker='o')  # Adicionei marcadores para melhor visualização
    plt.title('Comparação de Lucro e Tempo')
    plt.xlabel('Tempo de Execução (min)')
    plt.ylabel('Lucro (Bônus)')
    plt.grid(True)  # Adiciona uma grade para facilitar a leitura
    plt.show()
