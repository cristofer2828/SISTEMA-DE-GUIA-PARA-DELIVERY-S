import random
import time
from collections import deque

# Generar mapa 
def generar_mapa(tam_x, tam_y, ubic_sede):
    num_obstaculos = (tam_x * tam_y) // 5  # Más obstáculos en matrices grandes
    mapa = [['.' for _ in range(tam_x)] for _ in range(tam_y)]
    obstaculos = [
        (random.randint(1, tam_x), random.randint(1, tam_y))
        for _ in range(num_obstaculos)
    ]
    for x, y in obstaculos:
        if (x, y) != tuple(ubic_sede):  # Evitar colocar obstáculos en la sede
            mapa[tam_y - y][x - 1] = 'X'
    return mapa

# Generarción del repartidor cerca de la sede
def posicion_repartidor(ubic_sede, tam_x, tam_y):
    x_s, y_s = ubic_sede
    posibles = [
        (x_s + dx, y_s + dy)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 1 <= x_s + dx <= tam_x and 1 <= y_s + dy <= tam_y
    ]
    return random.choice(posibles)

# Dibujar mapa
def dibujar_mapa(mapa, ubic_repartidor=None, ubic_cliente=None, recorrido=None):
    mapa_dibujado = [fila[:] for fila in mapa]
    tam_y = len(mapa_dibujado)
    if recorrido:
        for x, y in recorrido:
            mapa_dibujado[tam_y - y][x - 1] = 'O'
    if ubic_repartidor:
        x_r, y_r = ubic_repartidor
        mapa_dibujado[tam_y - y_r][x_r - 1] = 'R'
    if ubic_cliente:
        x_c, y_c = ubic_cliente
        mapa_dibujado[tam_y - y_c][x_c - 1] = 'C'
    print("\nMapa actual:")
    for fila in mapa_dibujado:
        print(" ".join(fila))

# Calcular ruta más corta
def calcular_ruta(mapa, inicio, destino):
    tam_x, tam_y = len(mapa[0]), len(mapa)
    cola = deque([(inicio, [])])
    visitados = set()
    while cola:
        (x, y), camino = cola.popleft()
        if (x, y) == destino:
            return camino + [(x, y)]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= tam_x and 1 <= ny <= tam_y and (nx, ny) not in visitados:
                if mapa[tam_y - ny][nx - 1] != 'X':
                    visitados.add((nx, ny))
                    cola.append(((nx, ny), camino + [(x, y)]))
    return []

# Mostrar productos disponibles
def mostrar_productos_disponibles():
    productos = {
        1: ("Laptop", 3000),
        2: ("Smartphone", 1500),
        3: ("Cargador portátil", 100),
        4: ("Auriculares", 200),
        5: ("Reloj inteligente", 800),
    }
    print("\n|--- Productos disponibles ---|")
    for k, (nombre, precio) in productos.items():
        print(f"{k}. {nombre} - S/. {precio}")
    print("|-----------------------------|")
    return productos

# Agregar productos al carrito
def agregar_producto_al_carrito(productos, carrito):
    mostrar_productos_disponibles()
    try:
        opcion = int(input("Selecciona el número del producto para agregar al carrito: "))
        if opcion in productos:
            carrito.append(productos[opcion])
            print(f"{productos[opcion][0]} agregado al carrito.")
        else:
            print("Producto no válido.")
    except ValueError:
        print("Entrada inválida. Ingresa un número.")

# Obtener ubicación del cliente
def obtener_ubicacion_cliente(tam_x, tam_y):
    while True:
        try:
            x = int(input(f"Ingrese su ubicación X (1-{tam_x}): "))
            y = int(input(f"Ingrese su ubicación Y (1-{tam_y}): "))
            if 1 <= x <= tam_x and 1 <= y <= tam_y:
                return (x, y)
            else:
                print(f"Por favor, ingrese valores dentro del rango (1-{tam_x}, 1-{tam_y}).")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese números válidos.")

# Procesar compra
def procesar_compra(carrito, ruta):
    costo_productos = sum(producto[1] for producto in carrito)
    costo_delivery = len(ruta) - 1
    total = costo_productos + costo_delivery
    print("\n|--- Resumen de la compra ---|")
    print("Productos:")
    for producto, precio in carrito:
        print(f" - {producto}: S/. {precio}")
    print(f"Delivery: S/. {costo_delivery}")
    print(f"Total a pagar: S/. {total}")
    print("|----------------------------|")

# Cambiar de sede
def cambiar_sede():
    sedes = {
        "San Carlos": (10, 10, [8, 9]),
        "Abancay": (30, 30, [24, 30]),
        "Santa Rosa": (25, 25, [7, 21]),
        "Gamarra": (20, 20, [10, 20]),
        "Mariátegui": (15, 15, [12, 14]),
    }
    print("\n|--- Sedes disponibles ---|")
    for i, sede in enumerate(sedes.keys(), start=1):
        print(f"{i}. {sede}")
    print("|-------------------------|")
    try:
        opcion = int(input("Selecciona la sede a la que deseas cambiar: "))
        if 1 <= opcion <= len(sedes):
            sede = list(sedes.keys())[opcion - 1]
            return sede, sedes[sede]
        else:
            print("Opción no válida.")
    except ValueError:
        print("Entrada inválida.")
    return None, None

# Mostrar interfaz principal
def mostrar_interfaz_principal(carrito, sede_actual, ubic_repartidor):
    print("\n|--- Almacenes ApplesIncopx ---|")
    print(f"1. Productos en el carrito actuales: {len(carrito)}")
    print("2. Cambiar de sede")
    print("3. Ver mapa")
    print(f"   Sede actual: \"{sede_actual}\", Ubicación repartidor {ubic_repartidor}")
    print("4. Proceder a comprar")
    print("5. Salir")
    print("|---------------------------|")

# Main de ejecución
def main():
    carrito = []
    productos = mostrar_productos_disponibles()
    sede_actual, (tam_x, tam_y, ubic_sede) = "San Carlos", (10, 10, [8, 9])
    mapa = generar_mapa(tam_x, tam_y, ubic_sede)
    ubic_repartidor = posicion_repartidor(ubic_sede, tam_x, tam_y)

    while True:
        mostrar_interfaz_principal(carrito, sede_actual, ubic_repartidor)
        try:
            opcion = int(input("Selecciona una opción: "))
            if opcion == 1:
                agregar_producto_al_carrito(productos, carrito)
            elif opcion == 2:
                nueva_sede, datos_sede = cambiar_sede()
                if nueva_sede:
                    sede_actual, (tam_x, tam_y, ubic_sede) = nueva_sede, datos_sede
                    mapa = generar_mapa(tam_x, tam_y, ubic_sede)
                    ubic_repartidor = posicion_repartidor(ubic_sede, tam_x, tam_y)
            elif opcion == 3:
                dibujar_mapa(mapa, ubic_repartidor=ubic_repartidor)
            elif opcion == 4:
                if not carrito:
                    print("El carrito está vacío. Agrega productos primero.")
                else:
                    ubic_cliente = obtener_ubicacion_cliente(tam_x, tam_y)
                    ruta = calcular_ruta(mapa, tuple(ubic_repartidor), ubic_cliente)
                    if ruta:
                        print("\nSimulando recorrido del repartidor:")
                        for paso in ruta:
                            time.sleep(0.4)
                            dibujar_mapa(mapa, paso, ubic_cliente, ruta[:ruta.index(paso) + 1])
                        procesar_compra(carrito, ruta)
                        return
                    else:
                        print("No se encontró una ruta válida.")
            elif opcion == 5:
                print("Gracias por visitar Almacenes ApplesIncopx. ¡Hasta pronto!")
                return
            else:
                print("Opción no válida.")
        except ValueError:
            print("Entrada inválida.")
#Terminar
main()
