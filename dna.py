from re import S
import cv2
import numpy as np
import random   
import string  
import secrets
import os
import binascii
from x25519 import base_point_mult,multscalar,bytes_to_int,int_to_bytes
from dna_operation import dna,dna_sub
from encoder import *
from decoder import *
from shift import *
#Read image
img = cv2.imread("Lenna.png")

#Private key

ra_priv = os.urandom(32)
rb_priv = os.urandom(32)
ga_priv = os.urandom(32)
gb_priv = os.urandom(32)
ba_priv = os.urandom(32)
bb_priv = os.urandom(32)
#Public key
ra_pub = base_point_mult(ra_priv)
rb_pub = base_point_mult(rb_priv)
ga_pub = base_point_mult(ga_priv)
gb_pub = base_point_mult(gb_priv)
bb_pub = base_point_mult(bb_priv)
ba_pub = base_point_mult(ba_priv)
#Shared key
shared_ra = multscalar(ra_priv, rb_pub) # a (bG)
shared_rb = multscalar(rb_priv, ra_pub) # b (aG)
shared_ga = multscalar(ga_priv, gb_pub)
shared_gb = multscalar(gb_priv, ga_pub)
shared_ba = multscalar(ba_priv, rb_pub)
shared_bb = multscalar(bb_priv, ra_pub)

shift_address = {0:"DR",1:"D",2:"DL",3:"L",4:"UL",5:"U",6:"UR",7:"R"}
shift_direction = {"R":shift_array_right,"L":shift_array_left,"U":shift_array_up,"D":shift_array_down}

# def write_keys_to_file(file_name: str,key_a: str,key_b: str):
#     with open(file_name,"w") as f:
#         f.write(key_a)
#         f.write("\n")
#         f.write(key_b)
#         f.write("\n")






#deinterleave dna
def deinterleave_dna(b_dna,g_dna,r_dna):
    m,n = b_dna.shape
    b_dna_deinterleaved = np.zeros(shape=(b_dna.shape[0],b_dna.shape[1]),dtype="object")
    g_dna_deinterleaved = np.zeros(shape=(g_dna.shape[0],g_dna.shape[1]),dtype="object")
    r_dna_deinterleaved = np.zeros(shape=(r_dna.shape[0],r_dna.shape[1]),dtype="object")
    # for i in range(m):
    for j in range(n):
        if j%3==0:
            b_dna_deinterleaved[:,j] = b_dna[:,j]
            g_dna_deinterleaved[:,j] = g_dna[:,j]
            r_dna_deinterleaved[:,j] = r_dna[:,j]
        elif j%3==1:
            b_dna_deinterleaved[:,j] = g_dna[:,j]
            g_dna_deinterleaved[:,j] = r_dna[:,j]
            r_dna_deinterleaved[:,j] = b_dna[:,j]
        else:
            b_dna_deinterleaved[:,j] = r_dna[:,j]
            g_dna_deinterleaved[:,j] = b_dna[:,j]
            r_dna_deinterleaved[:,j] = g_dna[:,j]

    return b_dna_deinterleaved,g_dna_deinterleaved,r_dna_deinterleaved


inverse_shift_direction = {"R":shift_array_left,"L":shift_array_right,"U":shift_array_down,"D":shift_array_up}

def inverse_shift_array_with_octal_sequece(array: np.ndarray,shift_sequence: str,shared_key: str):
    shared_key = bytes_to_int(binascii.hexlify(shared_key.encode()))
    shift_order = [shift_address[int(num)] for num in shift_sequence]
    index = len(shift_order)-1
    shift_order = reversed(shift_order)

    for shift in shift_order:
        for direction in reversed(shift):
            array = inverse_shift_direction[direction](array,int(str(shared_key)[index:index+2]))
        index = index -1
    return array

#Step 3
def dna_subtraction(b_dec,g_dec,r_dec):
    b,g,r = b_dec,g_dec,r_dec
    m,n = b_dec.shape
    b_dna= np.zeros(shape=(b.shape[0],b.shape[1]),dtype="object")
    g_dna = np.zeros(shape=(g.shape[0],g.shape[1]),dtype="object")
    r_dna = np.zeros(shape=(r.shape[0],r.shape[1]),dtype="object")

    for i in range(m):
        for j in range(n):
            b_dna[i,j] = dna_sub["{0}{1}".format(g[i,j][0],b[i,j][0])]+dna_sub["{0}{1}".format(g[i,j][1],b[i,j][1])]+dna_sub["{0}{1}".format(g[i,j][2],b[i,j][2])]+dna_sub["{0}{1}".format(g[i,j][3],b[i,j][3])]
            g_dna[i,j] = dna_sub["{0}{1}".format(b_dna[i,j][0],g[i,j][0])]+dna_sub["{0}{1}".format(b_dna[i,j][1],g[i,j][1])]+dna_sub["{0}{1}".format(b_dna[i,j][2],g[i,j][2])]+dna_sub["{0}{1}".format(b_dna[i,j][3],g[i,j][3])]
            r_dna[i,j] = dna_sub["{0}{1}".format(g_dna[i,j][0],r[i,j][0])]+dna_sub["{0}{1}".format(g_dna[i,j][1],r[i,j][1])]+dna_sub["{0}{1}".format(g_dna[i,j][2],r[i,j][2])]+dna_sub["{0}{1}".format(g_dna[i,j][3],r[i,j][3])]
            
    b_dna = b_dna.astype(str)
    g_dna = g_dna.astype(str)
    r_dna = r_dna.astype(str)
    return b_dna,g_dna,r_dna




if __name__ == "__main__":
    b,g,r = split_image_into_channel(img)

    b_enc,g_enc,r_enc = encode_to_dna(b,g,r)
    
    b_dna,g_dna,r_dna = dna_addition(b_enc,g_enc,r_enc)

    shift_sequence_b = generate_random_octal_sequence()
    shift_sequence_g = generate_random_octal_sequence()
    shift_sequence_r = generate_random_octal_sequence()
    b_shift = shift_array_with_octal_sequece(b_dna,shift_sequence_b,shared_ba)
    g_shift = shift_array_with_octal_sequece(g_dna,shift_sequence_g,shared_ga)
    r_shift = shift_array_with_octal_sequece(r_dna,shift_sequence_r,shared_ra)
    

    b_dna_interleaved,g_dna_interleaved,r_dna_interleaved = interleave_dna(b_shift,g_shift,r_shift)

    b_bin = dna_to_binary(b_dna_interleaved)
    g_bin = dna_to_binary(g_dna_interleaved)
    r_bin = dna_to_binary(r_dna_interleaved)


    b_int = binary_to_int(b_bin)
    g_int = binary_to_int(g_bin)
    r_int = binary_to_int(r_bin)
    
    image = np.dstack((b_int,g_int,r_int))
    image = image.astype(np.uint8)

    # cv2.imshow("Image",image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite("encoded_image.jpg",image)

    #Decoder
    b,g,r = split_image_into_channel(image)
    b_dec,g_dec,r_dec = encode_to_dna(b,g,r)
    b_deinterleaved,g_deinterleaved,r_deinterleaved = deinterleave_dna(b_dec,g_dec,r_dec)

    #invershift
    b_shift = inverse_shift_array_with_octal_sequece(b_deinterleaved, shift_sequence_b, shared_ba)
    g_shift = inverse_shift_array_with_octal_sequece(g_deinterleaved, shift_sequence_g, shared_ga)
    r_shift = inverse_shift_array_with_octal_sequece(r_deinterleaved, shift_sequence_r, shared_ra)

    b_dna,g_dna,r_dna = dna_subtraction(b_shift,g_shift,r_shift)
    print("b_dna {0}".format(b_dna))

    b_dna_binary = dna_to_binary(b_dna)
    g_dna_binary = dna_to_binary(g_dna)
    r_dna_binary = dna_to_binary(r_dna)
    print(b_dna_binary[:10,:10])

    b_dna_int = binary_to_int(b_dna_binary)
    g_dna_int = binary_to_int(g_dna_binary)
    r_dna_int = binary_to_int(r_dna_binary)
    print(b_dna_int[:10,:10])

    image = np.dstack((b_dna_int,g_dna_int,r_dna_int))
    image = image.astype(np.uint8)
    cv2.imshow("Image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
