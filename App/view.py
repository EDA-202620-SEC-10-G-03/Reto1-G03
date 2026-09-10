import sys
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
import os
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sll 
# Asegura la resolución de rutas de importación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tabulate import tabulate
import logic

default_limit = 1000
sys.setrecursionlimit(default_limit * 10)

headers = ["Order_ID", "Product", "Country", "Channel", "Order_Date", "Price_per_Box", "Amount"]


def print_order_row(order):
    if not order:
        return []
    return [
        order.get('Order_ID'),
        order.get('Product'),
        order.get('Country'),
        order.get('Channel'),
        order.get('Order_Date'),
        order.get('Price_per_Box'),
        order.get('Amount')
    ]


def new_logic():
    """
    Se crea una instancia del controlador
    """
    return logic.new_logic()


def print_menu():
    print("\nBienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")


def load_data(control):
    """
    Carga los datos
    """
    filename = input("Ingrese el nombre del archivo en data/ (ej. chocolate_sale_100_elementos.csv): ").strip()
    path = f"Data/{filename}"
    res = logic.load_data(control, path)

    print(f"\nTiempo de carga: {res['elapsed_time_ms']:.2f} ms")
    print(f"Total de pedidos cargados: {res['total_orders']}")

    print("\nPedido de MENOR precio total (Amount):")
    if res['min_amount_order']:
        print(tabulate([print_order_row(res['min_amount_order'])], headers=headers, tablefmt="grid"))

    print("\nPedido de MAYOR precio total (Amount):")
    if res['max_amount_order']:
        print(tabulate([print_order_row(res['max_amount_order'])], headers=headers, tablefmt="grid"))

    print("\nPrimeros 5 registros:")
    print(tabulate([print_order_row(o) for o in res['first_5']], headers=headers, tablefmt="grid"))

    print("\nÚltimos 5 registros:")
    print(tabulate([print_order_row(o) for o in res['last_5']], headers=headers, tablefmt="grid"))


def print_data(control, id):
    """
    Función que imprime un dato dado su ID
    """
    orders = control['orders']
    sz = lt.size(orders)
    found = None

    for i in range(0, sz):
        elem = lt.get_element(orders, i)
        if str(elem.get('Order_ID')).strip() == str(id).strip():
            found = elem
            break

    if found:
        print(tabulate([print_order_row(found)], headers=headers, tablefmt="grid"))
    else:
        print(f"No se encontró el registro con Order_ID: {id}")


def print_req_1(control):
    """
    Función que imprime la solución del Requerimiento 1 en consola
    """
    product = input("Nombre del producto (ej. 70% Dark Bar): ").strip()
    res = logic.req_1(control, product)
    print(f"\nTiempo de ejecución: {res['elapsed_time_ms']:.2f} ms")
    print(f"Total pedidos: {res['total_count']}")
    if res['total_count'] > 0:
        print(f"Price_per_Box -> Prom: {res['avg_price']:.2f}, Min: {res['min_price']}, Max: {res['max_price']}")
        print(f"Discount_Pct  -> Prom: {res['avg_discount']:.2f}, Min: {res['min_discount']}, Max: {res['max_discount']}")
        print(f"Boxes_Shipped -> Prom: {res['avg_boxes']:.2f}, Min: {res['min_boxes']}, Max: {res['max_boxes']}")
        print(f"Marketing_Sp  -> Prom: {res['avg_spend']:.2f}, Min: {res['min_spend']}, Max: {res['max_spend']}")
        print(f"Año con más pedidos: {res['top_year']}")

        print("\nPedido de MAYOR Amount:")
        print(tabulate([print_order_row(res['max_amt_order'])], headers=headers, tablefmt="grid"))

        print("\nPedido de MENOR Amount:")
        print(tabulate([print_order_row(res['min_amt_order'])], headers=headers, tablefmt="grid"))


def print_req_2(control):
    """
    Función que imprime la solución del Requerimiento 2 en consola
    """
    p_min = float(input("Precio mínimo por caja: "))
    p_max = float(input("Precio máximo por caja: "))
    res = logic.req_2(control, p_min, p_max)
    print(f"\nTiempo de ejecución: {res['elapsed_time_ms']:.2f} ms")
    print(f"Cantidad de pedidos: {res['total_count']}")
    if res['total_count'] > 0:
        print(f"Promedio Discount_Pct: {res['avg_discount']:.2f}")
        print(f"Promedio Marketing_Spend: {res['avg_spend']:.2f}")
        print(f"Promedio Price_per_Box: {res['avg_price']:.2f}")

        print("\nPedido más reciente:")
        print(tabulate([print_order_row(res['most_recent'])], headers=headers, tablefmt="grid"))

        print("\nPedido de MENOR Amount:")
        print(tabulate([print_order_row(res['min_amt'])], headers=headers, tablefmt="grid"))

        print("\nPedido de MAYOR Amount:")
        print(tabulate([print_order_row(res['max_amt'])], headers=headers, tablefmt="grid"))


def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    country = input("País: ").strip()
    channel = input("Canal (Retail/Online/Wholesale): ").strip()
    res = logic.req_3(control, country, channel)
    print(f"\nTiempo de ejecución: {res['elapsed_time_ms']:.2f} ms")
    print(f"Total de pedidos: {res['total_count']}")
    if res['total_count'] > 0:
        print(f"Promedio Price_per_Box: {res['avg_price']:.2f}")
        print(f"Promedio Discount_Pct: {res['avg_discount']:.2f}")
        print(f"Promedio Marketing_Spend: {res['avg_spend']:.2f}")
        print(f"Promedio Boxes_Shipped: {res['avg_boxes']:.2f}")
        print(f"Producto más frecuente: {res['most_freq_product']}")
        print(f"Año con más pedidos: {res['top_year']}")


def print_req_4(control):
    """
    Función que imprime la solución del Requerimiento 4 en consola
    """
    product = input("Producto: ").strip()
    country = input("País: ").strip()
    
    res = logic.req_4(control, product, country)
    
    print(f"\nTiempo de ejecución: {res['elapsed_time_ms']:.2f} ms")
    print(f"Total de pedidos: {res['total_count']}")
    
    if res['total_count'] > 0:
        print(f"Promedio Price_per_Box: {res['avg_price']:.2f}")
        print(f"Promedio Discount_Pct: {res['avg_discount']:.2f}")
        print(f"Promedio Marketing_Spend: {res['avg_spend']:.2f}")
        print(f"Promedio Boxes_Shipped: {res['avg_boxes']:.2f}")

        print("\nTop 2 de mayor Amount:")
        top2_headers = ["Order_ID", "Channel", "Order_Date", "Boxes_Shipped", "Amount"]
        
        # Extraer filas iterando según la API de SLL
        rows = []
        top_list = res.get('top_2')
        if top_list is not None:
            for i in range(sll.size(top_list)):
                o = sll.get_element(top_list, i)
                rows.append([
                    o.get('Order_ID'),
                    o.get('Channel'),
                    o.get('Order_Date'),
                    o.get('Boxes_Shipped'),
                    o.get('Amount')
                ])
                
        print(tabulate(rows, headers=top2_headers, tablefmt="grid"))


def print_req_5(control):
    """
    Función que imprime la solución del Requerimiento 5 en consola
    """
    ftype = input("Filtro (MENOR / MAYOR): ").strip()
    product = input("Producto: ").strip()
    start_d = input("Fecha inicial (AAAA-MM-DD): ").strip()
    end_d = input("Fecha final (AAAA-MM-DD): ").strip()
    res = logic.req_5(control, ftype, product, start_d, end_d)
    print(f"\nTiempo de ejecución: {res['elapsed_time_ms']:.2f} ms")
    print(f"Filtro: {res.get('filter_type')}")
    print(f"Total de pedidos: {res['total_count']}")
    if res['total_count'] > 0:
        o = res['selected_order']
        print(f"\nPedido Resultante ({res['filter_type']}):")
        print(f"Price_per_Box: {o['Price_per_Box']}, Boxes_Shipped: {o['Boxes_Shipped']}, Amount: {o['Amount']}")
        print(f"Channel: {o['Channel']}, Order_Date: {o['Order_Date']}, Marketing_Spend: {o['Marketing_Spend']}")

        print("\nPromedio del grupo:")
        print(f"Price_per_Box: {res['avg_price']:.2f}, Boxes_Shipped: {res['avg_boxes']:.2f}, Marketing_Spend: {res['avg_spend']:.2f}")


def print_req_6(control):
    """
    Función que imprime la solución del Requerimiento 6 en consola
    """
    start_d = input("Fecha inicial (AAAA-MM-DD): ").strip()
    end_d = input("Fecha final (AAAA-MM-DD): ").strip()
    res = logic.req_6(control, start_d, end_d)
    print(f"\nTiempo de ejecución: {res['elapsed_time_ms']:.2f} ms")
    print(f"Total de pedidos en el rango de fechas: {res['total_count']}")
    if res['total_count'] > 0:
        mu = res['most_used_channel']
        mr = res['most_revenue_channel']
        print(f"\nCanal más usado: {mu['name']} ({mu['count']} pedidos, Recaudo total: ${mu['total_amount']:.2f})")
        print(f"Canal que más recauda: {mr['name']} ({mr['count']} pedidos, Recaudo total: ${mr['total_amount']:.2f})")

        print("\nEstadísticas por Canal:")
        for ch, st in res['channel_stats'].items():
            print(f"\n--- Canal: {ch} ---")
            print(f"Precio promedio: {st['avg_price']:.2f}, Inversión mercadeo promedio: {st['avg_spend']:.2f}")
            print("Pedido más costoso:")
            print(tabulate([print_order_row(st['most_expensive'])], headers=headers, tablefmt="grid"))
            print("Pedido más barato:")
            print(tabulate([print_order_row(st['cheapest'])], headers=headers, tablefmt="grid"))


# Se crea la lógica asociada a la vista
control = new_logic()


def main():
    """
    Menu principal
    """
    working = True
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n').strip()
        if not inputs.isdigit():
            print("Opción errónea, vuelva a elegir.\n")
            continue

        option = int(inputs)
        if option == 0:
            print("Cargando información de los archivos ....\n")
            load_data(control)
        elif option == 1:
            print_req_1(control)
        elif option == 2:
            print_req_2(control)
        elif option == 3:
            print_req_3(control)
        elif option == 4:
            print_req_4(control)
        elif option == 5:
            print_req_5(control)
        elif option == 6:
            print_req_6(control)
        elif option == 7:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()