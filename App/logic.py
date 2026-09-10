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


def req_1(catalog, product):
    """
    REQ 1: Calcula estadísticas y promedios para un producto específico usando SLL.
    """
    start_time = time.time()

    # Extraer la lista general
    orders = catalog['orders'] if isinstance(catalog, dict) and 'orders' in catalog else catalog
    sz = lt.size(orders)
    
    # 1. Filtrar usando Single Linked List (SLL)
    filtered = sll.new_list()
    prod_target = str(product).strip().lower()

    for i in range(sz):
        elem = lt.get_element(orders, i)
        prod_val = str(elem.get('Product', '')).strip().lower()
        if prod_val == prod_target:
            sll.add_last(filtered, elem)

    total_count = sll.size(filtered)

    if total_count == 0:
        end_time = time.time()
        return {
            'elapsed_time_ms': (end_time - start_time) * 1000,
            'total_count': 0,
            'max_amt_order': None,
            'min_amt_order': None
        }

    # Acumuladores y valores de comparación
    sum_price = sum_disc = sum_boxes = sum_spend = 0.0
    min_price = min_disc = min_boxes = min_spend = float('inf')
    max_price = max_disc = max_boxes = max_spend = float('-inf')

    year_counts = {}
    max_amt_order = None
    min_amt_order = None

    # 2. Recorrer la Single Linked List
    for i in range(total_count):
        elem = sll.get_element(filtered, i)

        # Conversiones seguras
        price = float(elem.get('Price_per_Box', 0)) if elem.get('Price_per_Box') != "Unknown" else 0.0
        disc = float(elem.get('Discount_Pct', 0)) if elem.get('Discount_Pct') != "Unknown" else 0.0
        boxes = float(elem.get('Boxes_Shipped', 0)) if elem.get('Boxes_Shipped') != "Unknown" else 0.0
        spend = float(elem.get('Marketing_Spend', 0)) if elem.get('Marketing_Spend') != "Unknown" else 0.0
        amount = float(elem.get('Amount', 0)) if elem.get('Amount') != "Unknown" else 0.0

        # Sumas
        sum_price += price
        sum_disc += disc
        sum_boxes += boxes
        sum_spend += spend

        # Mínimos y Máximos
        min_price, max_price = min(min_price, price), max(max_price, price)
        min_disc, max_disc = min(min_disc, disc), max(max_disc, disc)
        min_boxes, max_boxes = min(min_boxes, boxes), max(max_boxes, boxes)
        min_spend, max_spend = min(min_spend, spend), max(max_spend, spend)

        # Año con más pedidos
        o_date = str(elem.get('Order_Date', '')).strip()
        year = o_date[:4] if len(o_date) >= 4 else "Unknown"
        year_counts[year] = year_counts.get(year, 0) + 1

        # Pedido con MAYOR Amount (desempate por menor Marketing_Spend)
        if max_amt_order is None:
            max_amt_order = elem
        else:
            curr_max_amt = float(max_amt_order.get('Amount', 0))
            if amount > curr_max_amt:
                max_amt_order = elem
            elif amount == curr_max_amt:
                if spend < float(max_amt_order.get('Marketing_Spend', 0)):
                    max_amt_order = elem

        # Pedido con MENOR Amount (desempate por menor Marketing_Spend)
        if min_amt_order is None:
            min_amt_order = elem
        else:
            curr_min_amt = float(min_amt_order.get('Amount', 0))
            if amount < curr_min_amt:
                min_amt_order = elem
            elif amount == curr_min_amt:
                if spend < float(min_amt_order.get('Marketing_Spend', 0)):
                    min_amt_order = elem

    top_year = max(year_counts, key=year_counts.get) if year_counts else "N/A"
    end_time = time.time()

    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'avg_price': sum_price / total_count,
        'min_price': min_price,
        'max_price': max_price,
        'avg_discount': sum_disc / total_count,
        'min_discount': min_disc,
        'max_discount': max_disc,
        'avg_boxes': sum_boxes / total_count,
        'min_boxes': min_boxes,
        'max_boxes': max_boxes,
        'avg_spend': sum_spend / total_count,
        'min_spend': min_spend,
        'max_spend': max_spend,
        'top_year': top_year,
        'max_amt_order': max_amt_order,  # Llave corregida para el view
        'min_amt_order': min_amt_order   # Llave corregida para el view
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



import time

import time

import time

def req_3(catalog, country="any", channel="any"):
    """
    REQ 3: Retorna estadísticas (promedios, producto más frecuente y año con más pedidos)
    filtrando por País y/o Canal.
    """
    start_time = time.time()

    orders = catalog['orders'] if isinstance(catalog, dict) and 'orders' in catalog else catalog
    sz = lt.size(orders)
    filtered = lt.new_list()

    c_target = str(country).strip().lower()
    ch_target = str(channel).strip().lower()

    # 1. Filtrado por País y Canal
    for i in range(sz):
        elem = lt.get_element(orders, i)
        
        elem_country = str(elem.get('Country', elem.get('country', ''))).strip().lower()
        elem_channel = str(elem.get('Channel', elem.get('channel', ''))).strip().lower()

        match_country = (c_target == "any" or c_target == "" or elem_country == c_target)
        match_channel = (ch_target == "any" or ch_target == "" or elem_channel == ch_target)

        if match_country and match_channel:
            lt.add_last(filtered, elem)

    total_count = lt.size(filtered)

    if total_count == 0:
        end_time = time.time()
        return {
            'elapsed_time_ms': (end_time - start_time) * 1000,
            'total_count': 0,
            'avg_price': 0.0,
            'avg_discount': 0.0,
            'avg_spend': 0.0,
            'avg_boxes': 0.0,
            'most_freq_product': "N/A",
            'top_year': "N/A"
        }

    # 2. Acumulación para promedios y conteo de frecuencias
    sum_discount = 0.0
    sum_price = 0.0
    sum_spend = 0.0
    sum_boxes = 0.0

    product_counts = {}
    year_counts = {}

    for i in range(total_count):
        order = lt.get_element(filtered, i)

        disc = float(order.get('Discount_Pct', order.get('discount_pct', 0))) if order.get('Discount_Pct') != "Unknown" else 0.0
        price = float(order.get('Price_per_Box', order.get('price_per_box', 0))) if order.get('Price_per_Box') != "Unknown" else 0.0
        spend = float(order.get('Marketing_Spend', order.get('marketing_spend', 0))) if order.get('Marketing_Spend') != "Unknown" else 0.0
        boxes = float(order.get('Boxes_Shipped', order.get('boxes_shipped', 0))) if order.get('Boxes_Shipped') != "Unknown" else 0.0

        sum_discount += disc
        sum_price += price
        sum_spend += spend
        sum_boxes += boxes

        # Producto más frecuente
        prod = order.get('Product', order.get('product', 'Unknown'))
        product_counts[prod] = product_counts.get(prod, 0) + 1

        # Año con más pedidos (extrae los primeros 4 dígitos de Order_Date)
        o_date = str(order.get('Order_Date', order.get('order_date', ''))).strip()
        year = o_date[:4] if len(o_date) >= 4 else "Unknown"
        year_counts[year] = year_counts.get(year, 0) + 1

    most_freq_product = max(product_counts, key=product_counts.get) if product_counts else "N/A"
    top_year = max(year_counts, key=year_counts.get) if year_counts else "N/A"

    end_time = time.time()

    # Retorno con las llaves exactas que busca print_req_3
    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'avg_price': sum_price / total_count,
        'avg_discount': sum_discount / total_count,
        'avg_spend': sum_spend / total_count,
        'avg_boxes': sum_boxes / total_count,
        'most_freq_product': most_freq_product,
        'top_year': top_year
    }

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

def req_5(catalog, ftype, product, start_date, end_date):
    """
    REQ 5: Encuentra el pedido con MAYOR o MENOR valor para un producto y rango de fechas,
    y calcula los promedios del grupo filtrado.
    """
    start_time = time.time()

    orders = catalog['orders'] if isinstance(catalog, dict) and 'orders' in catalog else catalog
    sz = lt.size(orders)
    filtered = lt.new_list()

    # Normalizar búsqueda del producto
    prod_target = str(product).strip().lower()

    # 1. Filtrar pedidos por producto y rango de fechas
    for i in range(sz):
        elem = lt.get_element(orders, i)
        
        prod_val = str(elem.get('Product', '')).strip().lower()
        order_date = str(elem.get('Order_Date', '')).strip()

        if prod_val == prod_target and (start_date <= order_date <= end_date):
            lt.add_last(filtered, elem)

    total_count = lt.size(filtered)

    if total_count == 0:
        end_time = time.time()
        return {
            'elapsed_time_ms': (end_time - start_time) * 1000,
            'filter_type': ftype,
            'total_count': 0,
            'selected_order': None,
            'avg_price': 0.0,
            'avg_boxes': 0.0,
            'avg_spend': 0.0
        }

    # 2. Buscar el pedido MAYOR o MENOR según Amount y sumar promedios
    selected_order = lt.get_element(filtered, 0)
    best_value = float(selected_order.get('Amount', 0)) if selected_order.get('Amount') != "Unknown" else 0.0

    sum_price = 0.0
    sum_boxes = 0.0
    sum_spend = 0.0

    for i in range(total_count):
        curr_order = lt.get_element(filtered, i)
        
        # Extracción para promedios
        price = float(curr_order['Price_per_Box']) if curr_order.get('Price_per_Box') != "Unknown" else 0.0
        boxes = float(curr_order['Boxes_Shipped']) if curr_order.get('Boxes_Shipped') != "Unknown" else 0.0
        spend = float(curr_order['Marketing_Spend']) if curr_order.get('Marketing_Spend') != "Unknown" else 0.0
        
        curr_amt = curr_order.get('Amount', 0)
        curr_value = float(curr_amt) if curr_amt != "Unknown" else 0.0

        sum_price += price
        sum_boxes += boxes
        sum_spend += spend

        # Comparación MAYOR / MENOR
        if str(ftype).strip().upper() == "MAYOR":
            if curr_value > best_value:
                best_value = curr_value
                selected_order = curr_order
        elif str(ftype).strip().upper() == "MENOR":
            if curr_value < best_value:
                best_value = curr_value
                selected_order = curr_order

    end_time = time.time()

    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'filter_type': ftype,
        'total_count': total_count,
        'selected_order': selected_order,
        'avg_price': sum_price / total_count,
        'avg_boxes': sum_boxes / total_count,
        'avg_spend': sum_spend / total_count
    }

def req_6(catalog, start_date, end_date):
    """
    REQ 6: Identificar el canal con más ventas, mayor recaudación y estadísticas detalladas por canal.
    """
    start_time = time.time()

    orders = catalog['orders'] if isinstance(catalog, dict) and 'orders' in catalog else catalog
    sz = lt.size(orders)
    filtered = lt.new_list()

    # 1. Filtrar órdenes por rango de fechas
    for i in range(sz):
        elem = lt.get_element(orders, i)
        order_date = str(elem.get('Order_Date', ''))
        if start_date <= order_date <= end_date:
            lt.add_last(filtered, elem)

    total_count = lt.size(filtered)

    if total_count == 0:
        end_time = time.time()
        return {
            'elapsed_time_ms': (end_time - start_time) * 1000,
            'total_count': 0,
            'most_used_channel': {'name': "N/A", 'count': 0, 'total_amount': 0.0},
            'most_revenue_channel': {'name': "N/A", 'count': 0, 'total_amount': 0.0},
            'channel_stats': {}
        }

    # 2. Agrupar datos por canal
    channels_dict = {}

    for i in range(total_count):
        order = lt.get_element(filtered, i)
        ch = order.get('Channel', 'Unknown')
        
        price = float(order['Price_per_Box']) if order.get('Price_per_Box') != "Unknown" else 0.0
        spend = float(order['Marketing_Spend']) if order.get('Marketing_Spend') != "Unknown" else 0.0
        amt = float(order['Amount']) if order.get('Amount') != "Unknown" else 0.0

        if ch not in channels_dict:
            channels_dict[ch] = {
                'count': 0,
                'total_amount': 0.0,
                'sum_price': 0.0,
                'count_price': 0,
                'sum_spend': 0.0,
                'count_spend': 0,
                'most_expensive': order,
                'cheapest': order
            }

        st = channels_dict[ch]
        st['count'] += 1
        st['total_amount'] += amt

        if order.get('Price_per_Box') != "Unknown":
            st['sum_price'] += price
            st['count_price'] += 1

        if order.get('Marketing_Spend') != "Unknown":
            st['sum_spend'] += spend
            st['count_spend'] += 1

        # Evaluar pedido más costoso y más barato
        exp_price = float(st['most_expensive'].get('Price_per_Box', 0)) if st['most_expensive'].get('Price_per_Box') != "Unknown" else 0.0
        chp_price = float(st['cheapest'].get('Price_per_Box', 0)) if st['cheapest'].get('Price_per_Box') != "Unknown" else 0.0

        if price > exp_price:
            st['most_expensive'] = order
        if price < chp_price:
            st['cheapest'] = order

    # 3. Determinar Canal Más Usado y Canal de Mayor Recaudación
    mu_name = max(channels_dict, key=lambda k: channels_dict[k]['count'])
    mr_name = max(channels_dict, key=lambda k: channels_dict[k]['total_amount'])

    most_used_channel = {
        'name': mu_name,
        'count': channels_dict[mu_name]['count'],
        'total_amount': channels_dict[mu_name]['total_amount']
    }

    most_revenue_channel = {
        'name': mr_name,
        'count': channels_dict[mr_name]['count'],
        'total_amount': channels_dict[mr_name]['total_amount']
    }

    # 4. Formatear la salida de channel_stats
    channel_stats = {}
    for ch, st in channels_dict.items():
        channel_stats[ch] = {
            'avg_price': (st['sum_price'] / st['count_price']) if st['count_price'] > 0 else 0.0,
            'avg_spend': (st['sum_spend'] / st['count_spend']) if st['count_spend'] > 0 else 0.0,
            'most_expensive': st['most_expensive'],
            'cheapest': st['cheapest']
        }

    end_time = time.time()

    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'most_used_channel': most_used_channel,
        'most_revenue_channel': most_revenue_channel,  # Nombre corregido según la vista
        'channel_stats': channel_stats
    }