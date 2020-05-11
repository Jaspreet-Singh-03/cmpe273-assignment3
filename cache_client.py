import sys
import socket
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from node_ring import NodeRing
from lru_cache import lru_cache , lru_cache_put
from bloom_filter import BloomFilter

NUM_KEYS = 100
FALSE_POSITIVE_PROBABILITY = 0.05
bloomfilter = BloomFilter(NUM_KEYS,FALSE_POSITIVE_PROBABILITY)

BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

@lru_cache(5)
def get(key):
    if bloomfilter.is_member(key):
        return serialize_GET(key)
    else:
        return None , None

def put(key,value):
    bloomfilter.add(key)
    lru_cache_put(key,value)

def delete(key):
    if bloomfilter.is_member(key):
        return serialize_DELETE(key)
    else:
        return None , None

def process(udp_clients):
    client_ring = NodeRing(udp_clients)
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        put(key,data_bytes)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)
        hash_codes.add(str(response.decode()))

    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")

     # GET all users.
    for hc in hash_codes:
        data_bytes, key = get(hc)
        if key is None:
            if data_bytes is None:
                response = None
            else :
                response = data_bytes
        else:
            response = client_ring.get_node(key).send(data_bytes)
            lru_cache_put(key,data_bytes)
        print(response)

    for hc in hash_codes:
        data_bytes, key = delete(hc)
        if data_bytes is not None:
            response = client_ring.get_node(key).send(data_bytes)
        else:
            response = "Key not Present"
        print(response)

if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)
