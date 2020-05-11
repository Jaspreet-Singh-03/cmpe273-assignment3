# cmpe273-assignment3
CMPE 273 Assignment 3 (Spring 2020)

### Question What are the best k hashes and m bits values to store one million n keys (E.g. e52f43cd2c23bb2e6296153748382764) suppose we use the same MD5 hash key from pickle_hash.py and explain why?

Solution : So , I reserached and found a really good paper on it http://web.eecs.utk.edu/~jplank/plank/classes/cs494/494/notes/Bloom-Filter/index.html , we first have to decide on the length of bitarray to be used and it is dependent on the estimated number of keys to be inserted and the level of false positive acceptable to the client. Now, how to flase positive are related with k hash functions , the answer is that although higher the number of hash functions used will fill up the bitarray more quickly. However, the trade-off is that when the table isn't full, each additional hash function lowers the probability of a false positive, and we have to decide the level of false positive acceptable and other constraints to decide.

### For example, if key = 1 million (fixed), Using k=3 and false positive rate 0.01 the value of m is 9585058 and if we change like k =2 and false positive 0.08 the value of m is 5256973 which is about 54% of previous m value, so we can decide the k hashes, m bits and n keys which will mimize the error rate.  

## Solution for the program 
- added delete operation in pickle_hash , and currently putting all the requests -> getting the request -> deleting the request with sucess message.

- added lru_cache decorator is used in **cache_client.py** for get operation as per the assignment requirements with initial size of 5, so for managing the size please change the parameter there.

- added bloomfilter in **cache_client.py** with num of keys 100 and with same hash used 3 times and false probabilty rate 0.05 , bitarray size is calculated as per formula provided.

### Test Output 
<img src="https://github.com/Jaspreet-Singh-03/cmpe273-assignment3/blob/master/Program%20Outputs/Test%20Output.jpg" height="800">

### Program Output 
<img src="https://github.com/Jaspreet-Singh-03/cmpe273-assignment3/blob/master/Program%20Outputs/Client%20Output.jpg" height="800">


