import pandas as pd

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