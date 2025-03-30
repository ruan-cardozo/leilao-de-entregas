import heapq
import networkx as nx

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
                    novo_caminho = caminho + [(tempo_total_necessario, destino, bonus)]
                    heapq.heappush(pq, (tempo_total_necessario, novo_lucro, destino, novo_caminho))

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