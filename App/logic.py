import csv
csv.field_size_limit(2147483647)
import time
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sll 

def new_logic():
    """
    Crea el catálogo inicial para almacenar la estructura de datos.
    """
    catalog = {
        'orders': lt.new_list()
    }
    return catalog


def load_data(catalog, filename):
    """
    Carga los datos del reto desde el archivo CSV.
    """
    csv.field_size_limit(2147483647)
    
    start_time = time.time()
    catalog['orders'] = lt.new_list()
    
    total_records = 0
    min_amount_order = None
    max_amount_order = None
    
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for raw_row in reader:
            # 1. Limpiar las llaves del diccionario
            row = {}
            for key, val in raw_row.items():
                if key is not None:
                    clean_key = key.strip()
                    row[clean_key] = val

            total_records += 1
            
            # 2. Procesar cada campo directamente aquí adentro
            
            # Campos de texto
            order_id = row.get('Order_ID')
            if order_id is not None and str(order_id).strip() != "":
                order_id_val = str(order_id).strip()
            else:
                order_id_val = "Unknown"

            product = row.get('Product')
            if product is not None and str(product).strip() != "":
                product_val = str(product).strip()
            else:
                product_val = "Unknown"

            country = row.get('Country')
            if country is not None and str(country).strip() != "":
                country_val = str(country).strip()
            else:
                country_val = "Unknown"

            channel = row.get('Channel')
            if channel is not None and str(channel).strip() != "":
                channel_val = str(channel).strip()
            else:
                channel_val = "Unknown"

            order_date = row.get('Order_Date')
            if order_date is not None and str(order_date).strip() != "":
                order_date_val = str(order_date).strip()
            else:
                order_date_val = "Unknown"

            # Campo Discount_Pct (float)
            disc = row.get('Discount_Pct')
            if disc is not None and str(disc).strip() != "":
                try:
                    disc_val = float(disc)
                except ValueError:
                    disc_val = "Unknown"
            else:
                disc_val = "Unknown"

            # Campo Price_per_Box (float)
            price = row.get('Price_per_Box')
            if price is not None and str(price).strip() != "":
                try:
                    price_val = float(price)
                except ValueError:
                    price_val = "Unknown"
            else:
                price_val = "Unknown"

            # Campo Marketing_Spend (float)
            mkt = row.get('Marketing_Spend')
            if mkt is not None and str(mkt).strip() != "":
                try:
                    mkt_val = float(mkt)
                except ValueError:
                    mkt_val = "Unknown"
            else:
                mkt_val = "Unknown"

            # Campo Boxes_Shipped (int)
            boxes = row.get('Boxes_Shipped')
            if boxes is not None and str(boxes).strip() != "":
                try:
                    boxes_val = int(boxes)
                except ValueError:
                    boxes_val = "Unknown"
            else:
                boxes_val = "Unknown"

            # Campo Amount (float)
            amt = row.get('Amount')
            if amt is not None and str(amt).strip() != "":
                try:
                    amt_val = float(amt)
                except ValueError:
                    amt_val = "Unknown"
            else:
                amt_val = "Unknown"

            # 3. Construir el diccionario del pedido
            order = {
                'Order_ID': order_id_val,
                'Product': product_val,
                'Country': country_val,
                'Channel': channel_val,
                'Order_Date': order_date_val,
                'Discount_Pct': disc_val,
                'Price_per_Box': price_val,
                'Marketing_Spend': mkt_val,
                'Boxes_Shipped': boxes_val,
                'Amount': amt_val
            }
            
            # Guardar en la estructura de datos lt
            lt.add_last(catalog['orders'], order)
            
            # 4. Búsqueda del menor Amount (Desempate por menor Price_per_Box)
            if min_amount_order is None:
                min_amount_order = order
            elif order['Amount'] != "Unknown" and min_amount_order['Amount'] != "Unknown":
                if order['Amount'] < min_amount_order['Amount']:
                    min_amount_order = order
                elif order['Amount'] == min_amount_order['Amount']:
                    if order['Price_per_Box'] != "Unknown" and min_amount_order['Price_per_Box'] != "Unknown":
                        if order['Price_per_Box'] < min_amount_order['Price_per_Box']:
                            min_amount_order = order
                            
            # 5. Búsqueda del mayor Amount (Desempate por menor Price_per_Box)
            if max_amount_order is None:
                max_amount_order = order
            elif order['Amount'] != "Unknown" and max_amount_order['Amount'] != "Unknown":
                if order['Amount'] > max_amount_order['Amount']:
                    max_amount_order = order
                elif order['Amount'] == max_amount_order['Amount']:
                    if order['Price_per_Box'] != "Unknown" and max_amount_order['Price_per_Box'] != "Unknown":
                        if order['Price_per_Box'] < max_amount_order['Price_per_Box']:
                            max_amount_order = order

    end_time = time.time()
    
    # 6. Obtener los primeros 5 y últimos 5 usando lt
    first_5 = []
    last_5 = []
    sz = lt.size(catalog['orders'])
    
    if sz > 0:
        limit_first = 5
        if sz < 5:
            limit_first = sz
            
        for i in range(limit_first):
            element = lt.get_element(catalog['orders'], i)
            first_5.append(element)
            
        start_index = 0
        if sz > 5:
            start_index = sz - 5
            
        for i in range(start_index, sz):
            element = lt.get_element(catalog['orders'], i)
            last_5.append(element)

    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_orders': total_records,
        'min_amount_order': min_amount_order,
        'max_amount_order': max_amount_order,
        'first_5': first_5,
        'last_5': last_5
    }

import time
import DataStructures.List.array_list as lt


def req_1(dataset, product_name):
    """
    REQ 1: Promedio de características para un producto específico.
    
    :param dataset: Lista (TAD lt/array_list) con todos los pedidos cargados.
    :param product_name: Nombre del producto a buscar (str).
    :return: Diccionario con los resultados estadísticos del requerimiento.
    """
    start_time = time.time()

    # 1. Filtrar los pedidos del producto especificado usando la estructura lt
    filtered_list = lt.new_list()
    total_dataset = lt.size(dataset)

    for i in range(total_dataset):
        order = lt.get_element(dataset, i)
        if order.get("Product") == product_name:
            lt.add_last(filtered_list, order)

    count = lt.size(filtered_list)

    # Si no se encontraron pedidos para ese producto
    if count == 0:
        end_time = time.time()
        return {
            "execution_time_ms": (end_time - start_time) * 1000,
            "total_orders": 0,
            "price_per_box": {"avg": 0, "min": 0, "max": 0},
            "discount_pct": {"avg": 0, "min": 0, "max": 0},
            "boxes_shipped": {"avg": 0, "min": 0, "max": 0},
            "marketing_spend": {"avg": 0, "min": 0, "max": 0},
            "most_frequent_year": "N/A",
            "max_amount_order": None,
            "min_amount_order": None
        }

    # 2. Inicializar acumuladores y variables extremas con el primer elemento
    first_order = lt.get_element(filtered_list, 0)

    sum_price = float(first_order.get("Price_per_Box", 0))
    min_price = sum_price
    max_price = sum_price

    sum_discount = float(first_order.get("Discount_Pct", 0))
    min_discount = sum_discount
    max_discount = sum_discount

    sum_boxes = float(first_order.get("Boxes_Shipped", 0))
    min_boxes = sum_boxes
    max_boxes = sum_boxes

    sum_marketing = float(first_order.get("Marketing_Spend", 0))
    min_marketing = sum_marketing
    max_marketing = sum_marketing

    max_amount_order = first_order
    min_amount_order = first_order

    year_counts = {}
    
    # Conteo manual del año del primer elemento
    if "Order_Date" in first_order and first_order["Order_Date"]:
        year = first_order["Order_Date"].split("-")[0]
        year_counts[year] = 1

    # 3. Recorrer la lista filtrada para acumular y comparar
    for i in range(1, count):
        order = lt.get_element(filtered_list, i)

        # Precios
        price = float(order.get("Price_per_Box", 0))
        sum_price += price
        if price < min_price: min_price = price
        if price > max_price: max_price = price

        # Descuentos
        discount = float(order.get("Discount_Pct", 0))
        sum_discount += discount
        if discount < min_discount: min_discount = discount
        if discount > max_discount: max_discount = discount

        # Cajas enviadas
        boxes = float(order.get("Boxes_Shipped", 0))
        sum_boxes += boxes
        if boxes < min_boxes: min_boxes = boxes
        if boxes > max_boxes: max_boxes = boxes

        # Inversión en mercadeo
        mkt = float(order.get("Marketing_Spend", 0))
        sum_marketing += mkt
        if mkt < min_marketing: min_marketing = mkt
        if mkt > max_marketing: max_marketing = mkt

        # Conteo de frecuencia de años (manual)
        if "Order_Date" in order and order["Order_Date"]:
            year = order["Order_Date"].split("-")[0]
            if year in year_counts:
                year_counts[year] += 1
            else:
                year_counts[year] = 1

        # Comparación de MAX Amount (Desempate: menor Marketing_Spend)
        curr_amount = float(order.get("Amount", 0))
        max_amount = float(max_amount_order.get("Amount", 0))

        if curr_amount > max_amount:
            max_amount_order = order
        elif curr_amount == max_amount:
            curr_mkt = float(order.get("Marketing_Spend", 0))
            max_mkt = float(max_amount_order.get("Marketing_Spend", 0))
            if curr_mkt < max_mkt:
                max_amount_order = order

        # Comparación de MIN Amount (Desempate: menor Marketing_Spend)
        min_amount = float(min_amount_order.get("Amount", 0))

        if curr_amount < min_amount:
            min_amount_order = order
        elif curr_amount == min_amount:
            curr_mkt = float(order.get("Marketing_Spend", 0))
            min_mkt = float(min_amount_order.get("Marketing_Spend", 0))
            if curr_mkt < min_mkt:
                min_amount_order = order

    # 4. Cálculo manual del año con más pedidos
    most_frequent_year = "N/A"
    max_year_count = 0
    for year, count_val in year_counts.items():
        if count_val > max_year_count:
            max_year_count = count_val
            most_frequent_year = year

    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000

    # 5. Retornar el diccionario estructurado
    return {
        "execution_time_ms": execution_time_ms,
        "total_orders": count,
        "price_per_box": {
            "avg": sum_price / count,
            "min": min_price,
            "max": max_price
        },
        "discount_pct": {
            "avg": sum_discount / count,
            "min": min_discount,
            "max": max_discount
        },
        "boxes_shipped": {
            "avg": sum_boxes / count,
            "min": min_boxes,
            "max": max_boxes
        },
        "marketing_spend": {
            "avg": sum_marketing / count,
            "min": min_marketing,
            "max": max_marketing
        },
        "most_frequent_year": most_frequent_year,
        "max_amount_order": {
            "Amount": max_amount_order.get("Amount"),
            "Order_ID": max_amount_order.get("Order_ID"),
            "Country": max_amount_order.get("Country"),
            "Order_Date": max_amount_order.get("Order_Date"),
            "Price_per_Box": max_amount_order.get("Price_per_Box")
        },
        "min_amount_order": {
            "Amount": min_amount_order.get("Amount"),
            "Order_ID": min_amount_order.get("Order_ID"),
            "Country": min_amount_order.get("Country"),
            "Order_Date": min_amount_order.get("Order_Date"),
            "Price_per_Box": min_amount_order.get("Price_per_Box")
        }
    }

def req_2(catalog, min_price, max_price):
    """
    REQ 2: Filtrar pedidos por rango de precio
    """

    start_time = get_time()
    orders = catalog['orders']
    sz = lt.size(orders)
 
    # 'filtered' es un array_list, no una lista nativa
    filtered = lt.new_list()
 
    total_discount = 0
    count_discount = 0
    total_spend = 0
    count_spend = 0
    total_price = 0
    count_price = 0
 
    # Acumuladores para no tener que recorrer 'filtered' otra vez
    most_recent = None
    min_amt = None
    max_amt = None
 
    for i in range(0, sz):
        elem = lt.get_element(orders, i)
 
        # En vez de 'continue', envolvemos todo el procesamiento
        # en un único if: solo entra si el precio es válido y
        # está dentro del rango pedido.
        precio_valido = elem['Price_per_Box'] != "Unknown"
        en_rango = precio_valido and (min_price <= elem['Price_per_Box'] <= max_price)
 
        if en_rango:
            lt.add_last(filtered, elem)
 
            if elem['Discount_Pct'] != "Unknown":
                total_discount += elem['Discount_Pct']
                count_discount += 1
 
            if elem['Marketing_Spend'] != "Unknown":
                total_spend += elem['Marketing_Spend']
                count_spend += 1
 
            total_price += elem['Price_per_Box']
            count_price += 1
 
            # Pedido más reciente (Order_Date más grande; empate -> mayor Amount)
            if most_recent is None:
                most_recent = elem
            elif elem['Order_Date'] > most_recent['Order_Date']:
                most_recent = elem
            elif elem['Order_Date'] == most_recent['Order_Date']:
                if elem['Amount'] > most_recent['Amount']:
                    most_recent = elem
 
            # Pedido de menor Amount (empate -> menor Price_per_Box)
            if min_amt is None:
                min_amt = elem
            elif elem['Amount'] < min_amt['Amount']:
                min_amt = elem
            elif elem['Amount'] == min_amt['Amount']:
                if elem['Price_per_Box'] < min_amt['Price_per_Box']:
                    min_amt = elem
 
            # Pedido de mayor Amount (empate -> menor Price_per_Box)
            if max_amt is None:
                max_amt = elem
            elif elem['Amount'] > max_amt['Amount']:
                max_amt = elem
            elif elem['Amount'] == max_amt['Amount']:
                if elem['Price_per_Box'] < max_amt['Price_per_Box']:
                    max_amt = elem
 
    total_count = lt.size(filtered)
 
    if total_count == 0:
        return {
            'elapsed_time_ms': delta_time(start_time, get_time()),
            'total_count': 0
        }
 
    if count_discount > 0:
        avg_discount = total_discount / count_discount
    else:
        avg_discount = 0
 
    if count_spend > 0:
        avg_spend = total_spend / count_spend
    else:
        avg_spend = 0
 
    if count_price > 0:
        avg_price = total_price / count_price
    else:
        avg_price = 0
 
    end_time = get_time()
    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'total_count': total_count,
        'avg_discount': avg_discount,
        'avg_spend': avg_spend,
        'avg_price': avg_price,
        'most_recent': most_recent,
        'min_amt': min_amt,
        'max_amt': max_amt
    }
 


def req_3(catalog, country, channel):
    """
    REQ 3: Promedio por país y canal
    """
    
    start_time = get_time()
    
    orders = catalog['orders']
    sz = list_structure.size(orders)

    filtered = sll.new_list()

    for i in range(sz):
        elem = list_structure.get_element(orders, i)

        if elem['Country'] == country and elem['Channel'] == channel:
            sll.add_last(filtered, elem)

    total_count = sll.size(filtered)

    # Si no hay pedidos
    if total_count == 0:
        return {
            'elapsed_time_ms': delta_time(start_time, get_time()),
            'total_count': 0
        }

    total_price = 0
    count_price = 0

    total_discount = 0
    count_discount = 0

    total_spend = 0
    count_spend = 0

    total_boxes = 0
    count_boxes = 0

    product_counts = sll.new_list()
    year_counts = sll.new_list()

    current = filtered['first']

    while current is not None:

        order = current['info']

        if order['Price_per_Box'] != "Unknown":
            total_price += order['Price_per_Box']
            count_price += 1

        if order['Discount_Pct'] != "Unknown":
            total_discount += order['Discount_Pct']
            count_discount += 1

        if order['Marketing_Spend'] != "Unknown":
            total_spend += order['Marketing_Spend']
            count_spend += 1
            
        if order['Boxes_Shipped'] != "Unknown":
            total_boxes += order['Boxes_Shipped']
            count_boxes += 1

        product = order['Product']

        product_node = product_counts['first']
        found_product = False

        while product_node is not None:

            if product_node['info']['name'] == product:
                product_node['info']['count'] += 1
                found_product = True
                break

            product_node = product_node['next']

        if not found_product:
            product_data = {
                'name': product,
                'count': 1
            }

            sll.add_last(product_counts, product_data)

        if order['Order_Date'] != "Unknown":

            year = order['Order_Date'].split("-")[0]

            year_node = year_counts['first']
            found_year = False

            while year_node is not None:

                if year_node['info']['year'] == year:
                    year_node['info']['count'] += 1
                    found_year = True
                    break

                year_node = year_node['next']

            if not found_year:

                year_data = {
                    'year': year,
                    'count': 1
                }

                sll.add_last(year_counts, year_data)

        current = current['next']

    if count_price > 0:
        avg_price = total_price / count_price
    else:
        avg_price = 0

    if count_discount > 0:
        avg_discount = total_discount / count_discount
    else:
        avg_discount = 0

    if count_spend > 0:
        avg_spend = total_spend / count_spend
    else:
        avg_spend = 0

    if count_boxes > 0:
        avg_boxes = total_boxes / count_boxes
    else:
        avg_boxes = 0

    most_freq_product = "Unknown"
    max_product_count = 0

    product_node = product_counts['first']

    while product_node is not None:

        product_data = product_node['info']

        if product_data['count'] > max_product_count:
            max_product_count = product_data['count']
            most_freq_product = product_data['name']

        product_node = product_node['next']

    top_year = "Unknown"
    max_year_count = 0

    year_node = year_counts['first']

    while year_node is not None:

        year_data = year_node['info']

        if year_data['count'] > max_year_count:
            max_year_count = year_data['count']
            top_year = year_data['year']

        year_node = year_node['next']

    end_time = get_time()

    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'total_count': total_count,
        'avg_price': avg_price,
        'avg_discount': avg_discount,
        'avg_spend': avg_spend,
        'avg_boxes': avg_boxes,
        'most_freq_product': most_freq_product,
        'top_year': top_year
    }


def req_4(catalog, product, country):
    """
    REQ 4: Precio promedio para una combinación Producto-País
    """
    start_time = get_time()

    orders = catalog['orders']
    sz = list_structure.size(orders)
    filtered = sll.new_list()
    
    for i in range(sz):

        elem = list_structure.get_element(orders, i)

        if elem['Product'] == product and elem['Country'] == country:
            sll.add_last(filtered, elem)

    total_count = sll.size(filtered)

    if total_count == 0:
        return {
            'elapsed_time_ms': delta_time(start_time, get_time()),
            'total_count': 0
        }

    total_price = 0
    count_price = 0

    total_discount = 0
    count_discount = 0

    total_spend = 0
    count_spend = 0

    total_boxes = 0
    count_boxes = 0

    current = filtered['first']

    while current is not None:

        order = current['info']

        if order['Price_per_Box'] != "Unknown":
            total_price += order['Price_per_Box']
            count_price += 1

        if order['Discount_Pct'] != "Unknown":
            total_discount += order['Discount_Pct']
            count_discount += 1

        if order['Marketing_Spend'] != "Unknown":
            total_spend += order['Marketing_Spend']
            count_spend += 1

        if order['Boxes_Shipped'] != "Unknown":
            total_boxes += order['Boxes_Shipped']
            count_boxes += 1

        current = current['next']

    if count_price > 0:
        avg_price = total_price / count_price
    else:
        avg_price = 0

    if count_discount > 0:
        avg_discount = total_discount / count_discount
    else:
        avg_discount = 0

    if count_spend > 0:
        avg_spend = total_spend / count_spend
    else:
        avg_spend = 0

    if count_boxes > 0:
        avg_boxes = total_boxes / count_boxes
    else:
        avg_boxes = 0

    first = filtered['first']['info']

    top_1 = first
    top_2 = None

    current = filtered['first']['next']

    while current is not None:

        order = current['info']

        if order['Amount'] > top_1['Amount']:

            top_2 = top_1
            top_1 = order

        elif order['Amount'] == top_1['Amount']:

            if order['Marketing_Spend'] < top_1['Marketing_Spend']:

                top_2 = top_1
                top_1 = order

            elif order['Marketing_Spend'] == top_1['Marketing_Spend']:

                order_id = int(
                    order['Order_ID'].replace("ORD", "")
                    if order['Order_ID'].startswith("ORD")
                    else order['Order_ID']
                )

                top_1_id = int(
                    top_1['Order_ID'].replace("ORD", "")
                    if top_1['Order_ID'].startswith("ORD")
                    else top_1['Order_ID']
                )

                if order_id > top_1_id:
                    top_2 = top_1
                    top_1 = order

                else:
                    if top_2 is None or order['Amount'] > top_2['Amount']:
                        top_2 = order

        else:

            if top_2 is None:

                top_2 = order

            elif order['Amount'] > top_2['Amount']:

                top_2 = order

            elif order['Amount'] == top_2['Amount']:

                if order['Marketing_Spend'] < top_2['Marketing_Spend']:
                    top_2 = order

                elif order['Marketing_Spend'] == top_2['Marketing_Spend']:

                    order_id = int(
                        order['Order_ID'].replace("ORD", "")
                        if order['Order_ID'].startswith("ORD")
                        else order['Order_ID']
                    )

                    top_2_id = int(
                        top_2['Order_ID'].replace("ORD", "")
                        if top_2['Order_ID'].startswith("ORD")
                        else top_2['Order_ID']
                    )

                    if order_id > top_2_id:
                        top_2 = order

        current = current['next']
        
    top_2_list = sll.new_list()

    sll.add_last(top_2_list, top_1)

    if top_2 is not None:
        sll.add_last(top_2_list, top_2)

    end_time = get_time()

    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'total_count': total_count,
        'avg_price': avg_price,
        'avg_discount': avg_discount,
        'avg_spend': avg_spend,
        'avg_boxes': avg_boxes,
        'top_2': top_2_list
    }

def req_5(catalog, filter_type, product, start_date, end_date):
    """
    REQ 5: Identificar el pedido de menor/mayor monto de un producto en un rango de fechas
    """
    start_time = get_time()
    orders = catalog['orders']
    sz = lt.size(orders)
 
    filtro = filter_type.upper()
 
    total_price = 0
    count_price = 0
    total_boxes = 0
    count_boxes = 0
    total_spend = 0
    count_spend = 0
 
    total_count = 0
    selected_order = None
 
    for i in range(0, sz):
        elem = lt.get_element(orders, i)
 
        coincide_producto = elem['Product'] == product
        en_rango_fechas = start_date <= elem['Order_Date'] <= end_date
 
        if coincide_producto and en_rango_fechas:
            total_count += 1
 
            if elem['Price_per_Box'] != "Unknown":
                total_price += elem['Price_per_Box']
                count_price += 1
 
            if elem['Boxes_Shipped'] != "Unknown":
                total_boxes += elem['Boxes_Shipped']
                count_boxes += 1
 
            if elem['Marketing_Spend'] != "Unknown":
                total_spend += elem['Marketing_Spend']
                count_spend += 1
 
            if selected_order is None:
                selected_order = elem
            elif filtro == "MENOR":
                if elem['Amount'] < selected_order['Amount']:
                    selected_order = elem
                elif elem['Amount'] == selected_order['Amount']:
                    if elem['Price_per_Box'] < selected_order['Price_per_Box']:
                        selected_order = elem
                    elif elem['Price_per_Box'] == selected_order['Price_per_Box']:
                        if elem['Marketing_Spend'] < selected_order['Marketing_Spend']:
                            selected_order = elem
            else:
                if elem['Amount'] > selected_order['Amount']:
                    selected_order = elem
                elif elem['Amount'] == selected_order['Amount']:
                    if elem['Price_per_Box'] < selected_order['Price_per_Box']:
                        selected_order = elem
                    elif elem['Price_per_Box'] == selected_order['Price_per_Box']:
                        if elem['Marketing_Spend'] < selected_order['Marketing_Spend']:
                            selected_order = elem
 
    if total_count == 0:
        return {
            'elapsed_time_ms': delta_time(start_time, get_time()),
            'total_count': 0
        }
 
    if count_price > 0:
        avg_price = total_price / count_price
    else:
        avg_price = 0
 
    if count_boxes > 0:
        avg_boxes = total_boxes / count_boxes
    else:
        avg_boxes = 0
 
    if count_spend > 0:
        avg_spend = total_spend / count_spend
    else:
        avg_spend = 0
 
    end_time = get_time()
    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'filter_type': filtro,
        'total_count': total_count,
        'selected_order': selected_order,
        'avg_price': avg_price,
        'avg_boxes': avg_boxes,
        'avg_spend': avg_spend
    }



def req_6(catalog, start_date, end_date):
    """
    REQ 6: Identificar el canal con más ventas y mayor recaudación
    en un rango de tiempo
    """

    start_time = get_time()

    orders = catalog['orders']
    sz = list_structure.size(orders)

    filtered = lt.new_list()

    for i in range(sz):

        elem = list_structure.get_element(orders, i)

        if start_date <= elem['Order_Date'] <= end_date:
            lt.add_last(filtered, elem)

    total_count = lt.size(filtered)

    if total_count == 0:
        return {
            'elapsed_time_ms': delta_time(start_time, get_time()),
            'total_count': 0
        }

    channel_data = lt.new_list()

    for i in range(lt.size(filtered)):

        order = lt.get_element(filtered, i)
        channel = order['Channel']

        channel_position = -1

        for j in range(lt.size(channel_data)):

            data = lt.get_element(channel_data, j)

            if data['channel'] == channel:
                channel_position = j
                break

        if channel_position == -1:

            new_channel = {
                'channel': channel,
                'count': 1,
                'total_amount': order['Amount'],

                'total_price': (
                    order['Price_per_Box']
                    if order['Price_per_Box'] != "Unknown"
                    else 0
                ),

                'count_price': (
                    1
                    if order['Price_per_Box'] != "Unknown"
                    else 0
                ),

                'total_spend': (
                    order['Marketing_Spend']
                    if order['Marketing_Spend'] != "Unknown"
                    else 0
                ),

                'count_spend': (
                    1
                    if order['Marketing_Spend'] != "Unknown"
                    else 0
                ),

                'most_expensive': order,
                'cheapest': order
            }

            lt.add_last(channel_data, new_channel)

        else:

            data = lt.get_element(channel_data, channel_position)

            data['count'] += 1
            data['total_amount'] += order['Amount']

            if order['Price_per_Box'] != "Unknown":
                data['total_price'] += order['Price_per_Box']
                data['count_price'] += 1
                
            if order['Marketing_Spend'] != "Unknown":
                data['total_spend'] += order['Marketing_Spend']
                data['count_spend'] += 1

            if order['Amount'] > data['most_expensive']['Amount']:
                data['most_expensive'] = order

            if order['Amount'] < data['cheapest']['Amount']:
                data['cheapest'] = order

    first_channel = lt.get_element(channel_data, 0)

    most_used_channel = first_channel
    most_revenue_channel = first_channel

    for i in range(1, lt.size(channel_data)):

        data = lt.get_element(channel_data, i)

        if data['count'] > most_used_channel['count']:
            most_used_channel = data

        if data['total_amount'] > most_revenue_channel['total_amount']:
            most_revenue_channel = data

    channel_stats = lt.new_list()

    for i in range(lt.size(channel_data)):

        data = lt.get_element(channel_data, i)
        
        if data['count_price'] > 0:
            avg_price = data['total_price'] / data['count_price']
        else:
            avg_price = "Unknown"

        if data['count_spend'] > 0:
            avg_spend = data['total_spend'] / data['count_spend']
        else:
            avg_spend = "Unknown"

        stats = {
            'channel': data['channel'],
            'avg_price': avg_price,
            'avg_spend': avg_spend,
            'most_expensive': data['most_expensive'],
            'cheapest': data['cheapest']
        }

        lt.add_last(channel_stats, stats)

    end_time = get_time()

    return {
        'elapsed_time_ms': delta_time(start_time, end_time),

        'total_count': total_count,

        'most_used_channel': {
            'name': most_used_channel['channel'],
            'count': most_used_channel['count'],
            'total_amount': most_used_channel['total_amount']
        },

        'most_revenue_channel': {
            'name': most_revenue_channel['channel'],
            'count': most_revenue_channel['count'],
            'total_amount': most_revenue_channel['total_amount']
        },

        'channel_stats': channel_stats
    }