import math
from bitarray import bitarray
from pickle_hash import serialize,hash_code_hex

class BloomFilter(object):

    def __init__(self,NUM_KEYS,FALSE_POSITIVE_PROBABILITY):
        self.size = NUM_KEYS
        self.fpp = FALSE_POSITIVE_PROBABILITY
        self.num0fHashes = 3
        self.array_size = int ( - (self.size * math.log(self.fpp)) / math.pow(math.log(2),2))
        self.bitArray = bitarray(self.array_size)
        self.bitArray.setall(0)

    def add(self,key):
        data = serialize(key)
        for hash in range(self.num0fHashes):
            location = hash_code_hex(data)
            data = serialize(location)
            location = int(location,16) % self.array_size
            self.bitArray[location]=1

    def is_member(self,key):
        data = serialize(key)
        for hash in range(self.num0fHashes):
            location = hash_code_hex(data)
            data = serialize(location)
            location = int(location,16) % self.array_size
            if self.bitArray[location]==0:
                    return False
        return True

bf = BloomFilter(1000000,0.08)
print(bf.array_size)