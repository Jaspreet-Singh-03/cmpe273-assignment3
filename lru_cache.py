from pickle_hash import serialize,deserialize,hash_code_hex
hash_map = dict()
id_to_node = dict()

class Node:
    def __init__(self,key,data):
        self.key = key
        self.data = data
        self.next = None
        self.prev = None

class DoubleLinkedList:
    def __init__(self):
        self.start = None
        self.end = None
        self.size = 0

    def add(self,node):
        if self.start is None:
            self.start = node
            self.end = node
        else:
            self.end.next = node
            node.prev = self.end
            self.end = node
        hash_map[node.key] = node.data
        self.size = self.size + 1

    def remove(self,node):
        if(self.size>0):
            if node == self.start:
                if self.size>1:
                    self.start = node.next
                    node.next.prev = None
                else:
                    self.start = None
                    self.end = None
            elif node == self.end:
                self.end = node.prev
                node.prev.next = None
            else:
                node.prev.next = node.next
                node.next.prev = node.prev
            node.prev = None
            node.next = None
            del(hash_map[node.key])
            self.size = self.size - 1

    def list_print(self):
        node = self.start
        while node is not None:
            print(node.key)
            print(node.data)
            node = node.next

    def __len__(self):
        return self.size

    def update_node(self, node):
        if len(self) < cache_size:
            self.add(node)
        elif node.key in hash_map:
            self.remove(node)
            self.add(node)
        else:
            self.remove(self.start)
            self.add(node)

cache_size=0
dllist = DoubleLinkedList()
def lru_cache(decorator_args):
    global cache_size
    cache_size = int(decorator_args)
    def wrapper_function(function):
        def inner_function(object):
            if function.__name__== "get":
                node = key_to_node(object)
                if node is not None and hash_map.__contains__(node.key):
                    print("LRU Cached Response")
                    return lru_cache_get(node)
                else:
                    return function(object)

            else:
                return lru_test_put(decorator_args, function, object)
        return inner_function
    return wrapper_function

def lru_test_put(local_size,function,object):
    cache_size = int(local_size)
    name = function.__name__
    key = serialize(object)
    key_hash = hash_code_hex(key)
    if not hash_map.__contains__(key_hash):
        val = function(object)
        node = Node(key_hash, val)
        id_to_node[key_hash] = node
        dllist.update_node(node)
        print(f"{name}({object}) -> {node.data}")
        return val
    else:
        node = id_to_node[key_hash]
        print(f"cache hit, cache size is {cache_size} : {name}({object}) -> {node.data}")
        return node.data

def lru_cache_put(key,value):
    hash_code = key
    envelope_bytes = value
    if not hash_map.__contains__(hash_code):
        node = Node(hash_code, envelope_bytes)
        id_to_node[hash_code] = node
    else:
        node = id_to_node[hash_code]
    dllist.update_node(node)

def lru_cache_get(node):
    data = node.data
    dllist.update_node(node)
    return data, None

def lru_cache_delete(node):
    dllist.remove(node)

def key_to_node(key):
    hash_code = key
    if id_to_node.__contains__(hash_code):
        node = id_to_node[hash_code]
        return node
    else :
        return None


