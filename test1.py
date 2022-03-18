import os
import binascii
from x25519 import base_point_mult,multscalar,bytes_to_int,int_to_bytes


a = os.urandom(32)
b = os.urandom(32)
# a = int_to_bytes(10,32) # just for testing a=10 (32 bytes - 256 bits)
# b = int_to_bytes(12,32) # just for testing b=12 (32 bytes - 256 bits)

print (f"\n\nBob private (b):\t{bytes_to_int(b)}")
print (f"Alice private (a): \t{bytes_to_int(a)}")



# Traditional ECDH: 
a_pub = base_point_mult(a)
b_pub = base_point_mult(b)

print ("\n\nBob public (bG):\t",binascii.hexlify(b_pub.encode()))

print ("Alice public (aG):\t",binascii.hexlify(a_pub.encode()))

k_a = multscalar(a, b_pub) # a (bG)
k_b = multscalar(b, a_pub) # b (aG)

# print(type(k_a),type)
print ("\n\nBob shared (b)aG:\t",binascii.hexlify(k_b.encode()))
print ("Alice shared (a)bG:\t",binascii.hexlify(k_a.encode()))

ai = bytes_to_int(binascii.hexlify(k_a.encode()))
bi = bytes_to_int(binascii.hexlify(k_b.encode()))
print(ai)
print(bi)
print(int(str(ai)[:2]))
print(int(str(bi)[:2]))