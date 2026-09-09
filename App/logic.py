import csv
csv.field_size_limit(2147483647)
import time
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sll 

def new_logic():
    """
    Crea el catálogo para almacenar las estructuras de datos.
    """
    catalog = {
        'orders': list_structure.new_list()
    }
    return catalog


def load_data(catalog, filename):
    """
    Carga los datos del reto desde el archivo CSV.
    """
    csv.field_size_limit(2147483647)
    
    start_time = get_time()
    catalog['orders'] = list_structure.new_list()
    
    total_records = 0
    min_amount_order = None
    max_amount_order = None
    
    # 1. Usar 'utf-8-sig' para eliminar el carácter BOM invisible en el primer encabezado
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for raw_row in reader:
            # 2. Limpiar espacios alrededor de las llaves por si acaso
            row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in raw_row.items() if k}
            
            total_records += 1
            
            # Formatear campos y colocar 'Unknown' en vacíos
            order = {
                'Order_ID': row.get('Order_ID') if row.get('Order_ID') else "Unknown",
                'Product': row.get('Product') if row.get('Product') else "Unknown",
                'Country': row.get('Country') if row.get('Country') else "Unknown",
                'Channel': row.get('Channel') if row.get('Channel') else "Unknown",
                'Order_Date': row.get('Order_Date') if row.get('Order_Date') else "Unknown",
                'Discount_Pct': float(row['Discount_Pct']) if row.get('Discount_Pct') else "Unknown",
                'Price_per_Box': float(row['Price_per_Box']) if row.get('Price_per_Box') else "Unknown",
                'Marketing_Spend': float(row['Marketing_Spend']) if row.get('Marketing_Spend') else "Unknown",
                'Boxes_Shipped': int(row['Boxes_Shipped']) if row.get('Boxes_Shipped') else "Unknown",
                'Amount': float(row['Amount']) if row.get('Amount') else "Unknown"
            }
            
            list_structure.add_last(catalog['orders'], order)
            
            
            # Menor Amount (desempate por menor Price_per_Box)
            if min_amount_order is None:
                min_amount_order = order
            elif order['Amount'] != "Unknown" and min_amount_order['Amount'] != "Unknown":
                if order['Amount'] < min_amount_order['Amount']:
                    min_amount_order = order
                elif order['Amount'] == min_amount_order['Amount']:
                    if order['Price_per_Box'] < min_amount_order['Price_per_Box']:
                        min_amount_order = order
                        
            # Mayor Amount (desempate por menor Price_per_Box)
            if max_amount_order is None:
                max_amount_order = order
            elif order['Amount'] != "Unknown" and max_amount_order['Amount'] != "Unknown":
                if order['Amount'] > max_amount_order['Amount']:
                    max_amount_order = order
                elif order['Amount'] == max_amount_order['Amount']:
                    if order['Price_per_Box'] < max_amount_order['Price_per_Box']:
                        max_amount_order = order

    end_time = get_time()
    
    first_5 = []
    last_5 = []
    sz = list_structure.size(catalog['orders'])
    
    if sz > 0:
        # Obtener los primeros 5 elementos (índices 0 a min(5, sz) - 1)
        for i in range(0, min(5, sz)):
            first_5.append(list_structure.get_element(catalog['orders'], i))
            
        # Obtener los últimos 5 elementos (índices max(0, sz - 5) a sz - 1)
        start_index = max(0, sz - 5)
        for i in range(start_index, sz):
            last_5.append(list_structure.get_element(catalog['orders'], i))

    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'total_orders': total_records,
        'min_amount_order': min_amount_order,
        'max_amount_order': max_amount_order,
        'first_5': first_5,
        'last_5': last_5
    }


def req_1(catalog, product_name):
    """
    REQ 1: Promedio de características para un producto específico
    """
    start_time = get_time()
    orders = catalog['orders']
    sz = list_structure.size(orders)
    
    filtered_orders = []
    for i in range(0, sz):
        elem = list_structure.get_element(orders, i)
        if elem['Product'] == product_name:
            filtered_orders.append(elem)
            
    total_count = len(filtered_orders)
    if total_count == 0:
        return {'elapsed_time_ms': delta_time(start_time, get_time()), 'total_count': 0}
        
    prices = [o['Price_per_Box'] for o in filtered_orders if o['Price_per_Box'] != "Unknown"]
    discounts = [o['Discount_Pct'] for o in filtered_orders if o['Discount_Pct'] != "Unknown"]
    boxes = [o['Boxes_Shipped'] for o in filtered_orders if o['Boxes_Shipped'] != "Unknown"]
    spends = [o['Marketing_Spend'] for o in filtered_orders if o['Marketing_Spend'] != "Unknown"]
    
    year_counts = {}
    for o in filtered_orders:
        if o['Order_Date'] != "Unknown":
            year = o['Order_Date'].split("-")[0]
            year_counts[year] = year_counts.get(year, 0) + 1
            
    top_year = max(year_counts, key=year_counts.get) if year_counts else "Unknown"
    
    max_amt_order = filtered_orders[0]
    min_amt_order = filtered_orders[0]
    
    for o in filtered_orders[1:]:
        if o['Amount'] > max_amt_order['Amount']:
            max_amt_order = o
        elif o['Amount'] == max_amt_order['Amount']:
            if o['Marketing_Spend'] < max_amt_order['Marketing_Spend']:
                max_amt_order = o
                
        if o['Amount'] < min_amt_order['Amount']:
            min_amt_order = o
        elif o['Amount'] == min_amt_order['Amount']:
            if o['Marketing_Spend'] < min_amt_order['Marketing_Spend']:
                min_amt_order = o

    end_time = get_time()
    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'total_count': total_count,
        'avg_price': sum(prices)/len(prices) if prices else 0,
        'min_price': min(prices) if prices else 0,
        'max_price': max(prices) if prices else 0,
        'avg_discount': sum(discounts)/len(discounts) if discounts else 0,
        'min_discount': min(discounts) if discounts else 0,
        'max_discount': max(discounts) if discounts else 0,
        'avg_boxes': sum(boxes)/len(boxes) if boxes else 0,
        'min_boxes': min(boxes) if boxes else 0,
        'max_boxes': max(boxes) if boxes else 0,
        'avg_spend': sum(spends)/len(spends) if spends else 0,
        'min_spend': min(spends) if spends else 0,
        'max_spend': max(spends) if spends else 0,
        'top_year': top_year,
        'max_amt_order': max_amt_order,
        'min_amt_order': min_amt_order
    }


def req_2(catalog, min_price, max_price):
    """
    REQ 2: Filtrar pedidos por rango de precio
    """
    start_time = get_time()
    orders = catalog['orders']
    sz = lt.size(orders)
    
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
 
            # Pedido mas reciente (Order_Date mas grande; empate -> mayor Amount)
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
 
    avg_discount = total_discount / count_discount if count_discount > 0 else 0
    avg_spend = total_spend / count_spend if count_spend > 0 else 0
    avg_price = total_price / count_price if count_price > 0 else 0
 
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
    sz = list_structure.size(orders)
    
    filtered = []
    for i in range(0, sz):
        elem = list_structure.get_element(orders, i)
        if elem['Product'] == product and start_date <= elem['Order_Date'] <= end_date:
            filtered.append(elem)
            
    total_count = len(filtered)
    if total_count == 0:
        return {'elapsed_time_ms': delta_time(start_time, get_time()), 'total_count': 0}
        
    avg_price = sum(o['Price_per_Box'] for o in filtered if o['Price_per_Box'] != "Unknown") / total_count
    avg_boxes = sum(o['Boxes_Shipped'] for o in filtered if o['Boxes_Shipped'] != "Unknown") / total_count
    avg_spend = sum(o['Marketing_Spend'] for o in filtered if o['Marketing_Spend'] != "Unknown") / total_count
    
    selected_order = filtered[0]
    for o in filtered[1:]:
        if filter_type.upper() == "MENOR":
            if o['Amount'] < selected_order['Amount']:
                selected_order = o
            elif o['Amount'] == selected_order['Amount']:
                if o['Price_per_Box'] < selected_order['Price_per_Box']:
                    selected_order = o
                elif o['Price_per_Box'] == selected_order['Price_per_Box']:
                    if o['Marketing_Spend'] < selected_order['Marketing_Spend']:
                        selected_order = o
        else:
            if o['Amount'] > selected_order['Amount']:
                selected_order = o
            elif o['Amount'] == selected_order['Amount']:
                if o['Price_per_Box'] < selected_order['Price_per_Box']:
                    selected_order = o
                elif o['Price_per_Box'] == selected_order['Price_per_Box']:
                    if o['Marketing_Spend'] < selected_order['Marketing_Spend']:
                        selected_order = o

    end_time = get_time()
    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'filter_type': filter_type.upper(),
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