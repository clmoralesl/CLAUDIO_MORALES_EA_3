print ('Bienvenido a eventos “Sanchez Producciones”')
lista_asientos = []
lista_ventas= []
from datetime import date
fecha_actual = date.today()
diccionario_ventas = {} #Se inicia un diccionario que guardará los ruts y las ventas
def crear_matriz():
    for numeros in range(1,51):
        lista_asientos.append(numeros)
def mostrar_menu():
    print('''
-------------Menú-------------
1) Comprar entradas
2) Mostrar ubicaciones disponibles
3) Ver listado de asistentes
4) Mostrar ganancias totales
5) Salir
''')
def imprimir_asientos():
    print('\t\t|ASIENTOS DISPONIBLES|\t\t\t\t|CATEGORIA Y PRECIOS|')
    preciovip = '|Asientos Vip\t    $100.000|'
    precionormal = '|Asientos normales\t     $50.000|'
    preciobarato = '|Asientos económicos     $10.000|'
    for filas in range(0,50,10):
        print('')
        for indice in range(10):
            if len(str(lista_asientos[indice+filas]))<2:
                print(f'-[0{lista_asientos[indice+filas]}]-', end="")
            else:
                print(f'-[{lista_asientos[indice+filas]}]-', end="")
        print(preciovip if filas <20 else precionormal if filas==20 else preciobarato, end='')
    print('')
def menu_compra():
    if verificar_disponibilidad() == False: # Cada vez que se ingresa al menú de compra verifica primero que existan asientos disponibles
        print ('Lamentablemente no quedan entradas disponibles')
        return# Si no existen asientos disponibles sale de la función mediante un 'return'
    while True:
        try:
            rut=input('Ingrese su rut, sin puntos ni guión verificador:\n')
            if verificar_rut(rut) == False: #Se ocupa una función para verificar que no se ingrese un rut repetido
                continue
            if len(rut) < 7 or len(rut)>8:
                print('Rut inválido, vuelva a ingresar (El rut debe tener entre 7 y 8 numeros.Ejemplo: 12.345.678-9, debe ser 12345678)')
                continue
            num_entradas=int(input('Cuantas entradas desea comprar?(Maximo 2):\n'))
            while num_entradas < 1 or num_entradas > 2:
                print('Ingrese un monto válido')
                num_entradas=int(input('Cuantas entradas desea comprar?(Maximo 2):\n'))
            comprar_entradas(num_entradas,rut)
            break
        except ValueError:
            print('Error de dato, vuelva a intentar')
def comprar_entradas(entradas,rut):
    lista_numeros_asientos = []#Lista temporal para guardar los numeros de asientos asociados al rut
    precio_total=0 #Se define una variable para guardar el precio total de compra
    asientos_copia = lista_asientos[:] # Se genera una copia superficial de los datos de la lista, en caso que la compra no se concrete
    for entradas in range(entradas): #Se genera un bucle según la cantidad de entradas que se adesea comprar
        encontrado = False #Variable que define si existe el asiento seleccionado
        while encontrado == False: #Mientras no se seleccione un asiento válido no se saldrá del ciclo
            imprimir_asientos()
            try:
                asiento = int(input('Seleccione un asiento:\n'))
                if asiento <1 or asiento>50:
                    print('Seleccione un asiento válido')
                    continue#Si selecciona un asiento fuera del rango reinicia el bucle
            except ValueError:
                print('Error de dato, vuelva a intentar')
                continue
            for numeros in range(len(lista_asientos)):
                if asiento == lista_asientos[numeros-1]:#Se revisa toda la lista con asientos para comprobar si el asiento sigue disponible
                    precio_asiento = verificar_precio(asiento)#Se invoca la variable para comprobar el precio del asiento
                    print (f'Ha seleccionado el asiento número {asiento} por un precio de ${precio_asiento}')
                    precio_total+=precio_asiento # Se suma el precio individaual del asiento a la variable precio total
                    lista_asientos[numeros-1] = 'XX'
                    verificar_disponibilidad()
                    encontrado = True
                    lista_numeros_asientos.append(asiento) # Se modifica la variable para salir del while y seguir al siguiente ciclo for, si es que corresponde
            if encontrado == False:
                print('Asiento no disponible, vuelva a intentar')
        if verificar_disponibilidad() == False:
            print('Lamentablemente no quedan más entradas disponibles')
            break
    if aceptar_total(precio_total)==True:
        lista_ventas.append(precio_total)#Se guarda una lista el precio de la venta realizada 
        diccionario_ventas [rut] = (lista_numeros_asientos)  # Si la venta es exitosa se agrega el rut y los asientos a un diccionario
        print ('Volviendo al menú principal')
    else:
        for indices in range(len(lista_asientos)): #Si no se realiza la compra se copia nuevamente cada elemento de la copia de la lista guardada al principio
            lista_asientos [indices] = asientos_copia [indices]
        print('Volviendo al menú principal')
def aceptar_total(precio): #Función que se encarga de validar con el usuario el pago de la compra
    print(f'El total de su compra es de ${precio}')
    aceptar=''
    while aceptar=='':
        aceptar=input('Desea realizar el pago?(Si/No)\n').lower()
        if aceptar == 'si':
            print('Pago exitoso')
            return True
        elif aceptar == 'no':
            print('Compra cancelada')
            return False   
        else:
            print('Opción inválida')
            aceptar_total(precio)
def verificar_precio(asiento):#Función para definir el precio dependiendo del número de asiento
    if asiento <=20:
        return 100000
    elif asiento <=30:
        return 50000
    else:
        return 10000
def verificar_disponibilidad(): #Mediante un ciclo for se cuentan los asientos ocupados ('XX') y si los 50 están ocupados retorna False
    contador = 0
    for asientos in lista_asientos:
        if asientos == 'XX': 
            contador +=1
    if contador == 50:
        return False
    else:
        return True
def mostrar_ruts():#Esta función itera sobre el diccionario de ruts para mostrar su n° de rut y el número de asiento
    print('Los asistentes registrados hasta el momento son los siguientes:')
    contador_llaves = 1
    for llaves, elementos in diccionario_ventas.items():
        print (f'{contador_llaves}.RUT N°: {llaves} con asiento(s) numero(s) {elementos}')
        contador_llaves +=1
def monto_total():# Se itera sobre la lista que guarda las ventas para encontrar el monto total de ventas
    monto_total_ventas = 0
    for ventas in lista_ventas:
        monto_total_ventas += ventas
    print(f'El monto total de ganancias registradas hasta el momento es de :\n${monto_total_ventas}')
def verificar_rut(rut): #Función que itera sobre el diccionario para verificar que no se repita el mismo rut
    for llaves in diccionario_ventas.keys():
        if llaves == rut:
            print('Este rut ya ha realizado una compra, intente nuevamente')
            return False
    return True
crear_matriz()# Inicio de programa 
imprimir_asientos()
while True:
    mostrar_menu()
    try:
        opc_menu=int(input('Selecccione una opción:\n'))
        if opc_menu<1 or opc_menu>6:
            print('Opción inválida, ingrese nuevamente')
            continue
    except ValueError:
        print('Error de dato, ingrese nuevamente')
        continue
    match opc_menu:
        case 1:
            menu_compra()
        case 2:
            imprimir_asientos()
        case 3:
            mostrar_ruts() 
        case 4:
            monto_total()
        case 5:
            print ('Gracias por operar con eventos “Sanchez Producciones”')
            print (f'Saliendo del sistema \nClaudio Morales {fecha_actual}')
            break
            
            



            