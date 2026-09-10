import csv
csv.field_size_limit(2147483647)
from DataStructures.List import single_linked_list as sll
import time
from DataStructures.List import array_list as lt

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


def req_1(catalog, product_name):
    """
    REQ 1: Promedio de características para un producto específico.
    
    :param catalog: Catálogo principal que contiene la lista de pedidos en catalog['orders'].
    :param product_name: Nombre del producto a buscar (str).
    :return: Diccionario plano con los resultados estadísticos del requerimiento.
    """
    start_time = time.time()

    # Extraer la lista de pedidos del catálogo de manera segura
    if isinstance(catalog, dict) and 'orders' in catalog:
        dataset = catalog['orders']
    else:
        dataset = catalog

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
            "elapsed_time_ms": (end_time - start_time) * 1000,
            "total_count": 0,
            "avg_price": 0, "min_price": 0, "max_price": 0,
            "avg_discount": 0, "min_discount": 0, "max_discount": 0,
            "avg_boxes": 0, "min_boxes": 0, "max_boxes": 0,
            "avg_spend": 0, "min_spend": 0, "max_spend": 0,
            "top_year": "N/A",
            "max_amount_order": None,
            "min_amount_order": None
        }

    # 2. Inicializar acumuladores con el primer elemento
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

    sum_spend = float(first_order.get("Marketing_Spend", 0))
    min_spend = sum_spend
    max_spend = sum_spend

    max_amount_order = first_order
    min_amount_order = first_order

    year_counts = {}
    
    # Conteo manual del año del primer elemento
    if "Order_Date" in first_order and first_order["Order_Date"]:
        year = str(first_order["Order_Date"]).split("-")[0]
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

        # Inversión en mercadeo (Spend)
        mkt = float(order.get("Marketing_Spend", 0))
        sum_spend += mkt
        if mkt < min_spend: min_spend = mkt
        if mkt > max_spend: max_spend = mkt

        # Conteo de frecuencia de años
        if "Order_Date" in order and order["Order_Date"]:
            year = str(order["Order_Date"]).split("-")[0]
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
    top_year = "N/A"
    max_year_count = 0
    for year, count_val in year_counts.items():
        if count_val > max_year_count:
            max_year_count = count_val
            top_year = year

    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000

    # 5. Retornar con las claves exactas requeridas por tu view.py
    # 5. Retornar con las claves exactas requeridas por tu view.py
    # 5. Retornar con las claves exactas requeridas por tu view.py
    # 5. Retornar con las claves exactas requeridas por tu view.py
    return {
        "elapsed_time_ms": elapsed_time_ms,
        "total_count": count,
        
        "avg_price": sum_price / count,
        "min_price": min_price,
        "max_price": max_price,
        
        "avg_discount": sum_discount / count,
        "min_discount": min_discount,
        "max_discount": max_discount,
        
        "avg_boxes": sum_boxes / count,
        "min_boxes": min_boxes,
        "max_boxes": max_boxes,
        
        "avg_spend": sum_spend / count,
        "min_spend": min_spend,
        "max_spend": max_spend,
        
        "top_year": top_year,
        "max_amt_order": max_amount_order,
        "min_amt_order": min_amount_order
    }
    
def req_2(catalog, min_price, max_price):
    """
    REQ 2: Filtrar pedidos por rango de precio
    """
    start_time = time.time()
    
    # Extraer la lista de pedidos del catálogo de manera segura
    if isinstance(catalog, dict) and 'orders' in catalog:
        orders = catalog['orders']
    else:
        orders = catalog

    sz = lt.size(orders)
    filtered = lt.new_list()

    total_discount = 0.0
    count_discount = 0
    total_spend = 0.0
    count_spend = 0
    total_price = 0.0
    count_price = 0

    most_recent = None
    min_amt = None
    max_amt = None

    # Convertir min_price y max_price a float por seguridad
    min_price = float(min_price)
    max_price = float(max_price)

    for i in range(0, sz):
        elem = lt.get_element(orders, i)

        # Validación y conversión segura de Price_per_Box
        price_val = elem.get('Price_per_Box')
        if price_val is not None and price_val != "Unknown":
            try:
                price = float(price_val)
                en_rango = (min_price <= price <= max_price)
            except ValueError:
                en_rango = False
        else:
            en_rango = False

        if en_rango:
            lt.add_last(filtered, elem)

            # Procesar Descuento
            disc_val = elem.get('Discount_Pct')
            if disc_val is not None and disc_val != "Unknown":
                try:
                    total_discount += float(disc_val)
                    count_discount += 1
                except ValueError:
                    pass

            # Procesar Marketing Spend
            spend_val = elem.get('Marketing_Spend')
            if spend_val is not None and spend_val != "Unknown":
                try:
                    total_spend += float(spend_val)
                    count_spend += 1
                except ValueError:
                    pass

            total_price += price
            count_price += 1

            # Conversión segura para Amount y Date
            curr_amount = float(elem.get('Amount', 0))
            curr_date = str(elem.get('Order_Date', ''))

            # 1. Pedido más reciente (Order_Date mayor; empate -> mayor Amount)
            if most_recent is None:
                most_recent = elem
            else:
                rec_date = str(most_recent.get('Order_Date', ''))
                rec_amount = float(most_recent.get('Amount', 0))
                
                if curr_date > rec_date:
                    most_recent = elem
                elif curr_date == rec_date:
                    if curr_amount > rec_amount:
                        most_recent = elem

            # 2. Pedido de menor Amount (empate -> menor Price_per_Box)
            if min_amt is None:
                min_amt = elem
            else:
                min_amount_val = float(min_amt.get('Amount', 0))
                min_price_val = float(min_amt.get('Price_per_Box', 0))

                if curr_amount < min_amount_val:
                    min_amt = elem
                elif curr_amount == min_amount_val:
                    if price < min_price_val:
                        min_amt = elem

            # 3. Pedido de mayor Amount (empate -> menor Price_per_Box)
            if max_amt is None:
                max_amt = elem
            else:
                max_amount_val = float(max_amt.get('Amount', 0))
                max_price_val = float(max_amt.get('Price_per_Box', 0))

                if curr_amount > max_amount_val:
                    max_amt = elem
                elif curr_amount == max_amount_val:
                    if price < max_price_val:
                        max_amt = elem

    total_count = lt.size(filtered)
    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000

    if total_count == 0:
        return {
            'elapsed_time_ms': elapsed_time_ms,
            'total_count': 0
        }

    avg_discount = (total_discount / count_discount) if count_discount > 0 else 0.0
    avg_spend = (total_spend / count_spend) if count_spend > 0 else 0.0
    avg_price = (total_price / count_price) if count_price > 0 else 0.0

    return {
        'elapsed_time_ms': elapsed_time_ms,
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
    REQ 3: Promedio por país y canal usando exclusivamente la API de Singly Linked List (sll)
    """
    start_time = time.time()

    # 1. Obtener la lista de pedidos desde el catálogo
    if isinstance(catalog, dict) and 'orders' in catalog:
        orders = catalog['orders']
    else:
        orders = catalog

    # Obtener la cantidad de elementos usando sll.size
    total_orders = sll.size(orders)

    filtered = sll.new_list()

    # Normalizar parámetros de entrada
    target_country = str(country).strip().lower()
    target_channel = str(channel).strip().lower()

    # 2. Filtrar los pedidos usando la API de sll
    for i in range(total_orders):
        elem = sll.get_element(orders, i)
        c_val = str(elem.get('Country', '')).strip().lower()
        ch_val = str(elem.get('Channel', '')).strip().lower()

        if c_val == target_country and ch_val == target_channel:
            sll.add_last(filtered, elem)

    total_count = sll.size(filtered)

    if total_count == 0:
        end_time = time.time()
        return {
            'elapsed_time_ms': (end_time - start_time) * 1000,
            'total_count': 0,
            'avg_price': 0.0,
            'avg_discount': 0.0,
            'avg_spend': 0.0,
            'avg_boxes': 0.0,
            'most_freq_product': "Unknown",
            'top_year': "Unknown"
        }

    # Variables para acumuladores y contadores
    total_price = 0.0
    count_price = 0

    total_discount = 0.0
    count_discount = 0

    total_spend = 0.0
    count_spend = 0

    total_boxes = 0.0
    count_boxes = 0

    product_counts = sll.new_list()
    year_counts = sll.new_list()

    # 3. Procesar la lista filtrada usando sll.get_element
    for i in range(total_count):
        order = sll.get_element(filtered, i)

        # Precio por caja
        price_val = order.get('Price_per_Box')
        if price_val is not None and price_val != "Unknown":
            try:
                total_price += float(price_val)
                count_price += 1
            except ValueError:
                pass

        # Descuento %
        disc_val = order.get('Discount_Pct')
        if disc_val is not None and disc_val != "Unknown":
            try:
                total_discount += float(disc_val)
                count_discount += 1
            except ValueError:
                pass

        # Inversión en mercadeo
        spend_val = order.get('Marketing_Spend')
        if spend_val is not None and spend_val != "Unknown":
            try:
                total_spend += float(spend_val)
                count_spend += 1
            except ValueError:
                pass

        # Cajas enviadas
        boxes_val = order.get('Boxes_Shipped')
        if boxes_val is not None and boxes_val != "Unknown":
            try:
                total_boxes += float(boxes_val)
                count_boxes += 1
            except ValueError:
                pass

        # Frecuencia de Productos (usando SLL)
        product = order.get('Product')
        if product:
            p_size = sll.size(product_counts)
            found_product = False

            for p_idx in range(p_size):
                p_item = sll.get_element(product_counts, p_idx)
                if p_item['name'] == product:
                    p_item['count'] += 1
                    found_product = True
                    break

            if not found_product:
                sll.add_last(product_counts, {'name': product, 'count': 1})

        # Frecuencia de Años (usando SLL)
        order_date = order.get('Order_Date')
        if order_date and order_date != "Unknown":
            year = str(order_date).split("-")[0]
            y_size = sll.size(year_counts)
            found_year = False

            for y_idx in range(y_size):
                y_item = sll.get_element(year_counts, y_idx)
                if y_item['year'] == year:
                    y_item['count'] += 1
                    found_year = True
                    break

            if not found_year:
                sll.add_last(year_counts, {'year': year, 'count': 1})

    # 4. Cálculo de promedios
    avg_price = (total_price / count_price) if count_price > 0 else 0.0
    avg_discount = (total_discount / count_discount) if count_discount > 0 else 0.0
    avg_spend = (total_spend / count_spend) if count_spend > 0 else 0.0
    avg_boxes = (total_boxes / count_boxes) if count_boxes > 0 else 0.0

    # 5. Producto más frecuente
    most_freq_product = "Unknown"
    max_product_count = 0
    for p_idx in range(sll.size(product_counts)):
        p_item = sll.get_element(product_counts, p_idx)
        if p_item['count'] > max_product_count:
            max_product_count = p_item['count']
            most_freq_product = p_item['name']

    # 6. Año más frecuente
    top_year = "Unknown"
    max_year_count = 0
    for y_idx in range(sll.size(year_counts)):
        y_item = sll.get_element(year_counts, y_idx)
        if y_item['count'] > max_year_count:
            max_year_count = y_item['count']
            top_year = y_item['year']

    end_time = time.time()

    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'avg_price': avg_price,
        'avg_discount': avg_discount,
        'avg_spend': avg_spend,
        'avg_boxes': avg_boxes,
        'most_freq_product': most_freq_product,
        'top_year': top_year
    }

import time

def req_4(catalog, product, country):
    """
    REQ 4: Calcula estadísticas promedio y obtiene los 2 pedidos con mayor Amount 
    para una combinación específica de Producto y País.
    """
    start_time = time.time()

    # Extraer la lista de órdenes según la estructura del catálogo
    orders = catalog['orders'] if isinstance(catalog, dict) and 'orders' in catalog else catalog
    sz = lt.size(orders)
    
    # Lista enlazada para almacenar los elementos filtrados
    filtered = sll.new_list()

    # 1. Filtrado de datos por Producto y País
    for i in range(sz):
        elem = lt.get_element(orders, i)
        if elem.get('Product') == product and elem.get('Country') == country:
            sll.add_last(filtered, elem)

    total_count = sll.size(filtered)

    # Si no se encontraron coincidencias
    if total_count == 0:
        end_time = time.time()
        return {
            'elapsed_time_ms': (end_time - start_time) * 1000,
            'total_count': 0,
            'avg_price': 0.0,
            'avg_discount': 0.0,
            'avg_spend': 0.0,
            'avg_boxes': 0.0,
            'top_2': sll.new_list()
        }

    # Acumuladores y contadores para los promedios
    total_price = total_discount = total_spend = total_boxes = 0.0
    count_price = count_discount = count_spend = count_boxes = 0

    top_1 = None
    top_2 = None

    # 2. Recorrido de elementos filtrados mediante la API de SLL
    for i in range(total_count):
        order = sll.get_element(filtered, i)

        # Cálculo de promedios ignorando valores 'Unknown'
        if order.get('Price_per_Box') != "Unknown":
            total_price += float(order['Price_per_Box'])
            count_price += 1
            
        if order.get('Discount_Pct') != "Unknown":
            total_discount += float(order['Discount_Pct'])
            count_discount += 1
            
        if order.get('Marketing_Spend') != "Unknown":
            total_spend += float(order['Marketing_Spend'])
            count_spend += 1
            
        if order.get('Boxes_Shipped') != "Unknown":
            total_boxes += float(order['Boxes_Shipped'])
            count_boxes += 1

        # Lógica de ordenamiento / Selección de Top 2 por 'Amount'
        if top_1 is None:
            top_1 = order
        else:
            curr_amt = float(order.get('Amount', 0))
            top1_amt = float(top_1.get('Amount', 0))

            if curr_amt > top1_amt:
                top_2 = top_1
                top_1 = order
            elif curr_amt == top1_amt:
                # Criterio de desempate por menor Marketing_Spend
                curr_mkt = float(order.get('Marketing_Spend', 0))
                top1_mkt = float(top_1.get('Marketing_Spend', 0))
                if curr_mkt < top1_mkt:
                    top_2 = top_1
                    top_1 = order
                else:
                    if top_2 is None or curr_amt > float(top_2.get('Amount', 0)):
                        top_2 = order
            else:
                if top_2 is None or curr_amt > float(top_2.get('Amount', 0)):
                    top_2 = order

    # Empaquetar los mejores 2 en una lista SLL
    top_2_list = sll.new_list()
    if top_1:
        sll.add_last(top_2_list, top_1)
    if top_2:
        sll.add_last(top_2_list, top_2)

    end_time = time.time()

    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'avg_price': (total_price / count_price) if count_price > 0 else 0.0,
        'avg_discount': (total_discount / count_discount) if count_discount > 0 else 0.0,
        'avg_spend': (total_spend / count_spend) if count_spend > 0 else 0.0,
        'avg_boxes': (total_boxes / count_boxes) if count_boxes > 0 else 0.0,
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
    REQ 6: Identificar el canal con más ventas y mayor recaudación en un rango de tiempo
    """
    start_time = time.time()

    orders = catalog['orders'] if isinstance(catalog, dict) and 'orders' in catalog else catalog
    sz = lt.size(orders)
    filtered = lt.new_list()

    for i in range(sz):
        elem = lt.get_element(orders, i)
        if start_date <= str(elem.get('Order_Date', '')) <= end_date:
            lt.add_last(filtered, elem)

    total_count = lt.size(filtered)

    if total_count == 0:
        end_time = time.time()
        return {
            'elapsed_time_ms': (end_time - start_time) * 1000,
            'total_count': 0,
            'top_channel_count': "N/A",
            'top_channel_amount': "N/A"
        }

    channel_data = lt.new_list()

    for i in range(total_count):
        order = lt.get_element(filtered, i)
        channel = order.get('Channel', 'Unknown')
        amt = float(order.get('Amount', 0)) if order.get('Amount') != "Unknown" else 0.0

        channel_pos = -1
        for j in range(lt.size(channel_data)):
            item = lt.get_element(channel_data, j)
            if item['channel'] == channel:
                channel_pos = j
                break

        if channel_pos == -1:
            lt.add_last(channel_data, {
                'channel': channel,
                'count': 1,
                'total_amount': amt
            })
        else:
            item = lt.get_element(channel_data, channel_pos)
            item['count'] += 1
            item['total_amount'] += amt

    # Identificar canal con mayor volumen y mayor monto total
    max_count = -1
    max_count_channel = None

    max_amount = -1.0
    max_amount_channel = None

    for i in range(lt.size(channel_data)):
        data = lt.get_element(channel_data, i)
        if data['count'] > max_count:
            max_count = data['count']
            max_count_channel = data['channel']

        if data['total_amount'] > max_amount:
            max_amount = data['total_amount']
            max_amount_channel = data['channel']

    end_time = time.time()

    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'top_channel_count': max_count_channel,
        'top_channel_amount': max_amount_channel
    }