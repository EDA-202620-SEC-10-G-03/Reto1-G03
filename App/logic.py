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


def load_data(control, path):
    """
    Carga los datos del archivo CSV en una lista y calcula min, max y primeros/últimos registros.
    """
    start_time = time.time()
    orders = lt.new_list()
    
    min_amount_order = None
    max_amount_order = None
    
    with open(path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lt.add_last(orders, row)
            
            amount_str = row.get('Amount', 'Unknown')
            if amount_str != "Unknown":
                try:
                    amount_val = float(amount_str)
                    row['Amount'] = amount_val # Normalizar a float si es posible
                    
                    # Evaluar mínimo Amount
                    if min_amount_order is None or min_amount_order['Amount'] == "Unknown":
                        min_amount_order = row
                    else:
                        if amount_val < min_amount_order['Amount']:
                            min_amount_order = row
                        elif amount_val == min_amount_order['Amount']:
                            # Desempate por menor Price_per_Box
                            p_curr = float(row.get('Price_per_Box', 0)) if row.get('Price_per_Box') != "Unknown" else float('inf')
                            p_min = float(min_amount_order.get('Price_per_Box', 0)) if min_amount_order.get('Price_per_Box') != "Unknown" else float('inf')
                            if p_curr < p_min:
                                min_amount_order = row

                    # Evaluar máximo Amount
                    if max_amount_order is None or max_amount_order['Amount'] == "Unknown":
                        max_amount_order = row
                    else:
                        if amount_val > max_amount_order['Amount']:
                            max_amount_order = row
                        elif amount_val == max_amount_order['Amount']:
                            # Desempate por menor Price_per_Box
                            p_curr = float(row.get('Price_per_Box', 0)) if row.get('Price_per_Box') != "Unknown" else float('inf')
                            p_max = float(max_amount_order.get('Price_per_Box', 0)) if max_amount_order.get('Price_per_Box') != "Unknown" else float('inf')
                            if p_curr < p_max:
                                max_amount_order = row
                except ValueError:
                    pass

    control['orders'] = orders
    total_orders = lt.size(orders)
    
    first_5 = [lt.get_element(orders, i) for i in range(min(5, total_orders))]
    last_5 = [lt.get_element(orders, i) for i in range(max(0, total_orders - 5), total_orders)]
    
    end_time = time.time()
    
    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_orders': total_orders,
        'min_amount_order': min_amount_order,
        'max_amount_order': max_amount_order,
        'first_5': first_5,
        'last_5': last_5
    }

import time
import DataStructures.List.array_list as lt


def req_1(control, product_name):
    """
    Requerimiento 1: Estadísticas de un producto específico con contadores limpios para 'Unknown'.
    """
    start_time = time.time()
    orders = control['orders']
    sz = lt.size(orders)
    
    filtered = sll.new_list()
    sum_price = sum_disc = sum_boxes = sum_spend = 0.0
    c_p = c_d = c_b = c_s = 0
    
    min_price = float('inf')
    max_price = float('-inf')
    min_disc = float('inf')
    max_disc = float('-inf')
    min_boxes = float('inf')
    max_boxes = float('-inf')
    min_spend = float('inf')
    max_spend = float('-inf')
    
    years_count = {}
    max_amt_order = None
    min_amt_order = None
    
    for i in range(sz):
        o = lt.get_element(orders, i)
        if str(o.get('Product', '')).strip().lower() == str(product_name).strip().lower():
            sll.add_last(filtered, o)
            
            # Price_per_Box
            p_val = o.get('Price_per_Box')
            if p_val != "Unknown" and p_val is not None:
                val = float(p_val)
                sum_price += val
                c_p += 1
                if val < min_price: min_price = val
                if val > max_price: max_price = val
                
            # Discount_Pct
            d_val = o.get('Discount_Pct')
            if d_val != "Unknown" and d_val is not None:
                val = float(d_val)
                sum_disc += val
                c_d += 1
                if val < min_disc: min_disc = val
                if val > max_disc: max_disc = val

            # Boxes_Shipped
            b_val = o.get('Boxes_Shipped')
            if b_val != "Unknown" and b_val is not None:
                val = float(b_val)
                sum_boxes += val
                c_b += 1
                if val < min_boxes: min_boxes = val
                if val > max_boxes: max_boxes = val

            # Marketing_Spend
            m_val = o.get('Marketing_Spend')
            if m_val != "Unknown" and m_val is not None:
                val = float(m_val)
                sum_spend += val
                c_s += 1
                if val < min_spend: min_spend = val
                if val > max_spend: max_spend = val

            # Amount min/max para el producto
            a_val = o.get('Amount')
            if a_val != "Unknown" and a_val is not None:
                aval_f = float(a_val)
                if max_amt_order is None or aval_f > float(max_amt_order.get('Amount', 0)):
                    max_amt_order = o
                if min_amt_order is None or aval_f < float(min_amt_order.get('Amount', 0)):
                    min_amt_order = o

            # Años
            date_str = str(o.get('Order_Date', ''))
            if len(date_str) >= 4:
                yr = date_str[:4]
                years_count[yr] = years_count.get(yr, 0) + 1

    total_count = sll.size(filtered)
    top_year = max(years_count, key=years_count.get) if years_count else "N/A"
    
    end_time = time.time()
    
    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'avg_price': sum_price / c_p if c_p > 0 else 0.0,
        'min_price': min_price if min_price != float('inf') else 0.0,
        'max_price': max_price if max_price != float('-inf') else 0.0,
        'avg_discount': sum_disc / c_d if c_d > 0 else 0.0,
        'min_discount': min_disc if min_disc != float('inf') else 0.0,
        'max_discount': max_disc if max_disc != float('-inf') else 0.0,
        'avg_boxes': sum_boxes / c_b if c_b > 0 else 0.0,
        'min_boxes': min_boxes if min_boxes != float('inf') else 0.0,
        'max_boxes': max_boxes if max_boxes != float('-inf') else 0.0,
        'avg_spend': sum_spend / c_s if c_s > 0 else 0.0,
        'min_spend': min_spend if min_spend != float('inf') else 0.0,
        'max_spend': max_spend if max_spend != float('-inf') else 0.0,
        'top_year': top_year,
        'max_amt_order': max_amt_order,
        'min_amt_order': min_amt_order
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

def req_3(control, country_name, channel_name):
    """
    Requerimiento 3: Filtro por país y canal con promedios y contadores seguros ante 'Unknown'.
    """
    start_time = time.time()
    orders = control['orders']
    sz = lt.size(orders)
    
    sum_price = sum_disc = sum_spend = sum_boxes = 0.0
    c_p = c_d = c_s = c_b = 0
    products_count = {}
    years_count = {}
    total_count = 0
    
    for i in range(sz):
        o = lt.get_element(orders, i)
        c_match = str(o.get('Country', '')).strip().lower() == str(country_name).strip().lower()
        ch_match = str(o.get('Channel', '')).strip().lower() == str(channel_name).strip().lower()
        
        if c_match and ch_match:
            total_count += 1
            
            p_val = o.get('Price_per_Box')
            if p_val != "Unknown" and p_val is not None:
                sum_price += float(p_val)
                c_p += 1
                
            d_val = o.get('Discount_Pct')
            if d_val != "Unknown" and d_val is not None:
                sum_disc += float(d_val)
                c_d += 1
                
            m_val = o.get('Marketing_Spend')
            if m_val != "Unknown" and m_val is not None:
                sum_spend += float(m_val)
                c_s += 1
                
            b_val = o.get('Boxes_Shipped')
            if b_val != "Unknown" and b_val is not None:
                sum_boxes += float(b_val)
                c_b += 1
                
            prod = o.get('Product')
            if prod:
                products_count[prod] = products_count.get(prod, 0) + 1
                
            date_str = str(o.get('Order_Date', ''))
            if len(date_str) >= 4:
                yr = date_str[:4]
                years_count[yr] = years_count.get(yr, 0) + 1

    most_freq_product = max(products_count, key=products_count.get) if products_count else "N/A"
    top_year = max(years_count, key=years_count.get) if years_count else "N/A"
    
    end_time = time.time()
    
    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'avg_price': sum_price / c_p if c_p > 0 else 0.0,
        'avg_discount': sum_disc / c_d if c_d > 0 else 0.0,
        'avg_spend': sum_spend / c_s if c_s > 0 else 0.0,
        'avg_boxes': sum_boxes / c_b if c_b > 0 else 0.0,
        'most_freq_product': most_freq_product,
        'top_year': top_year
    }

def req_4(catalog, product, country):
    """
    REQ 4: Calcula estadísticas promedio y obtiene los 2 pedidos con mayor Amount 
    para una combinación específica de Producto y País, aplicando desempates completos.
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

        # Selección de Top 2 por 'Amount' con desempates completos
        if top_1 is None:
            top_1 = order
        else:
            curr_amt = float(order.get('Amount', 0)) if order.get('Amount') != "Unknown" else 0.0
            top1_amt = float(top_1.get('Amount', 0)) if top_1.get('Amount') != "Unknown" else 0.0

            curr_mkt = float(order.get('Marketing_Spend', 0)) if order.get('Marketing_Spend') != "Unknown" else 0.0
            top1_mkt = float(top_1.get('Marketing_Spend', 0)) if top_1.get('Marketing_Spend') != "Unknown" else 0.0

            curr_id = str(order.get('Order_ID', ''))
            top1_id = str(top_1.get('Order_ID', ''))

            # Evaluación contra top_1: Amount -> Marketing_Spend -> Order_ID
            es_mejor_que_top1 = False
            if curr_amt > top1_amt:
                es_mejor_que_top1 = True
            elif curr_amt == top1_amt:
                if curr_mkt < top1_mkt:
                    es_mejor_que_top1 = True
                elif curr_mkt == top1_mkt:
                    if curr_id < top1_id:
                        es_mejor_que_top1 = True

            if es_mejor_que_top1:
                top_2 = top_1
                top_1 = order
            else:
                # Evaluación contra top_2
                if top_2 is None:
                    top_2 = order
                else:
                    top2_amt = float(top_2.get('Amount', 0)) if top_2.get('Amount') != "Unknown" else 0.0
                    top2_mkt = float(top_2.get('Marketing_Spend', 0)) if top_2.get('Marketing_Spend') != "Unknown" else 0.0
                    top2_id = str(top_2.get('Order_ID', ''))

                    if curr_amt > top2_amt:
                        top_2 = order
                    elif curr_amt == top2_amt:
                        if curr_mkt < top2_mkt:
                            top_2 = order
                        elif curr_mkt == top2_mkt:
                            if curr_id < top2_id:
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
    con desempates triples (Amount -> Price_per_Box -> Marketing_Spend) y promedios exactos.
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

    # 2. Buscar el pedido MAYOR o MENOR según reglas de desempate y sumar promedios
    sum_price = sum_boxes = sum_spend = 0.0
    c_price = c_boxes = c_spend = 0
    selected_order = None

    for i in range(total_count):
        curr_order = lt.get_element(filtered, i)
        
        # Conteo para promedios exactos ignorando "Unknown"
        if curr_order.get('Price_per_Box') != "Unknown":
            sum_price += float(curr_order['Price_per_Box'])
            c_price += 1
        if curr_order.get('Boxes_Shipped') != "Unknown":
            sum_boxes += float(curr_order['Boxes_Shipped'])
            c_boxes += 1
        if curr_order.get('Marketing_Spend') != "Unknown":
            sum_spend += float(curr_order['Marketing_Spend'])
            c_spend += 1

        # Lógica de selección con desempate triple
        if selected_order is None:
            selected_order = curr_order
        else:
            curr_amt = float(curr_order.get('Amount', 0)) if curr_order.get('Amount') != "Unknown" else 0.0
            sel_amt = float(selected_order.get('Amount', 0)) if selected_order.get('Amount') != "Unknown" else 0.0

            curr_price = float(curr_order.get('Price_per_Box', 0)) if curr_order.get('Price_per_Box') != "Unknown" else 0.0
            sel_price = float(selected_order.get('Price_per_Box', 0)) if selected_order.get('Price_per_Box') != "Unknown" else 0.0

            curr_spend = float(curr_order.get('Marketing_Spend', 0)) if curr_order.get('Marketing_Spend') != "Unknown" else 0.0
            sel_spend = float(selected_order.get('Marketing_Spend', 0)) if selected_order.get('Marketing_Spend') != "Unknown" else 0.0

            cambiar = False
            ftype_str = str(ftype).strip().upper()

            if ftype_str == "MAYOR":
                if curr_amt > sel_amt:
                    cambiar = True
                elif curr_amt == sel_amt:
                    if curr_price < sel_price:
                        cambiar = True
                    elif curr_price == sel_price:
                        if curr_spend < sel_spend:
                            cambiar = True
            elif ftype_str == "MENOR":
                if curr_amt < sel_amt:
                    cambiar = True
                elif curr_amt == sel_amt:
                    if curr_price < sel_price:
                        cambiar = True
                    elif curr_price == sel_price:
                        if curr_spend < sel_spend:
                            cambiar = True

            if cambiar:
                selected_order = curr_order

    end_time = time.time()

    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'filter_type': ftype,
        'total_count': total_count,
        'selected_order': selected_order,
        'avg_price': sum_price / c_price if c_price > 0 else 0.0,
        'avg_boxes': sum_boxes / c_boxes if c_boxes > 0 else 0.0,
        'avg_spend': sum_spend / c_spend if c_spend > 0 else 0.0
    }
    
def req_6(control, start_date, end_date):
    """
    Requerimiento 6: Estadísticas por canal protegidas contra valores 'Unknown' en inicializaciones.
    """
    start_time = time.time()
    orders = control['orders']
    sz = lt.size(orders)
    
    channels = {}
    total_count = 0
    
    for i in range(sz):
        o = lt.get_element(orders, i)
        od = str(o.get('Order_Date', ''))
        
        if start_date <= od <= end_date:
            total_count += 1
            ch = o.get('Channel', 'Unknown_Channel')
            
            if ch not in channels:
                channels[ch] = {
                    'count': 0,
                    'total_amount': 0.0,
                    'sum_price': 0.0,
                    'c_price': 0,
                    'sum_spend': 0.0,
                    'c_spend': 0,
                    'most_expensive': None,
                    'cheapest': None
                }
                
            channels[ch]['count'] += 1
            
            # Amount para ingresos
            amt_val = o.get('Amount')
            if amt_val != "Unknown" and amt_val is not None:
                channels[ch]['total_amount'] += float(amt_val)
                
            # Price_per_Box
            p_val = o.get('Price_per_Box')
            if p_val != "Unknown" and p_val is not None:
                p_f = float(p_val)
                channels[ch]['sum_price'] += p_f
                channels[ch]['c_price'] += 1
                
                # Más costoso del canal
                exp = channels[ch]['most_expensive']
                if exp is None or exp.get('Price_per_Box') == "Unknown" or p_f > float(exp.get('Price_per_Box', 0)):
                    channels[ch]['most_expensive'] = o
                    
                # Más barato del canal
                cheap = channels[ch]['cheapest']
                if cheap is None or cheap.get('Price_per_Box') == "Unknown" or p_f < float(cheap.get('Price_per_Box', 0)):
                    channels[ch]['cheapest'] = o

            # Marketing_Spend
            m_val = o.get('Marketing_Spend')
            if m_val != "Unknown" and m_val is not None:
                channels[ch]['sum_spend'] += float(m_val)
                channels[ch]['c_spend'] += 1

    channel_stats = {}
    most_used_channel = {'name': 'N/A', 'count': 0, 'total_amount': 0.0}
    most_revenue_channel = {'name': 'N/A', 'count': 0, 'total_amount': -1.0}
    
    for ch, data in channels.items():
        c_p = data['c_price']
        c_s = data['c_spend']
        
        channel_stats[ch] = {
            'avg_price': data['sum_price'] / c_p if c_p > 0 else 0.0,
            'avg_spend': data['sum_spend'] / c_s if c_s > 0 else 0.0,
            'most_expensive': data['most_expensive'],
            'cheapest': data['cheapest']
        }
        
        if data['count'] > most_used_channel['count']:
            most_used_channel = {'name': ch, 'count': data['count'], 'total_amount': data['total_amount']}
            
        if data['total_amount'] > most_revenue_channel['total_amount']:
            most_revenue_channel = {'name': ch, 'count': data['count'], 'total_amount': data['total_amount']}

    end_time = time.time()
    
    return {
        'elapsed_time_ms': (end_time - start_time) * 1000,
        'total_count': total_count,
        'most_used_channel': most_used_channel,
        'most_revenue_channel': most_revenue_channel,
        'channel_stats': channel_stats
    }