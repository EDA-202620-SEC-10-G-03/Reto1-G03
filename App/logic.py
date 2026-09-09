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
    sz = list_structure.size(orders)
    
    filtered = []
    for i in range(0, sz):
        elem = list_structure.get_element(orders, i)
        if elem['Price_per_Box'] != "Unknown" and min_price <= elem['Price_per_Box'] <= max_price:
            filtered.append(elem)
            
    total_count = len(filtered)
    if total_count == 0:
        return {'elapsed_time_ms': delta_time(start_time, get_time()), 'total_count': 0}
        
    avg_discount = sum(o['Discount_Pct'] for o in filtered if o['Discount_Pct'] != "Unknown") / total_count
    avg_spend = sum(o['Marketing_Spend'] for o in filtered if o['Marketing_Spend'] != "Unknown") / total_count
    avg_price = sum(o['Price_per_Box'] for o in filtered if o['Price_per_Box'] != "Unknown") / total_count
    
    most_recent = filtered[0]
    for o in filtered[1:]:
        if o['Order_Date'] > most_recent['Order_Date']:
            most_recent = o
        elif o['Order_Date'] == most_recent['Order_Date']:
            if o['Amount'] > most_recent['Amount']:
                most_recent = o
                
    min_amt = filtered[0]
    max_amt = filtered[0]
    for o in filtered[1:]:
        if o['Amount'] < min_amt['Amount']:
            min_amt = o
        elif o['Amount'] == min_amt['Amount']:
            if o['Price_per_Box'] < min_amt['Price_per_Box']:
                min_amt = o
                
        if o['Amount'] > max_amt['Amount']:
            max_amt = o
        elif o['Amount'] == max_amt['Amount']:
            if o['Price_per_Box'] < max_amt['Price_per_Box']:
                max_amt = o

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
    
    filtered = []
    for i in range(0, sz):
        elem = list_structure.get_element(orders, i)
        if elem['Country'] == country and elem['Channel'] == channel:
            filtered.append(elem)
            
    total_count = len(filtered)
    if total_count == 0:
        return {'elapsed_time_ms': delta_time(start_time, get_time()), 'total_count': 0}
        
    avg_price = sum(o['Price_per_Box'] for o in filtered if o['Price_per_Box'] != "Unknown") / total_count
    avg_discount = sum(o['Discount_Pct'] for o in filtered if o['Discount_Pct'] != "Unknown") / total_count
    avg_spend = sum(o['Marketing_Spend'] for o in filtered if o['Marketing_Spend'] != "Unknown") / total_count
    avg_boxes = sum(o['Boxes_Shipped'] for o in filtered if o['Boxes_Shipped'] != "Unknown") / total_count
    
    product_counts = {}
    year_counts = {}
    for o in filtered:
        p = o['Product']
        product_counts[p] = product_counts.get(p, 0) + 1
        
        if o['Order_Date'] != "Unknown":
            y = o['Order_Date'].split("-")[0]
            year_counts[y] = year_counts.get(y, 0) + 1
            
    most_freq_product = max(product_counts, key=product_counts.get) if product_counts else "Unknown"
    top_year = max(year_counts, key=year_counts.get) if year_counts else "Unknown"
    
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
    
    filtered = []
    for i in range(0, sz):
        elem = list_structure.get_element(orders, i)
        if elem['Product'] == product and elem['Country'] == country:
            filtered.append(elem)
            
    total_count = len(filtered)
    if total_count == 0:
        return {'elapsed_time_ms': delta_time(start_time, get_time()), 'total_count': 0}
        
    avg_price = sum(o['Price_per_Box'] for o in filtered if o['Price_per_Box'] != "Unknown") / total_count
    avg_discount = sum(o['Discount_Pct'] for o in filtered if o['Discount_Pct'] != "Unknown") / total_count
    avg_spend = sum(o['Marketing_Spend'] for o in filtered if o['Marketing_Spend'] != "Unknown") / total_count
    avg_boxes = sum(o['Boxes_Shipped'] for o in filtered if o['Boxes_Shipped'] != "Unknown") / total_count
    
    def sort_key(o):
        return (o['Amount'], -o['Marketing_Spend'], -int(o['Order_ID'].replace("ORD", "") if o['Order_ID'].startswith("ORD") else o['Order_ID']))
        
    sorted_orders = sorted(filtered, key=sort_key, reverse=True)
    top_2 = sorted_orders[:2]
    
    end_time = get_time()
    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'total_count': total_count,
        'avg_price': avg_price,
        'avg_discount': avg_discount,
        'avg_spend': avg_spend,
        'avg_boxes': avg_boxes,
        'top_2': top_2
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
    REQ 6: Identificar el canal con más ventas y mayor recaudación en un rango de tiempo
    """
    start_time = get_time()
    orders = catalog['orders']
    sz = list_structure.size(orders)
    
    filtered = []
    for i in range(0, sz):
        elem = list_structure.get_element(orders, i)
        if start_date <= elem['Order_Date'] <= end_date:
            filtered.append(elem)
            
    total_count = len(filtered)
    if total_count == 0:
        return {'elapsed_time_ms': delta_time(start_time, get_time()), 'total_count': 0}
        
    channel_data = {}
    for o in filtered:
        ch = o['Channel']
        if ch not in channel_data:
            channel_data[ch] = {'orders': [], 'total_amount': 0.0, 'count': 0}
        channel_data[ch]['orders'].append(o)
        channel_data[ch]['total_amount'] += o['Amount']
        channel_data[ch]['count'] += 1
        
    most_used_channel = max(channel_data, key=lambda k: channel_data[k]['count'])
    most_revenue_channel = max(channel_data, key=lambda k: channel_data[k]['total_amount'])
    
    channel_stats = {}
    for ch, data in channel_data.items():
        ch_orders = data['orders']
        avg_price = sum(o['Price_per_Box'] for o in ch_orders) / len(ch_orders)
        avg_spend = sum(o['Marketing_Spend'] for o in ch_orders) / len(ch_orders)
        most_expensive = max(ch_orders, key=lambda o: o['Amount'])
        cheapest = min(ch_orders, key=lambda o: o['Amount'])
        
        channel_stats[ch] = {
            'avg_price': avg_price,
            'avg_spend': avg_spend,
            'most_expensive': most_expensive,
            'cheapest': cheapest
        }

    end_time = get_time()
    return {
        'elapsed_time_ms': delta_time(start_time, end_time),
        'total_count': total_count,
        'most_used_channel': {
            'name': most_used_channel,
            'count': channel_data[most_used_channel]['count'],
            'total_amount': channel_data[most_used_channel]['total_amount']
        },
        'most_revenue_channel': {
            'name': most_revenue_channel,
            'count': channel_data[most_revenue_channel]['count'],
            'total_amount': channel_data[most_revenue_channel]['total_amount']
        },
        'channel_stats': channel_stats
    }


def get_time():
    """
    Devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter() * 1000)


def delta_time(start, end):
    """
    Devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    return float(end - start)