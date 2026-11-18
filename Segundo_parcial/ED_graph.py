# Estructura de dato Grafo

from ED_list import List
from ED_queue import Queue
from ED_heap import HeapMin
from ED_stack import Stack
from typing import Any, Optional

class Graph(List):

    class __nodeVertex:

        def __init__(self, value: Any, other_values: Optional[Any] = None):
            self.value = value
            self.edges = List()
            self.edges.add_criterion('value', Graph._order_by_value)
            self.edges.add_criterion('weight', Graph._order_by_weight)
            self.other_values = other_values
            self.visited = False

        def __str__(self):
            return self.value

    class __nodeEdge:

        def __init__(self, value: Any, weight: Any, other_values: Optional[Any] = None):
            self.value = value
            self.weight = weight
            self.other_values = other_values

        def __str__(self):
            return f'  → Destination: {self.value} | Weight: {self.weight}'

    def _order_by_value(item):
        return item.value

    def _order_by_weight(item):
        return item.weight

    def __init__(self, is_directed: bool = False):

        self.add_criterion('value', self._order_by_value)

        self.is_directed = is_directed

    def show(self) -> None:
        for vertex in self:
            print(f'Vertex: {vertex}')
            vertex.edges.show()

    def insert_vertex(self, value: Any, other_values: Any = None) -> None:
        node_vertex = Graph.__nodeVertex(value, other_values)
        self.insert_value(node_vertex)

    def insert_edge(self, origin_vertex: Any, destination_vertex: Any, weight: int) -> None:
        origin = self.search('value', origin_vertex)
        destination = self.search('value', destination_vertex)
        if origin is not None and destination is not None:
            node_edge_destination = Graph.__nodeEdge(destination_vertex, weight)
            self[origin].edges.insert_value(node_edge_destination)
            if not self.is_directed and origin != destination:
                node_edge_origin = Graph.__nodeEdge(origin_vertex, weight)
                self[destination].edges.insert_value(node_edge_origin)
        else:
            print('No se puede insertar. Falta al menos un vértice.')

    def delete_edge(self, key_value: str, origin: Any, destination: Any) -> Optional[Any]:
        pos_origin = self.search(key_value, origin)
        if pos_origin is not None:
            edge = self[pos_origin].edges.delete_value(key_value, destination)
            if pos_origin is not None and not self.is_directed:
                pos_destination = self.search(key_value, destination)
                if pos_destination is not None:
                    self[pos_destination].edges.delete_value(key_value, origin)
            return edge

    def delete_vertex(self, value, key_value_vertex: str = None, key_value_edges: str = 'value'):
        delete_value = self.delete_value(key_value_vertex, value)
        if delete_value is not None:
            for vertex in self:
                self.delete_edge(key_value_edges, vertex.value, value)
        return delete_value

    def mark_as_unvisited(self) -> None:
        for vertex in self:
            vertex.visited = False

    def exist_path(self, origin, destination):
        def __exist_path(graph, origin, destination):
            result = False
            vertex_pos = graph.search('value', origin)
            if vertex_pos is not None:
                if not graph[vertex_pos].visited:
                    graph[vertex_pos].visited = True
                    if graph[vertex_pos].value == destination:
                        return True
                    for edge in graph[vertex_pos].edges:
                        destination_edge_pos = graph.search('value', edge.value)
                        if not graph[destination_edge_pos].visited:
                            result = __exist_path(graph, graph[destination_edge_pos].value, destination)
                            if result:
                                break
            return result

        self.mark_as_unvisited()
        result = __exist_path(self, origin, destination)
        return result

    def deep_sweep(self, value) -> None:
        def __deep_sweep(graph, value):
            pos_vertex = graph.search('value', value)
            if pos_vertex is not None:
                if graph[pos_vertex].visited is False:
                    graph[pos_vertex].visited = True
                    print(f'  → {graph[pos_vertex]}')
                    for edge in graph[pos_vertex].edges:
                        pos_edge = graph.search('value', edge.value)
                        if graph[pos_edge].visited is False:
                            __deep_sweep(graph, graph[pos_edge].value)

        self.mark_as_unvisited()
        __deep_sweep(self, value)

    def amplitude_sweep(self, value) -> None:
        queue_vertex = Queue()
        self.mark_as_unvisited()
        vertex_pos = self.search('value', value)
        if vertex_pos is not None:
            self[vertex_pos].visited = True
            queue_vertex.arrive(self[vertex_pos])
            while queue_vertex.size() > 0:
                vertex = queue_vertex.attention()
                print(f'  → {vertex.value}')
                for edge in vertex.edges:
                    destination_edge_pos = self.search('value', edge.value)
                    if destination_edge_pos is not None:
                        if self[destination_edge_pos].visited is False:
                            self[destination_edge_pos].visited = True
                            queue_vertex.arrive(self[destination_edge_pos])

    def dijkstra(self, origin):
        from math import inf
        no_visited = HeapMin()
        path = Stack()
        for vertex in self:
            if vertex.value == origin:
                distance = 0
            else:
                distance = inf 
            no_visited.arrive([vertex.value, vertex, None], distance)
        
        while no_visited.size() > 0:
            value = no_visited.attention()
            costo_nodo_actual = value[0]

            path.push([value[1][0], costo_nodo_actual, value[1][2]])
            edges = value[1][1].edges

            for edge in edges:
                pos = no_visited.search(edge.value)
                
                if pos is not None:
                    if costo_nodo_actual + edge.weight < no_visited.elements[pos][0]:
                        no_visited.elements[pos][1][2] = value[1][0]                        
                        no_visited.change_priority(pos, costo_nodo_actual + edge.weight)
                        
        return path

    def kruskal(self, origin_vertex):
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

                    if '-' not in vertex_origin and '-' not in vertex_destination:
                        forest.append(f'{vertex_origin}-{vertex_destination}-{edge[0]}')
                    elif '-' not in vertex_destination:
                        forest.append(vertex_origin+';'+f'{edge[1][0]}-{vertex_destination}-{edge[0]}')
                    elif '-' not in vertex_origin:
                        forest.append(vertex_destination+';'+f'{vertex_origin}-{edge[1][1]}-{edge[0]}')
                    else:
                        forest.append(vertex_origin+';'+vertex_destination+';'+f'{edge[1][0]}-{edge[1][1]}-{edge[0]}')
        
        from_vertex = search_in_forest(forest, origin_vertex)

        if from_vertex is not None:
            return forest[from_vertex]
        else:
            return forest

    def es_adyacente(self, vertex, destination) -> bool:
        vertex_pos = self.search('value', vertex)
        if vertex_pos is not None:
            for edge in self[vertex_pos].edges:
                if edge.value == destination:
                    return True
        return False

    def adyacentes(self, vertex) -> None:
        vertex_pos = self.search('value', vertex)
        if vertex_pos is not None:
            for edge in self[vertex_pos].edges:
                print(edge.value)