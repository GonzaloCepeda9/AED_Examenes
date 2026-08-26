# Ejercicio 2 - Lista
'''
Dada una lista de personajes de marvel (usar el archivo adjunto) debe tener 100 o mas, resolver:
    a. Listado ordenado de manera ascendente por nombre de los personajes.
    b. Determinar en que posicion esta The Thing y Rocket Raccoon.
    c. Listar todos los villanos de la lista.
    d. Poner todos los villanos en una cola para determinar luego cuales aparecieron antes de 1980.
    e. Listar los superheores que comienzan con  Bl, G, My, y W.
    f. Listado de personajes ordenado por nombre real de manera ascendente de los personajes.
    g. Listado de superheroes ordenados por fecha de aparación.
    h. Modificar el nombre real de Ant Man a Scott Lang.
    i. Mostrar los personajes que en su biografia incluyan la palabra time-traveling o suit.
    j. Eliminar a Electro y Baron Zemo de la lista y mostrar su información si estaba en la lista.
'''

from super_heroes_data import superheroes
from superheroe import Superheroe
from TDA_list import List
from TDA_queue import Queue

# ---------------------------------------------------------- Carga de datos ----------------------------------------------------------- #
lista_superheroes = List()
for superheroe in superheroes:
    lista_superheroes.append(Superheroe(**superheroe))

# ------------------------------------------ Creación de funciones para ordenar por criterio ------------------------------------------ #
def order_by_name(superheroe):
    return superheroe.name

def order_by_alias(superheroe):
    return superheroe.alias

def order_by_real_name(superheroe):
    return superheroe.real_name

def order_by_short_bio(superheroe):
    return superheroe.short_bio

def order_by_first_appearance(superheroe):
    return superheroe.first_appearance

def order_by_is_villain(superheroe):
    return superheroe.is_villain

# ------------------------------------------------ Agregación de criterios de búsqueda ------------------------------------------------ #
lista_superheroes.add_criterion('name', order_by_name)
lista_superheroes.add_criterion('alias', order_by_alias)
lista_superheroes.add_criterion('real_name', order_by_real_name)
lista_superheroes.add_criterion('short_bio', order_by_short_bio)
lista_superheroes.add_criterion('first_appearance', order_by_first_appearance)
lista_superheroes.add_criterion('is_villain', order_by_is_villain)

#################################################  Ejecución de pruebas del enunciado  #################################################
print(f'\nLista original de superhéroes: ')
lista_superheroes.show()

# a. Listado ordenado de manera ascendente por nombre de los personajes.
print('\n---------------------------------------- a. Listado ordenado por nombre de personaje -----------------------------------------')
lista_superheroes.sort_by_criterion('name')
lista_superheroes.show()

# b. Determinar en que posicion esta The Thing y Rocket Raccoon.
print('\n---------------------------------------- b. Determinación de posición de personajes ------------------------------------------')
personaje1 = 'The Thing'
posicion = lista_superheroes.search('alias', personaje1)
if posicion is not None:
    print(f'El personaje "{personaje1}" se encuentra en la posición {posicion}.')
else:
    print(f'El personaje "{personaje1}" no se encuentra en la lista."')

personaje2 = 'Rocket Raccoon'
posicion = lista_superheroes.search('alias', personaje2)
if posicion is not None:
    print(f'El personaje "{personaje2}" se encuentra en la posición {posicion}.')
else:
    print(f'El personaje "{personaje2} no se encuentra en la lista."')

# c. Listar todos los villanos de la lista.
print('\n-------------------------------------------- c. Listado de superhéroes villanos ----------------------------------------------')
lista_villanos = List()
for personaje in lista_superheroes:
    if personaje.is_villain == True:
        lista_villanos.insert_value(personaje)

if not lista_villanos.is_empty():
    print(f'Lista con personajes villanos: ')
    lista_villanos.show()
else:
    print('No se encontró ningún personaje villano.')

# d. Poner todos los villanos en una cola para determinar luego cuales aparecieron antes de 1980.
print('\n------------------ d. Colocación de villanos en una cola y muestreo de los que aparecieron antes de 1980 ---------------------')
cola_villanos = Queue()
for villano in lista_villanos:
    cola_villanos.arrive(villano)
print(f'Cola con personajes villanos: ')
cola_villanos.show()

cola_antiguos = Queue()
anio = 1980
for _ in range(cola_villanos.size()):
    personaje_frente = cola_villanos.on_front()
    if personaje_frente.first_appearance < anio:
        cola_antiguos.arrive(personaje_frente)
    cola_villanos.move_to_end()

if not cola_antiguos.is_empty():
    print(f'\nVillanos que aparecieron antes del año {anio}: ')
    cola_antiguos.show()
else:
    print(f'\nNo se encontraron villanos cuya primera aparición es anterior al año 1980.')

# e. Listar los superheores que comienzan con  Bl, G, My, y W.
print('\n------------------------------------ e. Listado de superéroes según caracteres iniciales -------------------------------------')
lista_auxiliar = List()
iniciales = ('Bl', 'G', 'My', 'W')
print(f'Iniciales: {iniciales}')
for superheroe in lista_superheroes:
    if superheroe.name.startswith(iniciales):
        lista_auxiliar.insert_value(superheroe)

if not lista_auxiliar.is_empty():
    print(f'\nLista de superheroes cuyos nombres comienzan con {iniciales}: ')
    lista_auxiliar.show()
else:
    print(f'\nNo se encontraron superhéroes cuyos nombres comiencen con {iniciales}')

# f. Listado de personajes ordenado por nombre real de manera ascendente de los personajes.
print('\n-------------------------- f. Listado de personajes ordenados por nombre real de manera ascendente ---------------------------')
lista_superheroes.sort_by_criterion('real_name')
lista_superheroes.show()

# g. Listado de superheroes ordenados por fecha de aparación.
print('\n--------------------------------- g. Listado de personajes ordenados por fecha de aparición ----------------------------------')
lista_superheroes.sort_by_criterion('first_appearance')
lista_superheroes.show()

# h. Modificar el nombre real de Ant Man a Scott Lang.
print('\n---------------------------------- h. Modificación del nombre real de Ant Man a Scott Lang -----------------------------------')
nombre_superheroe = 'Ant Man'
nuevo_nombre_real = 'Scott Lang'
position = lista_superheroes.search('name', nombre_superheroe)
if position is not None:
    lista_superheroes[position].real_name = nuevo_nombre_real
    print(f'El nombre del superhéroe {nombre_superheroe} ha sido modificado a {nuevo_nombre_real}')
else:
    print(f'El superhéroe {nombre_superheroe} no se encuentra en la lista.')

# i. Mostrar los personajes que en su biografia incluyan la palabra time-traveling o suit.
print('\n--------------------------- i. Muestra de personajes cuya biografía menciona palabras específicas ----------------------------')
palabra1 = 'time-traveling'
palabra2 = 'suit'
print(f'Palabras mencionadas: "{palabra1}" ó "{palabra2}": ')
for superheroe in lista_superheroes:
    if palabra1 in superheroe.short_bio or palabra2 in superheroe.short_bio:
        print(f'{superheroe}')

# j. Eliminar a Electro y Baron Zemo de la lista y mostrar su información si estaba en la lista.
print('\n--------------------------------- j. Eliminación de personajes y muestreo de su información ----------------------------------')
nombre_superheroe1 = 'Electro'
personaje = lista_superheroes.delete_value('name', nombre_superheroe1)
if personaje is not None:
    print(f'El personaje "{nombre_superheroe1}" ha sido eliminado.')
    print(personaje)
else:
    print(f'El personaje "{nombre_superheroe1}" no se encuentra en la lista.')

nombre_superheroe2 = 'Baron Zemo'
personaje = lista_superheroes.delete_value('name', nombre_superheroe2)
if personaje is not None:
    print(f'El personaje "{nombre_superheroe2}" ha sido eliminado.')
    print(personaje)
else:
    print(f'El personaje "{nombre_superheroe2}" no se encuentra en la lista.')