# Ejercicio 2 - Grafo
'''
Ejercicio 2: Dado un grafo no dirigido con personajes de la saga Star Wars, implementar los algoritmos necesarios para resolver las siguientes tareas:
• cada vértice debe almacenar el nombre de un personaje, las aristas representan la cantidad de episodios en los que aparecieron juntos ambos personajes que se relacionan;
• hallar el árbol de expansión mínimo desde el vértice que contiene a: C-3PO, Yoda y Leia;
• determinar cuál es el número máximo de episodio que comparten dos personajes, e indicar todos los pares de personajes que coinciden con dicho número;
• cargue al menos los siguientes personajes: Luke Skywalker, Darth Vader, Yoda, Boba Fett, C-3PO, Leia, Rey, Kylo Ren, Chewbacca, Han Solo, R2-D2, BB-8;
• calcule el camino mas ccorto desde: C-3PO a R2-D2 y desde Yoda a Darth Vader;
• indicar qué personajes aparecieron en los nueve episodios de la saga.

Importante una vez terminado el parcial subirlo a github y pegar el link en la entrega.
'''

from ED_graph import Graph
from ED_heap import HeapMin
from ED_list import List
from ED_stack import Stack
from ej2_grafo_listas import characters, shared_episodes

# --------- CREACIÓN DE FUNCIONES ADICIONALES --------- #

class Graph_Star_Wars(Graph):

    def modified_kruskal(self, origin_vertex):
        def search_in_forest(forest, value):
            for index, tree in enumerate(forest):
                if value in tree:
                    return index
                
        forest = []
        edges = HeapMin()
        for vertex in self:
            forest.append(vertex.value)
            for edge in vertex.edges:
                edges.arrive([vertex.value, edge.value], edge.weight)
        
        while len(forest) > 1 and edges.size() > 0:
            edge = edges.attention()
            origin = search_in_forest(forest, edge[1][0])
            destination = search_in_forest(forest, edge[1][1])
            if origin is not None and destination is not None:
                if origin != destination:
                    if origin > destination:
                        vertex_origin = forest.pop(origin)
                        vertex_destination = forest.pop(destination)
                    else:
                        vertex_destination = forest.pop(destination)
                        vertex_origin = forest.pop(origin)

                    if '|' not in vertex_origin and '|' not in vertex_destination:
                        forest.append(f'{vertex_origin}|{vertex_destination}|{edge[0]}')
                    elif '|' not in vertex_destination:
                        forest.append(vertex_origin+';'+f'{edge[1][0]}|{vertex_destination}|{edge[0]}')
                    elif '|' not in vertex_origin:
                        forest.append(vertex_destination+';'+f'{vertex_origin}|{edge[1][1]}|{edge[0]}')
                    else:
                        forest.append(vertex_origin+';'+vertex_destination+';'+f'{edge[1][0]}|{edge[1][1]}|{edge[0]}')
        
        from_vertex = search_in_forest(forest, origin_vertex)

        if from_vertex is not None:
            return forest[from_vertex]
        else:
            return forest
        
def rebuild_path(elements, destination):
    path = List()
    total_weight = None
    current = destination

    for element in elements:
        if element[0] == current:
            if total_weight is None:
                total_weight = element[1]

            path.insert_value(element[0])
            current = element[2]

    path.reverse()
    return path, total_weight

# --------- CARGA DE DATOS --------- #

graph_star_wars = Graph_Star_Wars()

for character in characters:
    graph_star_wars.insert_vertex(character['name'], character['episodes'])

for origin, destination, weight in shared_episodes:
    graph_star_wars.insert_edge(origin, destination, weight)

# --------- CREACIÓN DE FUNCIONES PARA FORMATO --------- #

class Color:
    RESET   = '\033[0m'
    NEGRITA = '\033[1m'
    CIAN    = '\033[96m'
    ROJO    = '\033[38;2;171;29;29m'     #AB1D1D
    AMARILLO= '\033[38;2;227;187;45m'    #E3BB2D
    AZUL    = '\033[38;2;0;48;176m'      #0030B0
    VERDE   = '\033[38;2;12;120;0m'      #0C7800
    VIOLETA = '\033[38;2;88;31;122m'     #581F7A

def print_seccion(titulo, ancho=140, relleno="-", color=Color.VERDE):
    print(f'\n{color}{f" {titulo} ".center(ancho, relleno)}{Color.RESET}')

def print_seccion_extra(titulo, ancho=140, relleno=" ", color=Color.VERDE):
    print(f'{color}{f" {titulo} ".center(ancho, relleno)}{Color.RESET}')

#################################################  EJECUCIÓN DE PRUEBAS DEL ENUNCIADO  #################################################
print(f'\n{Color.CIAN}{f' EJERCICIO 2: PERSONAJES DE LA SAGA STAR WARS '.center(140, "=")}{Color.RESET}')

# • hallar el árbol de expansión mínimo desde el vértice que contiene a: C-3PO, Yoda y Leia;
print_seccion('• hallar el árbol de expansión mínimo desde el vértice que contiene a: C-3PO, Yoda y Leia;')
origins = ['C-3PO', 'Yoda', 'Leia']
expansion_trees = List()

for origin_vertex in origins:
    expansion_tree = graph_star_wars.modified_kruskal(origin_vertex)
    edges = expansion_tree.split(';')
    edges_list = List()
    for edge in edges:
        origin, destination, weight = edge.split('|')
        edges_list.insert_value((origin, destination, int(weight)))
    expansion_trees.insert_value((origin_vertex, edges_list))

print(f'{Color.VIOLETA}Resultado:{Color.RESET}')
for origin_vertex, edges_list in expansion_trees:
    print(f'\n{Color.AZUL}  Árbol de expansión mínima desde el vértice que contiene a {origin_vertex}: {Color.RESET}')
    suma = 0
    for edge in edges_list:
        suma = suma + edge[2]
        print(f'  → {edge}')
    print(f'\n  → Cantidad de aristas del árbol de expansión: {edges_list.size()}')
    print(f'\n  → Peso total del árbol de expansión: {suma}')

print(f'\n{Color.AMARILLO}Aclaración: el grafo es no dirigido y conexo, por lo que su árbol de expansión mínimo es único. Por lo tanto, no es necesario hallarlo 3 veces. Se calculó de todas formas, a modo de comprobación.{Color.RESET}')


# • determinar cuál es el número máximo de episodio que comparten dos personajes, e indicar todos los pares de personajes que coinciden con dicho número;
print_seccion('• determinar cuál es el número máximo de episodio que comparten dos personajes, ')
print_seccion_extra('e indicar todos los pares de personajes que coinciden con dicho número;')

max_weight = 0
coincidences = List()

print(f'{Color.VIOLETA}Resultado:{Color.RESET}')
print(f'\n{Color.AZUL}  Número máximo de episodios: {Color.RESET}')
for character in graph_star_wars:
    for edge in character.edges:
        if edge.weight > max_weight:
            max_weight = edge.weight
print(f'  → {max_weight}')

for character in graph_star_wars:
    for edge in character.edges:
        if edge.weight == max_weight:
            pair = (character.value, edge.value)
            inverse_pair = (edge.value, character.value)
            if pair not in coincidences and inverse_pair not in coincidences:
                coincidences.insert_value(pair)

print(f'\n{Color.AZUL}  Pares de personajes que compartieron {max_weight} episodios: {Color.RESET}')
for coincidence in coincidences:
    char1, char2 = coincidence
    print(f'  → {char1} | {char2}')

# # • cargue al menos los siguientes personajes: Luke Skywalker, Darth Vader, Yoda, Boba Fett, C-3PO, Leia, Rey, Kylo Ren, Chewbacca, Han Solo, R2-D2, BB-8;
print_seccion('• cargue al menos los siguientes personajes: ')
print_seccion_extra('Luke Skywalker, Darth Vader, Yoda, Boba Fett, C-3PO, Leia, Rey, Kylo Ren, Chewbacca, Han Solo, R2-D2, BB-8;')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')

print(f'\n{Color.AZUL}  Personajes cargados de la saga Star Wars: {Color.RESET}')
for char in graph_star_wars:
    print(f'  → {char.value}')

# • calcule el camino mas ccorto desde: C-3PO a R2-D2 y desde Yoda a Darth Vader;
print_seccion('• calcule el camino mas ccorto desde: C-3PO a R2-D2 y desde Yoda a Darth Vader;')

print(f'{Color.VIOLETA}Resultados:{Color.RESET}')

# Camino desde C-3PO a R2-D2
origin = 'C-3PO'
destination = 'R2-D2'

path = graph_star_wars.dijkstra(origin)

stack_elements = List()     # stack_elements = elementos DE la pila. No quiere decir que stack_elements sea una Pila.
while not path.is_empty():
    stack_elements.insert_value(path.pop())

path, weight = rebuild_path(stack_elements, destination)

print(f'\n{Color.AZUL}  Camino más corto desde {origin} a {destination}: {Color.RESET}')
print(f'  → {' --> '.join(path)}')
print(f'  → Costo total: {weight}')

# Camino desde Yoda a Darth Vader
origin = 'Yoda'
destination = 'Darth Vader'

path = graph_star_wars.dijkstra(origin)

stack_elements = List()
while not path.is_empty():
    stack_elements.insert_value(path.pop())

path, weight = rebuild_path(stack_elements, destination)

print(f'\n{Color.AZUL}  Camino más corto desde {origin} a {destination}: {Color.RESET}')
print(f'  → {' --> '.join(path)}')
print(f'  → Costo total: {weight}')

# • indicar qué personajes aparecieron en los nueve episodios de la saga.
print_seccion('• indicar qué personajes aparecieron en los nueve episodios de la saga.')
in_the_9_episodes = List()
for character in graph_star_wars:
    if len(character.other_values) == 9:
        in_the_9_episodes.insert_value(character.value)

print(f'{Color.VIOLETA}Resultado:{Color.RESET}')
print(f'\n{Color.AZUL}  Personajes que aparecieron en los 9 episodios: {Color.RESET}')
for char in in_the_9_episodes:
    print(f'  → {char}')

print(f'\n{Color.CIAN}{f" FIN DE EJECUCIÓN DEL PROGRAMA ".center(140, "=")}{Color.RESET}')