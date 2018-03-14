import csv
VACIA=''
def csv_a_listas(ruta):
	'''Recibe la ruta de un archivo y devuelve una lista con cada una de sus
	
	lineas.
	
	'''
	listaarchivo = []
	with open(ruta) as file:
		for linea in file:
			linea = linea.rstrip('\n')
			linea = linea.split(',')
			listaarchivo.append(linea)
		listaarchivo.pop(0)    
	return listaarchivo
	
def diccionario_informacion_archivo_precios_y_supermercados(listasupermercados, listaprecios):
	'''Recibe como parametro la lista de supermercados y la lista de los
	
	precios de cada producto segun la fecha y el supermercado. Devuelve un 
	
	diccionario con todos los datos de ambas listas (sin tener en cuenta el
	
	nombre de los supermercados, solo su id).
	
	'''
	dicarchsuperyprecios = {}
	for super in listasupermercados:
		dicarchsuperyprecios[str(super[0])] = {}
	for precio in listaprecios:
		for super in dicarchsuperyprecios:
			if precio[0] == super:
				if precio[1] not in dicarchsuperyprecios[super]:
					dicarchsuperyprecios[super][precio[1]] = {precio[2] : precio[3]}
				if precio[2] not in dicarchsuperyprecios[super][precio[1]]: #si es que la fecha no esta
					dicarchsuperyprecios[super][precio[1]][precio[2]] = precio[3]
	return dicarchsuperyprecios
	
def buscar_producto(listaproductos):
	'''Recibe como parametro la lista de productos, le pide al usuario que
	
	ingrese un producto y busca todos los productos que tienen por nombre lo
	
	ingresado por el usuario. De entre ellos le pide cual es el que busca y 
	
	devuelve su id.
	
	'''
	listaidprods, contcoincidencias = peticion_y_validacion_producto(listaproductos)
	prodelegido = validacion_numericidad_y_rango_producto(contcoincidencias)
	idprod = listaidprods[int(prodelegido) - 1]
	return idprod

def peticion_y_validacion_producto(listaproductos):
	'''Recibe como parametro la lista de todos los datos del archivo productos.
	
	Le pide al usuario que ingrese un producto (o una cadena perteneciente
	
	a su nombre), tantas veces como no se encuentre en el archivo, reproduce
	
	todas las coincidencias encontradas, y junta su id en una lista, la cual
	
	es devuelta junto con un contador de la cantidad de elementos(ids de 
	
	productos) que tiene la lista.
	
	'''
	contcoincidencias = 0
	listaidprods = []
	listacaracteres = []
	
	while True:
		prodingresado = input('Ingrese el nombre de un producto existente: ')
		if prodingresado == '' or prodingresado[0] == ' ':
			continue
		prodingresadocapitalizado = prodingresado.capitalize()
		listaidprods, contcoincidencias = buscador_coincidencias_producto(listaproductos,
		prodingresadocapitalizado, contcoincidencias, listaidprods)
		listaidprods, contcoincidencias = buscador_coincidencias_producto(listaproductos,
		prodingresado, contcoincidencias, listaidprods)
		if listaidprods != []:
			break
		print('No se encontro ningun producto con nombre "' +prodingresado+ '"')
	return listaidprods, contcoincidencias
	
def validacion_numericidad_y_rango_producto(contcoincidencias):
	'''Recibe como parametro el contador de todas las coincidencias de
	
	productos encontradas. Le pide al usuario que ingrese el numero que
	
	corresponde al producto que busca. Esto se le pedira indefinidamente
	
	si no ingresa un numero entero que se encuentre entre 1 y el contador.
	
	Devuelve el numero (cadena) ingresado por el usuario.
	
	'''
	while True:
		prodelegido = input('Ingrese el numero correspondiente'+ 
		'al producto buscado: ')
		if (prodelegido.isdigit() and int(prodelegido) > 0 
		and int(prodelegido) <= contcoincidencias):
			break
		if not prodelegido.isdigit():
			print('Debe ingresar un numero.')
		else:
			print('El numero se debe encontrar dentro de los mostrados.')
	return prodelegido
	
def buscador_coincidencias_producto(listaproductos, prodingresado, 
contcoincidencias,listaidprods):
	'''Recibe como parametro la lista de todos los datos incluidos en el
	
	archivo de productos, la cadena ingresada por el usuario (correspondiente
	
	al nombre del producto o parte de el), un contador
	
	encontradas y la lista de ids de productos. Devuelve la lista
	
	de ids de productos con las coincidencias encontradas segun
	
	lo ingresado por el usuario y un contador que cuenta esas 
	
	coincidencias.
	
	'''
	for linea in listaproductos:
		if prodingresado in linea[1]:
			if linea[0] not in listaidprods:
				contcoincidencias += 1
				listaidprods.append(linea[0])
				print(str(contcoincidencias) + '. ' + linea[1])
	return listaidprods, contcoincidencias

def inflacion_por_supermercado(fecha1, fecha2, dicarchsuperyprecios, listasupermercados):
	'''Recibe como parametro una fecha inicial y una fecha inicial (ambas
	
	cadenas con formato <año-mes>), el diccionario de los archivos de precios y
	
	supermercados y la lista de los supermercados. Calcula la inflación de 
	
	precios de cada supermercado en el período indicado y lo muestra en pantalla.
	
	'''
	contadorproductos = 0
	inflaciones = 0
	for super in dicarchsuperyprecios:
		for producto in dicarchsuperyprecios[super]:
			precio1 = dicarchsuperyprecios[super][producto][fecha1]
			precio2 = dicarchsuperyprecios[super][producto][fecha2]
			inflacion = 100 * ((float(precio2) - float(precio1)) / 
			float(precio1))
			contadorproductos += 1
			inflaciones += inflacion
		resultado = inflaciones / contadorproductos
		print()
		print(listasupermercados[int(super) - 1][1], ':', 
		round(resultado, 2), '%')
		
def mejor_precio_para_producto(fecha, dicarchsuperyprecios, listasupermercados,
 listaproductos):
	'''Recibe una fecha en numeros (cadena) con formato <año-mes>, el 
	
	diccionario de los archivos precios y supermercados, la lista de productos 
	
	y la lista de los supermercados. Pide al usuario que ingrese un producto y 
	
	luego imprime en pantalla el supermercado que ofrece el mejor precio para
	
	el producto ingresado junto con el precio.
	
	'''
	idproducto = buscar_producto(listaproductos) #producto es igual al id del producto
	dic = {}
	listaprecios = []
	for super in dicarchsuperyprecios:
		precio = dicarchsuperyprecios[super][idproducto][str(fecha)]
		listaprecios.append(precio)
		dic[precio] = super
	preciominimo = min(listaprecios)
	idsuper = dic[preciominimo]
	super = listasupermercados[int(idsuper) - 1][1]
	print()
	print(super, ': $', preciominimo)
	
def inflacion_general_promedio(fecha1, fecha2, dicarchsuperyprecios):
	'''Recibe como parametro dos fechas en numeros (cadenas) con formato 
	
	<año-mes> y el diccionario de los archivos precios y supermercados. 
	
	Calcula el promedio de la inflación de todos los productos, llamada 
	
	inflacion general, y luego la imprime en pantalla.
	
	'''
	contadorproductos = 0
	inflaciones = 0
	for super in dicarchsuperyprecios:
		for producto in dicarchsuperyprecios[super]:
			precio1 = dicarchsuperyprecios[super][producto][fecha1]
			precio2 = dicarchsuperyprecios[super][producto][fecha2]
			inflacion = 100 * ((float(precio2) - float(precio1)) / 
			float(precio1))
			contadorproductos += 1
			inflaciones += inflacion
	resultado = inflaciones / contadorproductos
	print()
	print('La inflacion general es:', round(resultado,2), '%')
    
def inflacion_por_producto(fecha1, fecha2, dicarchsuperyprecios, 
listasupermercados, listaproductos):
	'''Recibe como parametro dos fechas numericas como cadenas con formato
	
	<año-mes>, el diccionario de los archivos de precios y supermercados, 
	
	la lista de productos y la lista de supermercados. Le pide al 
	
	usuario un producto y calcula la inflacion del mismo en cada supermercado, 
	
	imprimiendola en pantalla.
	
	'''
	producto = buscar_producto(listaproductos)
	for super in dicarchsuperyprecios:
		inflacion = 0
		precio1 = dicarchsuperyprecios[super][producto][fecha1]
		precio2 = dicarchsuperyprecios[super][producto][fecha2]
		inflacion = 100 * ((float(precio2) - float(precio1)) / float(precio1))
		super = listasupermercados[int(super) - 1][1]
		print()
		print('La inflacion de', super, 'es:', round(inflacion, 2),'%')
        
def rango_fechas(listaprecios):
	'''Recibe la lista con las lineas del arhicvo de precios y devuelve las
	
	fechas maxima y minima del rango de fechas que contiene el archivo (para
	
	cada producto se repiten las fechas).
	
	'''
	listafechas = []
	for fecha in listaprecios:
		listafechas.append(fecha[2])
	maxima = max(listafechas)
	minima = min(listafechas)
	return maxima, minima
	
def pedir_fecha(inicialofinal, listaprecios):
	'''Recibe como parametro una cadena (final o inicial) y la lista de precios.
	
	Pide un año y un mes y los devuelve concatenados.
	
	'''
	maxima, minima = rango_fechas(listaprecios)
	while True:
		año = input('Ingrese el año (4 cifras) ' + inicialofinal + ': ')
		if not anio_valido(año):
			print('El año ingresado es invalido')
			continue
		mes = input('Ingrese el mes ' + inicialofinal + ': ')
		if mes_valido(mes):
			if len(mes) == 1:
				mes = '0' + mes
			fecha = año + mes
			if int(fecha) >= int(minima) and int(fecha) <= int(maxima):
				return fecha
			print('La fecha no se encuentra en el archivo')		
			print()
			
def mes_valido(mes):
	'''Recibe como parametro el mes (en numeros) como cadena. Devuelve True
	
	si esta bien escrito, False en caso contrario.
	
	'''
	if mes.isdigit():
		if len(mes) == 2 and int(mes) <= 12:
			return True
		if len(mes) == 1 and mes != '0':
			return True
	return False
	
def anio_valido(año):
	'''Recibe como parametro el año como cadena. Devuelve True si esta bien 
	
	escrito,False en caso contrario.'''
	
	if año.isdigit() and len(año) == 4 and año[0] != '0':
		return True
	return False
	
def fecha_inicial_menor_final(fecha1, fecha2):
	'''Recibe como parametros una fecha inicial y otra final. Devuelve
	
	True si la primera es menor a la segunda, False en caso contrario.
	
	'''
	if int(fecha1) > int(fecha2):
		return False
	return True
	
def mostrar_menu(listasupermercados, listaproductos, listaprecios, dicarchsuperyprecios):
	'''Recibe como parametros la lista de supermercados, la de productos,
	
	la de precios y el diccionario de los archivos precios y supermercados. 
	
	Imprime un menu con 5 opciones, pidiendole al usuario que ingrese una
	
	de las opciones. Segun cual elija se pediran una o dos fechas y se
	
	ejecutara la funcion que cumple lo pedido por el usuario.
	
	'''
	while True:
		print()
		print('Usted se encuentra en el menu principal, ingrese un numero del 1 '
		'al 5 para seleccionar alguna de las siguientes opciones para comenzar: ',
		'1. Inflacion por supermercado', '2. Inflacion por producto', 
		'3. Inflacion general promedio', '4. Mejor precio para un producto', 
		'5. Salir', sep='\n')
		print()
		respuesta = input('Por favor ingrese: ')
		if respuesta == '1' or respuesta == '2' or respuesta == '3':
			while True:
				fecha1 = pedir_fecha('inicial', listaprecios)
				fecha2 = pedir_fecha('final', listaprecios)
				if fecha_inicial_menor_final(fecha1, fecha2):
					break
				print('La fecha inicial debe ser menor que la final')
			if respuesta == '1':
				inflacion_por_supermercado(fecha1, fecha2, dicarchsuperyprecios,
				listasupermercados)
				respuesta = VACIA
			elif respuesta == '2':
				inflacion_por_producto(fecha1, fecha2, dicarchsuperyprecios,
				listasupermercados, listaproductos)
				respuesta = VACIA
			elif respuesta == '3':
				inflacion_general_promedio(fecha1, fecha2, dicarchsuperyprecios)
				respuesta = VACIA
		elif respuesta == '4':
			fecha = pedir_fecha('', listaprecios)
			mejor_precio_para_producto(fecha, dicarchsuperyprecios, 
			listasupermercados, listaproductos)
			respuesta = VACIA
		elif respuesta == '5':
			return
		else:
			respuesta = input('La opcion ingresada no es correcta, ' +
			'vuelva a ingresar una de las opciones ofrecidas')

def main():
	'''Función principal. Esta convierte las lineas de tres archivos (productos, 
	
	precios y supermercados en listas. Crea un diccionario con la informacion 
	
	proveida por el archivo de supermercados y precios (sin tener en cuenta el
	
	nombre de los supermercados) y muestra un menu donde se le pide al usuario
	
	que desea hacer, si calcular la inflacion por supermercado, por producto,
	
	la general, o el mejor precio para un determinado producto. O le permite
	
	salir si es que deseea. Segun lo pedido se ejecutara una determinada funcion
	
	que haga eso (pidiendole al usuario las fechas entre las cuales quiere 
	
	obtener el resultado, excepto en el primer caso que se pide una sola, o
	
	pidiendole que ingrese un producto segun corresponda.
	
	'''
	try:
		listasupermercados = csv_a_listas('supermercados.csv')
		listaproductos = csv_a_listas('productos.csv')
		listaprecios = csv_a_listas('precios.csv')
		dicarchsuperyprecios = diccionario_informacion_archivo_precios_y_supermercados(listasupermercados, 
		listaprecios)
		mostrar_menu(listasupermercados, listaproductos, listaprecios,
		dicarchsuperyprecios)
	except ValueError:
		print('Programa interrumpido: se un ingreso en uno de los archivos un' + 
		'numero donde iria una palabra o viceversa. Por favor revise los' +
		'datos ingresados en el archivo .csv .')
	except ZeroDivisionError:
		print('Programa interrumpido: se ingreso 0 en algun precio del' +
		'archivo de precios.')
	except IOError:
		print('Programa interrumpido: uno de los archivos no se encuentra' +
		'disponible (no existe o ya esta abrierto).')
		
main()