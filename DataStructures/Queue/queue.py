from DataStructures.List import array_list as lt

def new_queue():
    return lt.new_list()

def enqueue(my_queue, element):
    lt.add_last(my_queue, element)
    return my_queue

def dequeue(my_queue):
    if lt.is_empty(my_queue):
        raise Exception('EmptyStructureError: queue is empty')
    
    # remove_first elimina el primer elemento y reduce el 'size' en la lista interna
    element = lt.remove_first(my_queue)
    return element

def peek(my_queue):
    if lt.is_empty(my_queue):
        raise Exception('EmptyStructureError: queue is empty')
    return lt.first_element(my_queue)

def is_empty(my_queue):
    return lt.is_empty(my_queue)

def size(my_queue):
    return lt.size(my_queue)