from DataStructures.List import list_node as ln


def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size" : 0,
    }
    
    return newlist

def add_first(my_list, element):
    nodo = ln.new_single_node(element)
    
    if my_list["size"] == 0:
        my_list["first"] = nodo
        my_list["last"] = nodo
    else:
        nodo["next"] = my_list["first"]
        my_list["first"] = nodo
    my_list["size"] += 1
    
    return my_list

def add_last(my_list, element):
    nodo = ln.new_single_node(element)
    
    if my_list["size"] == 0:
        my_list["first"] = nodo
        my_list["last"] = nodo
    else:
        my_list["last"]["next"] = nodo
        my_list["last"] = nodo

    my_list["size"] += 1
    return my_list



def first_element(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    else:
       return my_list["first"]["info"]
   

def is_empty(my_list):
    if my_list["size"] == 0:
        return True
    else:
        return False
   

def size(my_list):
    return my_list["size"]


def last_element(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    else:
        return my_list["last"]["info"]


def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception('IndexError: list index out of range')
    else:
        if pos == 0:
            my_list["first"] = my_list ["first"]["next"]
        else:
            anterior = my_list["first"]
            for i in range(pos-1):
                anterior = anterior["next"]
            anterior["next"] = anterior["next"]["next"]
        my_list["size"] = my_list["size"] - 1
    return my_list


def remove_first(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    else:
        eliminado = my_list["first"]["info"]
        my_list["first"] = my_list["first"]["next"]
        my_list["size"] = my_list["size"] -1
        return eliminado


def remove_last(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    else:
        eliminado = my_list["last"]["info"]
        anterior = my_list["first"]
        for i in range(my_list["size"] - 2):
            anterior = anterior["next"]
        anterior["next"] = None
        my_list["last"] = anterior
        my_list["size"] = my_list["size"] -1
        return eliminado


def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list["size"]:
        raise Exception('IndexError: list index out of range')
    else:
        nodo = ln.new_single_node(element)
        if pos == 0:
            nodo["next"] = my_list["first"]
            my_list["first"] = nodo
            if my_list["size"] == 0:
                my_list["last"] = nodo
        else:
            anterior = my_list["first"]
            for i in range(pos - 1):
                anterior = anterior["next"]
            nodo["next"] = anterior["next"]
            anterior["next"] = nodo
            if nodo["next"] is None:
                my_list["last"] = nodo
        my_list["size"] += 1
        return my_list
    
def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception('IndexError: list index out of range')
    else:
        actual = my_list["first"]
        for i in range(pos):
            actual = actual["next"]
        actual["info"] = new_info
        return my_list

def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 >= my_list["size"]) or (pos_2 < 0 or pos_2 >= my_list["size"]):
        raise Exception('IndexError: list index out of range')
    else:
        nodo_1 = my_list["first"]
        for i in range(pos_1):
            nodo_1 = nodo_1["next"]

        nodo_2 = my_list["first"]
        for i in range(pos_2):
            nodo_2 = nodo_2["next"]
            
        primera = nodo_1["info"]
        segunda = nodo_2["info"]
        nodo_2["info"] = primera
        nodo_1["info"] = segunda

        return my_list
    
def sub_list(my_list, pos, num_elements):
    if pos + num_elements > my_list["size"]: # Si los elementos uqe quieremos agregar superan el tamaño de la lista error.
        raise IndexError("List out of range")

    mi_sub_lista =  {"first":None,"last":None,"size":0} #esta es nuestra sublista que vamos a retornar
    cuantos_nodos = 0 # contamos cuantos nodos para saber hasta donde llegamos en pos para agregar el ultimo valor de pos 
    llegue_al_ultimo = my_list["first"]
    while cuantos_nodos < pos and llegue_al_ultimo != None:
          llegue_al_ultimo = llegue_al_ultimo["next"]
          cuantos_nodos += 1
    
    agregados = 0
    while agregados < num_elements and llegue_al_ultimo != None:
          copia_nodo = {"info": llegue_al_ultimo["info"], "next": None}
          if mi_sub_lista["first"] == None:
              mi_sub_lista["first"] = copia_nodo
              mi_sub_lista["last"] = copia_nodo
          else:
              mi_sub_lista["last"]["next"] = copia_nodo
              mi_sub_lista["last"] = copia_nodo

          mi_sub_lista["size"] += 1
          llegue_al_ultimo = llegue_al_ultimo["next"]
          agregados += 1

    return mi_sub_lista    




def get_element(my_list, pos):
    searchpos = 0
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos += 1
    return node["info"]

def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True
        else:
            temp = temp["next"]
            count += 1

    if not is_in_array:
        count = -1
    return count