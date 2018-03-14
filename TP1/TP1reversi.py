import string
N = 8
JUGADOR1 = 'N'
JUGADOR2 = 'B'
VACIO = ' '
LISTADIRECCIONES = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (1,1), (-1,1), 
(1,-1)]
LISTALETRAS = list(string.ascii_uppercase)
POSICIONCOLUMNA = 0
JUGADORES = (JUGADOR1, JUGADOR2)
def generar_tablero():
	'''Devuelve un tablero de N filas y N columnas.'''
	tablero = []
	for fil in range(N):
		fila = []
		for col in range(N):
			fila += VACIO
		tablero.append(fila)
	return tablero
	
def campo_del_medio(tablero):
	'''Recibe como parametro el tablero y lo llena con las fichas
	
	iniciales de ambos jugadores.
	
	'''
	tablero[N // 2][N // 2] = JUGADOR2
	tablero[(N//2) - 1][(N//2) - 1] = JUGADOR2
	tablero[(N//2) - 1][(N // 2)] = JUGADOR1
	tablero[N // 2][(N//2) - 1] = JUGADOR1
	return tablero
	
def mostrar_tablero(tablero):
	'''Recibe como parametro el tablero (lista de listas) de dimension NxN y 
	
	lo imprime con los dos tipos de coordenadas.
	
	'''
	cont = 1
	cont2 = 0
	for fila in range(N+1):
		if fila == 0:
			print(VACIO, end=VACIO)
		else:
			print(cont, end='|')
			cont += 1
		for columna in range(N):
			if fila == 0:
				print(string.ascii_uppercase[columna], end=VACIO)
			else:
				print(tablero[cont2][columna], end='|')	
		if fila != 0:
			cont2 += 1
		print()
	print()
	
def peticion_jugada(jugadoractual):
	'''Recibe como parametro el simbolo del jugador (cadena) y le pide
	
	las coordenadas donde ingresar la ficha.
	
	'''
	while True:
		jugada = input('Jugador '+jugadoractual+' ingrese una coordenada donde pueda capturar fichas '+
		'<primero la columna y luego la fila, sin espacios> : ')
		validacion = validacion_jugada(jugada)
		
		if validacion == True:
			return jugada
		print('La coordenada esta mal ingresada')
		
def posiciones_en_tablero_de_jugada(jugada):
	'''Recibe como parametro la jugada (columna y fila) ingresada por 
	
	el usuario,devuelve sus posiciones en el tablero.
	
	'''
	coordenadas = jugada
	coordenadas = coordenadas.upper()
	listacoordenadas = []
	
	for posiciones in coordenadas:
		listacoordenadas.append(posiciones)
	coordenadacolumna = listacoordenadas.pop(POSICIONCOLUMNA)
	coordenadafila = int(''.join(listacoordenadas))
	return coordenadafila, coordenadacolumna
	
def validacion_jugada(jugada):
	'''Recibe la jugada ingresada por el usuario. En caso de ser correctas
	
	sus coordenadas, devuelve True, en caso contrario, False.
	
	'''
	coordenadasfila = ''
	coordenadacolumna = jugada[POSICIONCOLUMNA]
	coordenadafila = 0
	for coordenadas in jugada:
		if coordenadacolumna.isalpha():
			coordenadacolumna = coordenadacolumna.upper()
			if coordenadas.isdigit():
				coordenadasfila += coordenadas
				if len(coordenadasfila) == len(jugada) - 1:
					coordenadafila = int(coordenadasfila)
	return (coordenadafila >= 1 and coordenadafila <= N and 
	coordenadacolumna in LISTALETRAS[:N])
	
def limite_tablero_excedido(x, y):
	'''Recibe dos coordenadas x, y. Devuelve True si estan fuera
	
	del rango del tablero. False en caso contrario.
	
	'''
	return x >= N or x < 0 or y >= N or y < 0
	

def revisar_direcciones(tablero, jugadoractual, oponente, coordenadafila, coordenadacolumna):
	'''Recibe como parametro una lista de listas (tablero), dos cadenas 
	
	(el jugador actual y su oponente) y dos numeros enteros (las posiciones 
	
	de la coordenada de la jugada ingresada por el usuario en juego). Recorre 
	
	todas las direcciones posibles desde la coordenada y devuelve una lista de

	las coordenadas donde se puede capturar fichas junto con la direccion por 
	
	donde estan esas fichas.
	
	'''
	listacapturas = []
	
	for dx,dy in LISTADIRECCIONES:
		x = coordenadafila - 1
		y = LISTALETRAS.index(coordenadacolumna)
		x += dx
		y += dy
		while True:
			contador = 0
			if limite_tablero_excedido(x, y):
				break
			while tablero[x][y] == oponente:
				x += dx
				y += dy
				contador += 1
				if limite_tablero_excedido(x, y):
					break
				if tablero[x][y] == jugadoractual:
					for captura in range(1, contador+1):
						listacapturas.append((x - dx*captura, y - dy*captura, dx, dy))
						listacapturas += listacapturas
			else:
				break
	return listacapturas
	
def reemplazar_coordenadas(tablero, jugadoractual, oponente, coordenadafila, coordenadacolumna):
	'''Recibe los mismos parametros que la fucion revisar_coordenadas, 
	
	devuelve el nuevo tablero con las fichas reemplazadas.
	
	'''
	listacapturas = revisar_direcciones(tablero, jugadoractual, oponente, coordenadafila, coordenadacolumna)
	for coordenadasareemplazar in listacapturas:
		x, y, dx, dy = coordenadasareemplazar
		x += dx
		y += dy
		while tablero[x - dx][y - dy] == oponente:
			tablero[x - dx][y - dy] = jugadoractual
			x -= dx
			y -= dy
		tablero[coordenadafila - 1][LISTALETRAS.index(coordenadacolumna)] = jugadoractual
	return tablero

def posibilidad_de_jugar(tablero, jugadoractual, oponente):
	'''Recibe como parametros una lista de listas (tablero) y dos cadenas
	
	(jugador y oponente), devuelve True en caso de que el jugador tenga
	
	jugadas posibles, False en caso contrario.
	
	'''
	for fila in range(1, N+1) :
		for columna in range(N):
			fila = str(fila)
			columna = LISTALETRAS[columna]
			jugada = columna + fila
			coordenadafila, coordenadacolumna = posiciones_en_tablero_de_jugada(jugada)
			if tablero[coordenadafila - 1][LISTALETRAS.index(coordenadacolumna)] == VACIO:
				listacapturas = revisar_direcciones(tablero, jugadoractual, 
				oponente, coordenadafila, coordenadacolumna)
				if listacapturas != []:
					return True
	return False
	
def paso_de_turnos(turnos):
	'''Recibe un numero entero turnos y devuelve dos cadenas, asignandoles
	
	el nombre que les corresponda.
	
	'''
	jugadoractual = JUGADORES[turnos % 2]
	oponente = JUGADORES[(turnos+1) % 2]
	return jugadoractual, oponente
	
def contar_fichas_en_tablero(tablero):
	'''Recibe por parametro una lista de listas (tablero). Recorre el tablero,

	cuenta las cantidad de fichas blancas y negras que hay en el y las
	
	devuelve.
	
	'''
	ocupadopornegras = 0
	ocupadoporblancas = 0
	for fila in tablero:
		for columna in fila:
			if columna == JUGADOR1:
				ocupadopornegras += 1
			elif columna == JUGADOR2:
				ocupadoporblancas += 1
	return ocupadopornegras, ocupadoporblancas
	
def ganador(ocupadopornegras, ocupadoporblancas):
	'''Decide quien ha ganado (o si hay empate) y lo imprime en pantalla.'''
	if ocupadopornegras > ocupadoporblancas:
		print('¡Han ganado las negras!')
	elif ocupadopornegras < ocupadoporblancas:
		print('¡Han ganado las blancas!')
	else:
		print('¡Ha sido un empate!')
		
def jugar_de_vuelta():
	'''Pregunta al usuario si desea jugar nuevamente. Devuelve False en caso
	
	de ser NO la respuesta, True si es SI.
	
	'''
	while True:
		repetirreversi = input('¿Desea jugar de nuevo? Ingrese SI o NO : ')
		repetirreversi = repetirreversi.upper()
		if repetirreversi == 'NO':
			return False
		elif repetirreversi == 'SI':
			return True
	
def main():
	'''	Reproduce el juego Reversi: imprime un tablero con las fichas inciales, 
	
	y les pide a cada jugador las coordenadas donde quieren poner sus fichas, 
	
	uno por vez, pasando de turnos adecuadamente. En caso de ingresar mal la 
	
	coordenada se le pide de vuelta y si no tiene jugadas validas se pasa el
	
	turno. Cuando ya los dos no pueden jugar la funcion cuenta las fichas de
	
	cada uno e imprime quien es el ganador o si hay empate. Luego se le 
	
	pregunta al usuario si quiere jugar nuevamente. En caso de ser SI la 
	
	respuesta, el juego vuelve a funcionar.
	
	'''

	print()
	print('!Bienvenido al reversi!')
	print()
	
	while True:
		tablero = generar_tablero()
		tablero = campo_del_medio(tablero)
		mostrar_tablero(tablero)
		turnos = 0
		sinposibilidades = 0
	
		while sinposibilidades < 2:
			jugadoractual, oponente = paso_de_turnos(turnos)
			if posibilidad_de_jugar(tablero, jugadoractual, oponente) == False:
				sinposibilidades += 1
				continue
			posibilidadjugar = 0
			listacapturas = []
			while listacapturas == []:
				jugada = peticion_jugada(jugadoractual)
				coordenadafila, coordenadacolumna = posiciones_en_tablero_de_jugada(jugada)
				if (tablero[coordenadafila - 1][LISTALETRAS.index(coordenadacolumna)] == JUGADOR1 
				or tablero[coordenadafila - 1][LISTALETRAS.index(coordenadacolumna)] == JUGADOR2):
					continue
				listacapturas = revisar_direcciones(tablero, jugadoractual, 
				oponente, coordenadafila, coordenadacolumna)
			tablero = reemplazar_coordenadas(tablero, jugadoractual, oponente, coordenadafila, coordenadacolumna)
			mostrar_tablero(tablero)
			turnos += 1
		print('El juego ha finalizado')
		ocupadopornegras, ocupadoporblancas = contar_fichas_en_tablero(tablero)
		ganador(ocupadopornegras, ocupadoporblancas)
		repeticionjuego = jugar_de_vuelta()
		if repeticionjuego == False:
			break
		
main()