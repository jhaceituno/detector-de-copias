# Programa de comparacion automatica de ficheros
# Desarrollado por Javier Hernandez Aceituno

import sys   # Lectura de parametros y escritura por pantalla
import glob  # Busqueda de ficheros

# ------------------------------------------------------------------------------

# La funcion 'compara' compara dos cadenas de caracters 'fich1' y 'fich2'
# y devuelve el porcentaje de similitud entre ellas

def compara(fich1, fich2):

  i = 0  # Puntero en fich1
  j = 0  # Puntero en fich2
  k = 0  # Desfase para busquedas
  len1 = len(fich1)
  len2 = len(fich2)
  coincidencias = 0

  while i < len1 and j < len2:  # Para todos los caracteres de las cadenas
    if fich1[i] == fich2[j]:    # Si se detecta una coincidencia, se
      coincidencias += 1        # incremente el contador
    else:
      k = 1                     # Si se detecta una diferencia, se intentara
      while 1:                  # encontrar el caracter similar mas proximo
        ik = i+k < len1         # en ambas cadenas
        jk = j+k < len2

        for l in range(k):      # Dentro de un rango incremental k:

          iljk = i+l < len1 and jk
          if iljk and fich1[i+l] == fich2[j+k]:
            coincidencias += 1
            i += l              # Si se encuentra una coindicencia entre
            j += k              # fich[i+l] y fich2[j+k], con l < k,
            k = 0               # se deja de buscar
            break

          ikjl = j+l < len2 and ik
          if ikjl and fich1[i+k] == fich2[j+l]:
            coincidencias += 1
            i += k              # Si se encuentra una coindicencia entre
            j += l              # fich[i+k] y fich2[j+l], con l < k,
            k = 0               # se deja de buscar
            break

          if ik and jk and fich1[i+k] == fich2[j+k]:
            coincidencias += 1
            i += k
            j += k             # Si se encuentra una coindicencia entre
            k = 0              # fich[i+k] y fich2[j+l], se deja de buscar
            break

          if not (iljk or ikjl):
            i += k
            j += k             # Si se llega al final de ambos ficheros,
            k = 0              # se termina el proceso
            break
        if k:
          k += 1
        else:                  # La funcion devuelve el porcentaje de
          break                # coincidencias respecto a la media de
    i += 1                     # las longitudes de los ficheros
    j += 1

  return round((200 * coincidencias) / (len1 + len2), 2)

# ------------------------------------------------------------------------------

# La funcion 'barraCarga' muestra una barra de carga con el texto dado, para
# un cierto valor entero menos que un total

def barraCarga(texto, valor, total):
  marcas = (10 * valor) // total # Se calcula el numero de marcas a mostrar de
                                 # un total de 10, en funcion del porcentaje
  sys.stdout.write(texto + ' [' + ('#' * marcas) +\
    (' ' * (10 - marcas) + '] ' + str((100 * valor) // total) + '%\r'))
  sys.stdout.flush()             # Se muestran las marcas y el porcentaje


# Programa principal -----------------------------------------------------------

manual = '> python ' + sys.argv.pop(0) +\
  ' [-s|n|p|lA|cA,B] {lista de ficheros}\n' +\
  '  -s:    no ignorar espacios\n' +\
  '  -n:    no ignorar saltos de linea\n' +\
  '  -lA:   ignorar comentarios de linea que comiencen por A (ej: -l//)\n  ' +\
  '-cA,B: ignorar comentarios multilinea delimitados por A y B (ej: -c/*,*/)'

sinEspacios = 1       # Indica si se descartan los espacios de los ficheros
sinSaltos = 1         # Indica si se descartan los saltos de linea
comentarioLinea = []  # Comienzo de un comentario de linea
comentarioBloqA = []  # Comienzo de un comentario multilinea
comentarioBloqB = []  # Final de un comentario multilinea
nombres = []          # Nombres de los ficheros a cargar


for arg in sys.argv:  # Para cada argumento dado al programa

  if arg[0] == '-':     # Si el usuario ha dado un parametro de configuracion:

    if arg[1] == 's':     # Opcion -s: no ignorar espacios
      sinEspacios = 0

    elif arg[1] == 'n':   # Opcion -n: no ignorar saltos de linea
      sinSaltos = 0

    elif arg[1] == 'l':   # Opcion -l: ignorar comentarios de linea
      comentarioLinea = arg[2:]

    elif arg[1] == 'c':   # Opcion -c: ignorar comentarios de bloque
      coma = arg.find(',')
      if coma < 3 or coma == len(arg) - 1:
        sys.exit('! Formato de comentario multilinea incorrecto\n' + manual)
      comentarioBloqA = arg[2:coma]  # El principio esta antes de la coma
      comentarioBloqB = arg[coma+1:] # El final aparece despues de la coma

    else:  # Opcion incorrecta
      sys.exit('! ' + arg + ' no es una opcion valida\n' + manual)

  else:                             # Si no es un parametro, es un fichero.
    nombres.extend(glob.glob(arg))  # Se utiliza 'glob' para procesar comodines


nombres = list(set(nombres))  # Se eliminan los elementos duplicados
ficheros = len(nombres)
if ficheros < 2:              # Si solo se ha dado un fichero, se aborta
  sys.exit('! Se requieren al menos 2 ficheros para realizar comparaciones\n' +\
    manual)
nombres.sort()                # Se ordenan los ficheros por nombre
fichero = [None] * ficheros   # Contenido de los ficheros. Se reserva memoria


for i in range(ficheros):     # Para cada fichero:

  barraCarga('Cargando ficheros', i, ficheros)
  fich = open(nombres[i],'r')
  fichero[i] = fich.read()    # Se guarda todo su contenido en el array
  fich.close()

  if comentarioLinea:  # Si se ha indicado un formato, se eliminan todos
    while 1:           # los comentarios de linea del fichero

      principio = fichero[i].find(comentarioLinea)  # Buscar comienzo
      if principio < 0:
        break
      fin = fichero[i][principio:].find('\n')       # Buscar final

      if fin > 0:      # Se elimina el comentario hasta el final de la linea
        fichero[i] = fichero[i][:principio] + fichero[i][principio + fin:]
      else:            # o hasta el final del fichero
        fichero[i] = fichero[i][:principio]

  if comentarioBloqA:  # Si se ha indicado un formato, se eliminan todos
    while 1:           # los comentarios multilinea del fichero

      principio = fichero[i].find(comentarioBloqA)       # Buscar comienzo
      if principio < 0:
        break
      fin = fichero[i][principio:].find(comentarioBloqB) # Buscar final
      if fin > 0:      # Se elimina el comentario completo
        fichero[i] = fichero[i][:principio] +\
                     fichero[i][principio + fin + len(comentarioBloqB):]
      else:            # Si no se detecta el final del comentario multilinea
        break          # se ignora

  if sinEspacios:      # Eliminar todos los espacios del fichero
    fichero[i] = fichero[i].replace(' ', '')

  if sinSaltos:        # Eliminar todos los saltos de linea del fichero
    fichero[i] = fichero[i].replace('\n', '')


# Cada fichero se comparara con todos los posteriores a el en el array de
# ficheros. Por lo tanto, para N ficheros, cada i-esimo fichero se puede
# comparar con (N-i) ficheros. El numero total de comparaciones a realizar
# es por tanto (N-1) + (N-2) + ... + 3 + 2 + 1 = (N*(N-1))/2
total = ((ficheros * (ficheros - 1)) // 2)
similitud = [None] * total  # Array de similitudes
k = 0                       # Indice del array de similitudes

for i in range(ficheros - 1):  # Para cada fichero, salvo el ultimo
  barraCarga('Comparando ficheros', k, total)

  for j in range(i + 1, ficheros):  # Para cada fichero posterior al i-esimo
    aux = compara(fichero[i], fichero[j])  # Se calcula el grado de similitud
    l = k
    while l > 0:
      if similitud[l - 1][2] < aux:        # El array de similitudes se ordena
        similitud[l] = similitud[l - 1]    # de mayor a menor mientras se
        l -= 1                             # construye
      else:
        break
    similitud[l] = [i, j, aux]  # En el array se almacena los indices de los
    k += 1                      # ficheros y su grado de similitud


# Se muestran los resultados por pantalla
print('| Ficheros | Similitud                    ')
for dif in similitud:
  print('|{0:4d}  {1:<4d}| {2}%'.format(dif[0], dif[1], dif[2]))

print('\nFicheros:')
for i in range(ficheros):
  print('{:<4d}'.format(i) + nombres[i])
