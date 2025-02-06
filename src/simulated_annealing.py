import random
import math
from collections import deque

# Classe para representar o grafo
def parse_instancia(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    # Linha 1: delta, T
    _, delta, T_max = map(int, linhas[0].split())
    
    # Linha 2: Número de grupos de recursos
    m = int(linhas[1])
    
    # Próximas m linhas: tempos de disponibilização dos recursos
    recursos = []
    for i in range(2, 2 + m):
        t, k = map(int, linhas[i].split())
        recursos.extend([t] * k)
    
    # Restante: arestas do grafo
    grafo = {}
    for linha in linhas[2 + m:]:
        if linha.strip():
            x1_y1, x2_y2, t = linha.strip().split()
            x1, y1 = map(int, x1_y1.split('-'))
            x2, y2 = map(int, x2_y2.split('-'))
            t = int(t)
            u = (x1, y1)
            v = (x2, y2)
            grafo.setdefault(u, []).append((v, t))
            grafo.setdefault(v, []).append((u, t))  # Grafo não-direcionado
    
    return delta, T_max, recursos, grafo

# Função de custo (número total de infecções)
def calcular_custo(grafo, alocacao_recursos, T, delta):
    infectados = set()
    pior_caso = 0
    
    for s in grafo:  # Simula a fake news começando de cada nó
        fila = deque([(s, 0)])
        visitados = set()
        temp_infectados = set()
        
        while fila:
            v, tempo = fila.popleft()
            if v in visitados or tempo > T:
                continue
            visitados.add(v)
            temp_infectados.add(v)
            
            for vizinho, t in grafo[v]:
                atraso = delta if v in alocacao_recursos else 0
                if tempo + t + atraso <= T:
                    fila.append((vizinho, tempo + t + atraso))
        
        pior_caso = max(pior_caso, len(temp_infectados))
    
    return pior_caso

# Função de vizinhança
def gerar_vizinhos(alocacao_recursos, servidores):
    novo_estado = alocacao_recursos[:]
    if novo_estado:
        for _ in range(len(novo_estado) // 2 + 1):  # Modifica múltiplos recursos
            novo_estado[random.randint(0, len(novo_estado) - 1)] = random.choice(servidores)
    return novo_estado

# Inicialização dos recursos de forma estratégica
def inicializar_alocacao(servidores, recursos, grafo):
    # Escolher servidores com maior grau (mais conexões)
    servidores_ordenados = sorted(servidores, key=lambda v: -len(grafo[v]))
    return servidores_ordenados[:min(len(servidores), len(recursos))]

# Simulated Annealing
def simulated_annealing(grafo, servidores, T_max, delta, recursos, iteracoes=5000, T_ini=200, T_min=0.1):
    alocacao_recursos = inicializar_alocacao(servidores, recursos, grafo)
    custo_atual = calcular_custo(grafo, alocacao_recursos, T_max, delta)
    
    T = T_ini
    for i in range(iteracoes):
        novo_estado = gerar_vizinhos(alocacao_recursos, servidores)
        custo_novo = calcular_custo(grafo, novo_estado, T_max, delta)
        
        if custo_novo < custo_atual or random.random() < math.exp((custo_atual - custo_novo) / T):
            alocacao_recursos = novo_estado
            custo_atual = custo_novo
        
        # Resfriamento mais lento
        T = max(T_min, T * 0.95)
        
    return alocacao_recursos, custo_atual

# Execução principal
def main():
    arquivo = './instances/fn1.dat'  # Nome do arquivo de entrada
    delta, T_max, recursos, grafo = parse_instancia(arquivo)
    servidores = list(grafo.keys())
    
    melhor_alocacao, menor_custo = simulated_annealing(grafo, servidores, T_max, delta, recursos)
    
    print("Melhor alocação de recursos:", melhor_alocacao)
    print("Menor número de servidores infectados:", menor_custo)

if __name__ == "__main__":
    main()
