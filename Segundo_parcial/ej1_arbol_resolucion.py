# Ejercicio 1 - Árbol
'''
Ejercicio 1: Se tiene los datos de Pokémons de las 9 generaciones cargados de manera aleatoria (1025 en total) de los cuales se conoce su nombre, número, tipo/tipos, debilidad frente a tipo/tipos, si tiene mega evolucion (bool) y si tiene forma gigamax (bool) para el cual debemos construir tres árboles para acceder de manera eficiente a los datos contemplando lo siguiente:
los índices de cada uno de los árboles deben ser nombre, número y tipo;
mostrar todos los datos de un Pokémon a partir de su número y nombre –para este último, la búsqueda debe ser por proximidad, es decir si busco “bul” se deben mostrar todos los Pokémons cuyos nombres comiencen o contengan dichos caracteres–;
mostrar todos los nombres de los Pokémons de un determinado tipo: fantasma, fuego, acero y eléctrico;
realizar un listado en orden ascendente por número y nombre de Pokémon, y además un listado por nivel por nombre;
mostrar todos los Pokémons que son débiles frente a Jolteon, Lycanroc y Tyrantrum;
mostrar todos los tipos de Pokémons y cuántos hay de cada tipo;
determinar cuantos Pokémons tienen megaevolucion.
determinar cuantos Pokémons tiene forma gigamax.
cargue al menos 100 Pokémons.
'''

from typing import Any
from ED_list import List
from ED_tree import BinaryTree
from ej1_arbol_lista import lista_pokemons

# --------- CREACIÓN DE FUNCIONES ADICIONALES --------- #

class BinaryTreePokemon(BinaryTree):

    def proximity_search(self, value: Any):
        value_lower = value.lower()
        def __search(root, value):
            if root is not None:
                name_lower = root.value.lower()
                if name_lower.startswith(value_lower) or value_lower in name_lower:
                    print(f'  → {root.value} | {root.other_values}')
                __search(root.left, value)
                __search(root.right, value)

        aux = None
        if self.root is not None:
            aux = __search(self.root, value)
        return aux

    def show_names_by_type(self, type_name):
        def __search(root, type_name):
            if root is not None:
                __search(root.left, type_name)
                if root.value == type_name:
                    print(f'  → {root.other_values["nombre"]}')
                __search(root.right, type_name)

        if self.root is not None:
            __search(self.root, type_name)

    def show_weak_against(self, attacker_types):

        attacker_types_flat = List()
        for types in attacker_types:
            for type_name in types:
                if type_name not in attacker_types_flat:
                    attacker_types_flat.insert_value(type_name)

        def __search(root, attacker_types_flat):
            if root is not None:
                __search(root.left, attacker_types_flat)
                weaknesses = root.other_values['debilidades']
                match = False
                for type_name in attacker_types_flat:
                    if type_name in weaknesses:
                        match = True
                if match:
                    print(f'  → {root.value}')
                __search(root.right, attacker_types_flat)

        if self.root is not None:
            __search(self.root, attacker_types_flat)

    def get_unique_types(self):
        types = List()
        def __search(root, types):
            if root is not None:
                __search(root.left, types)
                if root.value not in types:
                    types.insert_value(root.value)
                __search(root.right, types)

        if self.root is not None:
            __search(self.root, types)

        return types

    def count_by_type(self, types):
        for type_name in types:
            def __search(root, type_name, counter):
                if root is not None:
                    counter = __search(root.left, type_name, counter)
                    if root.value == type_name:
                        counter += 1
                    counter = __search(root.right, type_name, counter)
                return counter

            counter = 0
            if self.root is not None:
                counter = __search(self.root, type_name, counter)

            print(f'  → {type_name}: {counter}')

    def count_by_boolean(self, key):
        def __search(root, counter, key):
            if root is not None:
                counter = __search(root.left, counter, key)
                if root.other_values[key] is True:
                    counter += 1
                counter = __search(root.right, counter, key)
            return counter

        counter = 0
        if self.root is not None:
            counter = __search(self.root, counter, key)

        return counter

    def count_nodes(self):
        def __search(root, counter):
            if root is not None:
                counter += 1
                counter = __search(root.left, counter)
                counter = __search(root.right, counter)
            return counter

        if self.root is not None:
            return __search(self.root, 0)
        return 0
    
# --------- CARGA DE DATOS --------- #

arbol_pokemons_nombre = BinaryTreePokemon()
arbol_pokemons_numero = BinaryTreePokemon()
arbol_pokemons_tipos = BinaryTreePokemon()

for pokemon in lista_pokemons:
    datos = {
        'nombre': pokemon['nombre'],
        'numero': pokemon['numero'],
        'tipos': pokemon['tipos'],
        'debilidades': pokemon['debilidades'],
        'mega_evolucion': pokemon['mega_evolucion'],
        'gigamax': pokemon['gigamax'],
    }

    datos_copy_1 = datos.copy()
    datos_copy_1.pop('nombre')
    arbol_pokemons_nombre.insert(pokemon['nombre'], datos_copy_1)

    datos_copy_2 = datos.copy()
    datos_copy_2.pop('numero')
    arbol_pokemons_numero.insert(pokemon['numero'], datos_copy_2)

    datos_copy_3 = datos.copy()
    datos_copy_3.pop('tipos')
    for tipo in pokemon['tipos']:
        arbol_pokemons_tipos.insert(tipo, datos_copy_3)

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
print(f'\n{Color.CIAN}{f' EJERCICIO 1: POKÉMONS '.center(140, "=")}{Color.RESET}')

# • los índices de cada uno de los árboles deben ser nombre, número y tipo;
print_seccion('• los índices de cada uno de los árboles deben ser nombre, número y tipo;')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')
print(f'  → Árbol 1: cargado por nombre')
print(f'  → Árbol 2: cargado por número')
print(f'  → Árbol 3: cargado por tipo')

# • mostrar todos los datos de un Pokémon a partir de su número y nombre –para este último, la búsqueda debe ser por proximidad, es decir si busco “bul” se deben mostrar todos los Pokémons cuyos nombres comiencen o contengan dichos caracteres–;
print_seccion('• mostrar todos los datos de un Pokémon a partir de su número y nombre –para este último, la búsqueda debe ser por proximidad,')
print_seccion_extra('es decir si busco “bul” se deben mostrar todos los Pokémons cuyos nombres comiencen o contengan dichos caracteres–;')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')

print(f'{Color.AZUL}\n  Datos de un Pokémon a partir de su número: {Color.RESET}')
numero_buscado = 9
pokemon_buscado = arbol_pokemons_numero.search(numero_buscado)
if pokemon_buscado is not None:
    print(f'  → {pokemon_buscado.value} | {pokemon_buscado.other_values}')
else:
    print(f'  → El Pokémon n° {numero_buscado} no se encuentra en el árbol.')

print(f'{Color.AZUL}\n  Datos de un Pokémon a partir de su nombre (búsqueda por proximidad): {Color.RESET}')
coincidencia_buscada = 'ra'
print(f'  Coincidencia buscada: "{coincidencia_buscada}"')
arbol_pokemons_nombre.proximity_search(coincidencia_buscada)

# • mostrar todos los nombres de los Pokémons de un determinado tipo: fantasma, fuego, acero y eléctrico;
print_seccion('• mostrar todos los nombres de los Pokémons de un determinado tipo: ')
print_seccion_extra('fantasma, fuego, acero y eléctrico;')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')

tipo_buscado = 'Fantasma'
print(f'{Color.AZUL}\n  Nombres de Pokémons de tipo {tipo_buscado}: {Color.RESET}')
arbol_pokemons_tipos.show_names_by_type(tipo_buscado)

tipo_buscado = 'Fuego'
print(f'{Color.AZUL}\n  Nombres de Pokémons de tipo {tipo_buscado}: {Color.RESET}')
arbol_pokemons_tipos.show_names_by_type(tipo_buscado)

tipo_buscado = 'Acero'
print(f'{Color.AZUL}\n  Nombres de Pokémons de tipo {tipo_buscado}: {Color.RESET}')
arbol_pokemons_tipos.show_names_by_type(tipo_buscado)

tipo_buscado = 'Eléctrico'
print(f'{Color.AZUL}\n  Nombres de Pokémons de tipo {tipo_buscado}: {Color.RESET}')
arbol_pokemons_tipos.show_names_by_type(tipo_buscado)

# • realizar un listado en orden ascendente por número y nombre de Pokémon, y además un listado por nivel por nombre;
print_seccion('• realizar un listado en orden ascendente por número y nombre de Pokémon, ')
print_seccion_extra('y además un listado por nivel por nombre;')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')

print(f'{Color.AZUL}\n  Listado ascendente por número:{Color.RESET}')
arbol_pokemons_numero.in_order()

print(f'{Color.AZUL}\n  Listado ascendente por nombre:{Color.RESET}')
arbol_pokemons_nombre.in_order()

print(f'{Color.AZUL}\n  Listado por nivel por nombre:{Color.RESET}')
arbol_pokemons_nombre.by_level()

# • mostrar todos los Pokémons que son débiles frente a Jolteon, Lycanroc y Tyrantrum;
print_seccion('• mostrar todos los Pokémons que son débiles frente a Jolteon, Lycanroc y Tyrantrum;')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')

atacantes = ['Jolteon', 'Lycanroc', 'Tyrantrum']
tipos_atacantes = List()
for nombre_atacante in atacantes:
    nodo = arbol_pokemons_nombre.search(nombre_atacante)
    if nodo is not None:
        tipos_atacantes.insert_value(nodo.other_values['tipos'])
    else:
        print(f'  → {nombre_atacante} no está en el árbol.')

print(f'{Color.AZUL}\n  Tipos de los Pokémons atacantes: {Color.RESET}')
for tipo in tipos_atacantes:
    for t in tipo:
        print(f'  → {t}')

print(f'{Color.AZUL}\n  Pokémons débiles contra Pokémons de estos tipos: {Color.RESET}')
arbol_pokemons_nombre.show_weak_against(tipos_atacantes)

# • mostrar todos los tipos de Pokémons y cuántos hay de cada tipo;
print_seccion('• mostrar todos los tipos de Pokémons y cuántos hay de cada tipo;')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')

tipos_unicos = arbol_pokemons_tipos.get_unique_types()
print(f'{Color.AZUL}\n  Tipos de los Pokémons: {Color.RESET}')
tipos_unicos.show()

print(f'{Color.AZUL}\n  Cantidad por tipo: {Color.RESET}')
arbol_pokemons_tipos.count_by_type(tipos_unicos)

# • determinar cuántos Pokémons tienen megaevolución
print_seccion('• determinar cuántos Pokémons tienen megaevolución.')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')
cantidad_megaevolucion = arbol_pokemons_nombre.count_by_boolean('mega_evolucion')
print(f'  → Pokémons con megaevolución: {cantidad_megaevolucion}')

# • determinar cuántos Pokémons tienen forma gigamax
print_seccion('• determinar cuántos Pokémons tienen forma gigamax.')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')
cantidad_gigamax = arbol_pokemons_nombre.count_by_boolean('gigamax')
print(f'  → Pokémons con forma gigamax: {cantidad_gigamax}')

# • cargue al menos 100 Pokémons.
print_seccion('• cargue al menos 100 Pokémons.')
print(f'{Color.VIOLETA}Resultado:{Color.RESET}')
cantidad_nodos = arbol_pokemons_nombre.count_nodes()
if cantidad_nodos >= 100:
    print(f'  → El árbol contiene {cantidad_nodos} Pokémons. Por lo tanto, cumple la consigna.')
elif cantidad_nodos > 0 and cantidad_nodos < 100:
    print(f'  → El árbol contiene {cantidad_nodos} Pokémons. Por lo tanto, no cumple la consigna.')
else:
    print(f'  → El árbol está vacío. Por lo tanto, no cumple la consigna.')

print(f'\n{Color.CIAN}{f" FIN DE EJECUCIÓN DEL PROGRAMA ".center(140, "=")}{Color.RESET}')