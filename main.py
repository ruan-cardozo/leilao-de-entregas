import pandas as pd
import heapq
import networkx as nx
import matplotlib.pyplot as plt

def ler_conexoes(caminho_arquivo: str):
    """
    Lê a matriz de conexões a partir de um arquivo .txt e cria instâncias da classe Conexao.
    """
    # Lê o arquivo CSV como um DataFrame
    matriz = pd.read_csv(caminho_arquivo, delimiter=',', header=None, names=['origem', 'destino', 'tempo'])
    
    # Cria instâncias da classe Conexao para cada linha no DataFrame
    conexoes = [Conexao(row['origem'], row['destino'], row['tempo']) for _, row in matriz.iterrows()]

    return conexoes

def ler_entregas(caminho_arquivo: str):
    """
    Lê a lista de entregas a partir de um arquivo .txt e cria instâncias da classe Entrega.
    """
    # Lê o arquivo CSV como um DataFrame
    entregas_df = pd.read_csv(caminho_arquivo, delimiter=',', header=None, names=['minuto', 'destino', 'bonus'])
    
    # Ordena as entregas pelo 'minuto'
    entregas_df = entregas_df.sort_values(by='minuto')
    
    # Cria instâncias da classe Entrega para cada linha no DataFrame
    entregas = [Entrega(row['minuto'], row['destino'], row['bonus']) for _, row in entregas_df.iterrows()]
    
    return entregas

class Entrega:
    def __init__(self, minuto, destino, bonus):
        self.minuto = minuto
        self.destino = destino
        self.bonus = bonus

    def __repr__(self):
        return f"Entrega(minuto={self.minuto}, destino={self.destino}, bonus={self.bonus})"

class Conexao:
    def __init__(self, origem, destino, tempo):
        self.origem = origem
        self.destino = destino
        self.tempo = tempo

    def __repr__(self):
        return f"Conexao(origem={self.origem}, destino={self.destino}, tempo={self.tempo})"

def criar_grafo(conexoes):
    """
    Cria um grafo direcionado a partir de uma lista de objetos Conexao, incluindo arestas reversas.
    """
    grafo = nx.Graph()

    # Itera sobre as conexões
    for c in conexoes:
        origem = c.origem
        destino = c.destino
        peso = c.tempo
        
        # Adiciona a aresta original (origem -> destino)
        grafo.add_edge(origem, destino, weight=peso)

    return grafo

def dijkstra_entregas_basico(grafo, inicio, entregas):
    """
    Algoritmo de Dijkstra modificado para calcular o melhor caminho com base no bônus e no tempo de entrega,
    considerando as restrições de tempo e maximizando o lucro.
    """
    pq = []  # Fila de prioridade para os caminhos
    heapq.heappush(pq, (0, 0, inicio, []))  # (tempo_total, lucro_total, nó_atual, caminho)

    melhor_lucro = 0
    melhor_caminho = []

    while pq:
        tempo_atual, lucro_atual, node, caminho = heapq.heappop(pq)

        # Atualiza o melhor lucro e caminho se necessário
        if lucro_atual > melhor_lucro:
            melhor_lucro = lucro_atual
            melhor_caminho = caminho

        # Verifica as entregas disponíveis a partir do nó atual
        for entrega in entregas:
            minuto_entrega = entrega.minuto
            destino = entrega.destino
            bonus = entrega.bonus

            # Ignora destinos já entregues
            if destino in [c[1] for c in caminho]:
                continue

            try:
                # Calcula o tempo de viagem até o destino da entrega
                tempo_ate_destino = nx.shortest_path_length(grafo, source=node, target=destino, weight='weight')
                tempo_total_necessario = tempo_atual + tempo_ate_destino

                # Verifica se há caminho de retorno de volta para o ponto inicial
                try:
                    tempo_retorno = nx.shortest_path_length(grafo, source=destino, target=inicio, weight='weight')
                    tempo_total_necessario_com_retorno = tempo_total_necessario + tempo_retorno

                except nx.NetworkXNoPath:
                    # Se não houver caminho de retorno, ignora a entrega
                    continue

                # Verifica se o tempo total para a entrega está dentro do limite
                if tempo_total_necessario <= minuto_entrega:
                    # Adiciona ao heap o novo caminho com o tempo e lucro atualizados
                    novo_lucro = lucro_atual + bonus
                    novo_caminho = caminho + [(tempo_total_necessario_com_retorno, destino, bonus)]
                    heapq.heappush(pq, (tempo_total_necessario_com_retorno, novo_lucro, destino, novo_caminho))

            except nx.NetworkXNoPath:
                # Se não houver caminho até o destino, ignora a entrega
                continue

    return melhor_lucro, melhor_caminho

def a_star_entregas(grafo, inicio, entregas):
    """
    Algoritmo A* para calcular o melhor caminho com base no bônus e no tempo de entrega,
    considerando as restrições de tempo e maximizando o lucro.
    """
    pq = []  # Fila de prioridade para os caminhos
    heapq.heappush(pq, (0, 0, inicio, 0, []))  # (custo_estimado, lucro_total, nó_atual, tempo_atual, caminho)

    melhor_lucro = 0
    melhor_caminho = []

    while pq:
        custo_estimado, lucro_atual, node, tempo_atual, caminho = heapq.heappop(pq)

        # Atualiza o melhor lucro e caminho se necessário
        if lucro_atual > melhor_lucro:
            melhor_lucro = lucro_atual
            melhor_caminho = caminho

        # Verifica as entregas disponíveis a partir do nó atual
        for entrega in entregas:
            minuto_entrega = entrega.minuto
            destino = entrega.destino
            bonus = entrega.bonus

            # Ignora destinos já entregues
            if destino in [c[1] for c in caminho]:
                continue

            # Calcula o tempo de viagem até o destino
            if grafo.has_edge(node, destino):
                tempo_ate_destino = grafo[node][destino]['weight']
            else:
                continue  # Ignora se não houver conexão direta

            tempo_total_necessario = tempo_atual + tempo_ate_destino

            # Calcula o tempo de retorno ao ponto inicial
            if grafo.has_edge(destino, inicio):
                tempo_retorno = grafo[destino][inicio]['weight']
            else:
                tempo_retorno = float('inf')  # Sem caminho de retorno

            tempo_total_necessario_com_retorno = tempo_total_necessario + tempo_retorno

            # Verifica se o tempo total (incluindo retorno) está dentro do limite
            if tempo_total_necessario_com_retorno <= minuto_entrega:
                # Calcula a heurística (lucro potencial restante)
                lucro_potencial = sum(e.bonus for e in entregas if e.destino not in [c[1] for c in caminho])
                custo_estimado = -(lucro_atual + bonus + lucro_potencial)  # Negativo para priorizar maior lucro

                # Adiciona ao heap o novo caminho com o tempo e lucro atualizados
                novo_lucro = lucro_atual + bonus
                novo_caminho = caminho + [(tempo_total_necessario, destino, bonus)]
                heapq.heappush(pq, (custo_estimado, novo_lucro, destino, tempo_total_necessario, novo_caminho))

        # Adiciona a possibilidade de "esperar" para entregas futuras
        for entrega in entregas:
            if entrega.destino not in [c[1] for c in caminho] and tempo_atual < entrega.minuto:
                # Calcula o tempo de espera necessário
                tempo_espera = entrega.minuto - tempo_atual
                heapq.heappush(pq, (custo_estimado, lucro_atual, node, tempo_atual + tempo_espera, caminho))

    return melhor_lucro, melhor_caminho

def simulacao_basica(grafo, entregas):
    """
    Simulação utilizando otimização para maximizar o lucro.
    Retorna as entregas realizadas, o tempo total gasto e o lucro total.
    """
    entregas_realizadas = []
    lucro_total = 0
    tempo_atual = 0  # Começa no ponto A
    ponto_inicial = 'A'

    while entregas:
        # Calcula o melhor caminho e lucro para as entregas restantes
        lucro, melhor_caminho = dijkstra_entregas_basico(grafo, ponto_inicial, entregas)

        if not melhor_caminho:
            # Se não houver mais entregas possíveis, encerra a simulação
            break

        # Atualiza o tempo atual e registra as entregas realizadas
        for tempo, destino, bonus in melhor_caminho:
            tempo_atual = tempo
            entregas_realizadas.append((destino, bonus, tempo))
            lucro_total += bonus

        # Remove as entregas realizadas da lista de entregas pendentes
        entregas = [e for e in entregas if e.destino not in [c[1] for c in melhor_caminho]]

    return {
        "entregas_realizadas": entregas_realizadas,
        "tempo_total": tempo_atual,
        "lucro_total": lucro_total
    }

def simulacao_otimizada(grafo, entregas):
    """
    Simulação utilizando o algoritmo A* para maximizar o lucro.
    Retorna as entregas realizadas, o tempo total gasto e o lucro total.
    """
    entregas_realizadas = []
    lucro_total = 0
    tempo_atual = 0  # Começa no ponto A
    ponto_inicial = 'A'

    while entregas:
        # Calcula o melhor caminho e lucro para as entregas restantes
        lucro, melhor_caminho = a_star_entregas(grafo, ponto_inicial, entregas)

        if not melhor_caminho:
            # Se não houver mais entregas possíveis, encerra a simulação
            break

        # Atualiza o tempo atual e registra as entregas realizadas
        for tempo, destino, bonus in melhor_caminho:
            tempo_atual = tempo
            entregas_realizadas.append((destino, bonus, tempo))
            lucro_total += bonus  # Agora acumulamos o lucro corretamente

        # Remove as entregas realizadas da lista de entregas pendentes
        entregas = [e for e in entregas if e.destino not in [c[1] for c in melhor_caminho]]

    return {
        "entregas_realizadas": entregas_realizadas,
        "tempo_total": tempo_atual,
        "lucro_total": lucro_total
    }

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