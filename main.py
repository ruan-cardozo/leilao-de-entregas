from src.leitor_dados import ler_conexoes, ler_entregas
from src.simulador import simulacao_basica, simulacao_otimizada
from src.visualizador import plotar_grafico_tempo_lucro
from src.grafo_conexoes import criar_grafo

def main():
    # Ler dados
    conexoes = ler_conexoes('data/conexoes.txt')
    entregas = ler_entregas('data/entregas.txt')

    # Criar o grafo a partir das conexões
    grafo = criar_grafo(conexoes)

    # Rodar simulações
    print("Executando simulação básica...")
    resultado_basico = simulacao_basica(grafo, entregas)
    print("Resultados da Simulação Básica:")
    print(f"Entregas realizadas: {resultado_basico['entregas_realizadas']}")
    print(f"Tempo total gasto: {resultado_basico['tempo_total']} minutos")
    print(f"Lucro total: {resultado_basico['lucro_total']}")

    print("\nExecutando simulação otimizada...")
    resultado_otimizado = simulacao_otimizada(grafo, entregas)
    print("Resultados da Simulação Otimizada:")
    print(f"Entregas realizadas: {resultado_otimizado['entregas_realizadas']}")
    print(f"Tempo total gasto: {resultado_otimizado['tempo_total']} minutos")
    print(f"Lucro total: {resultado_otimizado['lucro_total']}")

    # Exibir gráficos comparando os lucros
    print("\nGerando gráfico de comparação...")
    plotar_grafico_tempo_lucro(
        ['Simulação Básica', 'Simulação Otimizada'],
        [resultado_basico['lucro_total'], resultado_otimizado['lucro_total']]
    )

if __name__ == '__main__':
    main()