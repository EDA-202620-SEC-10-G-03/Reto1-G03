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



def req_3(catalog, country="any", channel="any"):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    pedidos = lt.new_list()
    
    
    prom_product = lt.new_list()
    count_product = lt.new_list()
    prom_order_date = lt.new_list()
    count_order_date = lt.new_list()
    prom_discount_pct = 0
    prom_price_per_box = 0
    prom_marketing_spend = 0
    prom_boxes_shipped = 0
    prom_amount = 0

    
    if not country == "any" and not channel == "any":
        
        for posicion in range(catalog["country"]["size"]):
            if lt.get_element(catalog["country"], posicion-1) == country:
                pedido = lt.new_list()
                order_id = lt.get_element(catalog["order_id"], (posicion-1))
                product = lt.get_element(catalog["product"], (posicion-1))
                order_date = lt.get_element(catalog["order_date"], (posicion-1))
                discount_pct = lt.get_element(catalog["discount_pct"], (posicion-1))
                price_per_box = lt.get_element(catalog["price_per_box"], (posicion-1))
                marketing_spend = lt.get_element(catalog["marketing_spend"], (posicion-1))
                boxes_shipped = lt.get_element(catalog["boxes_shipped"], (posicion-1))
                amount = lt.get_element(catalog["amount"], (posicion-1))
                
                if lt.is_present(prom_product, product) == -1:
                    lt.add_last(prom_product)
                    lt.add_last(count_product, 1)
                else:
                    pos = lt.is_present(prom_product, product)
                    lt.change_info(prom_product, pos, (lt.get_element(prom_product, pos) + 1))
                
                if lt.is_present(prom_order_date) == -1:
                    lt.add_last(prom_order_date , order_date)
                    lt.add_last(count_order_date, 1)
                else:
                    pos = lt.is_present(prom_order_date, order_date)
                    lt.change_info(prom_order_date, pos, (lt.get_element(prom_order_date, pos) + 1))
                
                
                prom_discount_pct += discount_pct
                prom_price_per_box += price_per_box
                prom_marketing_spend += marketing_spend
                prom_boxes_shipped += boxes_shipped
                prom_amount += amount
                lt.add_last(pedido, order_id)
                lt.add_last(pedidos, pedido)
    
    tamano = lt.size(pedidos)
    
    more_product = 0
    more_order_date = 0
    for x in range(tamano):
        if lt.get_element(count_order_date, (x-1)) > more_order_date:
            more_order_date = lt.get_element(count_order_date, (x-1))
        if lt.get_element(count_product, (x-1)) > more_product:
            more_product = lt.get_element(count_product, (x-1))
            
    
    variable_final = {
    "total_orders": tamano,
    "prom_product": lt.get_element(prom_product, lt.is_present(count_product, more_product)),
    "prom_order_date": lt.get_element(prom_order_date, lt.is_present(count_order_date, more_order_date)) ,
    "prom_discount_pct": prom_discount_pct / tamano,
    "prom_price_per_box": prom_price_per_box / tamano,
    "prom_marketing_spend": prom_marketing_spend / tamano,
    "prom_boxes_shipped": prom_boxes_shipped / tamano,
    "prom_amount": prom_amount / tamano,                
              
    }

    
    end_time = get_time()
    dif = delta_time(start_time, end_time)
    variable_final["time"]= dif
    return  variable_final

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
import time

import time

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