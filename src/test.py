import random
import math

def parse_input(filename):
    """ Lê a entrada de um arquivo .dat no formato especificado """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    n, delta, T_max = map(int, lines[0].split())
    m = int(lines[1])
    
    resources = []
    for i in range(2, 2 + m):
        t, k = map(int, lines[i].split())
        resources.extend([t] * k)
    
    graph = {}
    for line in lines[2 + m:]:
        x1_y1, x2_y2, t = line.split()
        x1, y1 = map(int, x1_y1.split('-'))
        x2, y2 = map(int, x2_y2.split('-'))
        u, v = (x1, y1), (x2, y2)
        if u not in graph:
            graph[u] = []
        graph[u].append((v, int(t)))
    
    print("Grafo carregado:", graph)
    print("Recursos disponíveis:", resources)
    print("Delta:", delta, "Tempo máximo:", T_max)
    
    return graph, delta, resources, T_max

def simulated_annealing(graph, delta, resources, T_max, alpha=0.99, T_min=1e-3):
    """ Implementa Simulated Annealing para minimizar a disseminação de fake news """
    def propagate_news(alloc):
        """ Simula a propagação da fake news com a alocação de recursos """
        reached = set()
        queue = [(0, (1, 1))]  # Começa do servidor inicial (1,1) no tempo 0
        while queue:
            time, node = queue.pop(0)
            if time > T_max:
                continue
            reached.add(node)
            for neighbor, t_uv in graph.get(node, []):
                delay = delta if alloc.get(node, None) is not None else 0
                queue.append((time + t_uv + delay, neighbor))
        
        print("Propagação finalizada. Servidores atingidos:", reached)
        return len(reached)
    
    # Inicializa alocação vazia
    current_alloc = {}
    best_alloc = current_alloc.copy()
    best_cost = propagate_news(current_alloc)
    
    print("Custo inicial:", best_cost)
    
    T = T_max  # Define temperatura inicial
    
    while T > T_min:
        new_alloc = current_alloc.copy()
        server = random.choice(list(graph.keys()))
        if server in new_alloc:
            del new_alloc[server]  # Remove recurso
        else:
            new_alloc[server] = random.choice(resources)  # Adiciona recurso aleatório
        
        new_cost = propagate_news(new_alloc)
        delta_cost = new_cost - best_cost
        
        print(f"Nova alocação: {new_alloc}, Novo custo: {new_cost}, Delta: {delta_cost}, Temperatura: {T}")
        
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / T):
            current_alloc = new_alloc
            if new_cost < best_cost:
                best_alloc, best_cost = new_alloc, new_cost
        
        T *= alpha  # Resfriamento
    
    return best_alloc, best_cost

if __name__ == "__main__":
    filename = "./instances/fn1.dat"  # Altere para o nome correto do arquivo
    graph, delta, resources, T_max = parse_input(filename)
    solution, cost = simulated_annealing(graph, delta, resources, T_max)
    print("Melhor alocação:", solution)
    print("Servidores atingidos:", cost)


