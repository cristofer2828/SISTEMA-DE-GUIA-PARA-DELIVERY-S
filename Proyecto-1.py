# Función para dibujar el mapa cartesiano básico en consola
def dibujar_mapa(ubicaciones, repartidor_pos=None):
    # Definir tamaño del mapa (un plano de 10x10 para simular un mapa cartesiano)
    max_x = 10
    max_y = 10
    
    # Crear una cuadrícula vacía de 10x10
    mapa = [['.' for _ in range(max_x)] for _ in range(max_y)]
    
    # Colocar el repartidor en el mapa
    if repartidor_pos:
        x, y = repartidor_pos
        mapa[max_y - y - 1][x] = 'R'
    
    # Colocar las ubicaciones de los clientes en el mapa
    for nombre, (x, y) in ubicaciones.items():
        if nombre != "Repartidor":  # No poner un cliente sobre el repartidor
            if 0 <= x < max_x and 0 <= y < max_y:
                mapa[max_y - y - 1][x] = 'C'  # Usamos 'C' para los clientes
    
    # Dibujar el mapa
    print("\nMapa de ubicaciones (R = Repartidor, C = Cliente):")
    for fila in mapa:
        print(" ".join(fila))
    print("\nEl sistema está listo para ingresar las ubicaciones de los clientes.")

# Función para calcular la distancia euclidiana entre dos puntos en metros
def calcular_distancia(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

# Función para obtener la ruta más corta usando un algoritmo simple de "cercanía"
def obtener_ruta_optima(ubicaciones):
    ruta = ["Repartidor"]
    puntos_restantes = list(ubicaciones.keys())[1:]  # Excluye "Repartidor"
    ubicacion_actual = "Repartidor"
    
    while puntos_restantes:
        siguiente_cliente = min(puntos_restantes, key=lambda x: calcular_distancia(ubicaciones[ubicacion_actual], ubicaciones[x]))
        ruta.append(siguiente_cliente)
        puntos_restantes.remove(siguiente_cliente)
        ubicacion_actual = siguiente_cliente

    return ruta

# Función para mostrar la ruta en la consola
def mostrar_ruta(ruta, ubicaciones):
    print("Ruta de entrega óptima:")
    print(" -> ".join(ruta))
    print("\nDetalles de las distancias (en metros):")
    
    distancia_total = 0
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i + 1]
        distancia = calcular_distancia(ubicaciones[origen], ubicaciones[destino])
        distancia_total += distancia
        print(f"De {origen} a {destino}: {distancia:.2f} metros")
    
    print(f"\nDistancia total de la ruta: {distancia_total:.2f} metros")

# Función para ingresar las ubicaciones de los clientes
def ingresar_ubicaciones():
    ubicaciones = {}
    repartidor_x = int(input("Ingresa la coordenada X del Repartidor: "))
    repartidor_y = int(input("Ingresa la coordenada Y del Repartidor: "))
    ubicaciones["Repartidor"] = (repartidor_x, repartidor_y)
    
    # Ingresar clientes
    num_clientes = int(input("¿Cuántos clientes deseas agregar?: "))
    
    for i in range(1, num_clientes + 1):
        nombre_cliente = f"Cliente {i}"
        print(f"\nIngresando ubicaciones para {nombre_cliente}:")
        cliente_x = int(input(f"  Ingresa la coordenada X de {nombre_cliente}: "))
        cliente_y = int(input(f"  Ingresa la coordenada Y de {nombre_cliente}: "))
        ubicaciones[nombre_cliente] = (cliente_x, cliente_y)
    
    return ubicaciones

# Función principal
def main():
    # Ingresar ubicaciones de los clientes
    ubicaciones = ingresar_ubicaciones()

    # Mostrar el mapa de ubicaciones inicial
    dibujar_mapa(ubicaciones, repartidor_pos=ubicaciones["Repartidor"])

    # Obtener la ruta óptima
    ruta_optima = obtener_ruta_optima(ubicaciones)

    # Mostrar la ruta y las distancias
    mostrar_ruta(ruta_optima, ubicaciones)

    # Mostrar la ruta del repartidor en el mapa
    print("\nSimulación de la ruta del repartidor:")
    posicion_repartidor = ubicaciones["Repartidor"]
    for paso in ruta_optima[1:]:  # Excluye el repartidor de la ruta inicial
        print(f"Repartidor se mueve de {posicion_repartidor} a {ubicaciones[paso]}")
        dibujar_mapa(ubicaciones, repartidor_pos=ubicaciones[paso])
        posicion_repartidor = ubicaciones[paso]  # Actualizar la posición del repartidor

# Ejecutar el programa
main()
