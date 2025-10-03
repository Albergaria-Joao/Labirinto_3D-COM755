# Labirinto 3D - COM755  

Este projeto foi desenvolvido como parte da disciplina **Computação de Alto Desempenho**, ministrada pelo Prof. MSc. Sérgio Yoshioka, e tem como objetivo explorar diferentes algoritmos de busca em um **labirinto tridimensional (de até 100×100×100)**, analisando desempenho, complexidade e aplicabilidade em cenários de alta dimensão.  

Autores:
- Gabriel Palace Novaes Henrique | RA 202310491
- João Vítor Albergaria Barbosa | RA 202310501

---

## ✨ Funcionalidades  
- Geração e visualização interativa de labirintos 3D em Python.  
- Com **paredes, teleportes para o início e saída** posicionados aleatoriamente.  
- Implementação e comparação de diferentes algoritmos de busca de caminho:  
  - **Autoral (multithread e randômico com backtracking)**  
  - **Breadth-First Search (BFS)**  
  - **Depth-First Search (DFS)**  
  - **Dijkstra**  
  - **Bellman-Ford**  
- Visualização dos resultados com **Matplotlib 3D**.  

---

## ⚙️ Algoritmos e Desempenho  
- **BFS** → Melhor desempenho prático no labirinto 100³, garantindo o menor número de passos e menor tempo.  
- **Dijkstra** → Bom desempenho, considerando pesos, mas gera caminhos mais longos.  
- **Bellman-Ford** → Muito custoso (O(N⁶)), porém encontra resultados corretos.  
- **DFS** → Simples, mas sujeito a *stack overflow* em grandes dimensões.  
- **Autoral** → Exploração paralela e randômica; eficaz em labirintos pequenos, mas ineficiente em grandes (tende a vagar).
- **Autoral v2** → Versão do autoral que leva em consideração também os valores de cada célula do labirinto [-5, 5] em busca do caminho com maior pontuação

---

## 📈 Complexidade dessa implementação
- **BFS / DFS** → `O(N³)`  
- **Dijkstra** → `O(N³ log N³)`  
- **Bellman-Ford** → `O(N⁶)`  
- **Autoral** → Variável, até `O(N³)` no pior caso  

---

## 🚀 Melhorias Futuras  
- Compartilhamento de informações entre threads no algoritmo autoral.  
- Armazenamento de múltiplos caminhos para análise estatística.  
- Uso de heurísticas (como no A*) para guiar a busca.  
- Paralelização real com `multiprocessing` ou GPU.  

---

## 📚 Referências  
- [GeeksforGeeks - BFS](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)  
- [GeeksforGeeks - DFS](https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/)  
- [GeeksforGeeks - Bellman-Ford](https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23/)  
- [GeeksforGeeks - Dijkstra](https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7)  
- [WilliamFiset - DFS (YouTube)](https://www.youtube.com/watch?v=7fujbpJ0LB4)  
- [Abdul Bari - BFS & DFS (YouTube)](https://www.youtube.com/watch?v=pcKY4hjDrxk)  
- [VisuAlgo - Visualização interativa](https://visualgo.net/en/sssp)  
