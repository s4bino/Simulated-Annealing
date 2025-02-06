import random
import math

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
    
    for s in grafo:  # Qualquer vértice pode ser inicial
        fila = [(s, 0)]
        visitados = set()
        
        while fila:
            v, tempo = fila.pop(0)
            if v in visitados or tempo > T:
                continue
            visitados.add(v)
            infectados.add(v)
            
            for vizinho, t in grafo[v]:
                atraso = delta if v in alocacao_recursos else 0
                fila.append((vizinho, tempo + t + atraso))
    
    return len(infectados)

# Função de vizinhança
def gerar_vizinhos(alocacao_recursos, servidores):
    novo_estado = alocacao_recursos[:]
    if novo_estado:
        novo_estado[random.randint(0, len(novo_estado) - 1)] = random.choice(servidores)
    return novo_estado

# Inicialização dos recursos
def inicializar_alocacao(servidores, recursos):
    return random.sample(servidores, min(len(servidores), len(recursos)))

# Simulated Annealing
def simulated_annealing(grafo, servidores, T_max, delta, recursos, iteracoes=1000, T_ini=100, T_min=1):
    alocacao_recursos = inicializar_alocacao(servidores, recursos)
    custo_atual = calcular_custo(grafo, alocacao_recursos, T_max, delta)
    
    T = T_ini
    for i in range(iteracoes):
        novo_estado = gerar_vizinhos(alocacao_recursos, servidores)
        custo_novo = calcular_custo(grafo, novo_estado, T_max, delta)
        
        if custo_novo < custo_atual or random.random() < math.exp((custo_atual - custo_novo) / T):
            alocacao_recursos = novo_estado
            custo_atual = custo_novo
        
        # Resfriamento
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
