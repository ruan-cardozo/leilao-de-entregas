from src.grafo_conexoes import dijkstra_entregas_basico
from src.grafo_conexoes import a_star_entregas

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

from src.grafo_conexoes import a_star_entregas

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
