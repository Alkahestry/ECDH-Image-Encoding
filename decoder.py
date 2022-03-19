from re import S
import cv2
import numpy as np
import random   
import string  
import secrets
import os
import binascii
from x25519 import base_point_mult,multscalar,bytes_to_int,int_to_bytes

#Read image
img = cv2.imread("encoded_image1.jpg")

ra_priv = b'\x96\xa4g7\x9d-\xc4Y\x88\x82\xa6\x87\xd5\xd4\xd0\x9f\xbb\xef\x16E5X\x98\xb8.\x0c>\xff\xabM\xec\xdf'
rb_priv =  b'. \x00\xd4?/\x0cF\x1f\x03|\x82\x93\xe5\x84O\xe9\xe1\x87\xaa(\xd7\\A1\xcd\xd7\xdf\x93\xd2\xaf5'
ga_priv = b'9\xa3`\xc0\xea<\xc5\xc3\x8b^\xacRc\x0c\xf6\x132\xef\xa2\x9a\x8d^\xf9\xab1C?\x94\xc6W0U'
gb_priv = b'^\x160\xeb\xf9\xc1\xe6\x8c`\x1f\xc2\x00\xff\x19\x8e7\x17:u1?k\xd4\xaa\x1aAg\x12m\xa1e\xe2'
bb_priv = b'\xc7\xa8\xd4m!\xb2;\\\x15AR$\xc2)\x84\xecI\xe8\xf6\xacD-v\xa7\x18c\x7f\x81\xfd\xfa\xe9\xaf'
ba_priv = b'\xc5skO@]c\x11\xfa\xaa\xae\xcb|7w\xbc\xaep\xdc\x01\x0b\x05\x14\xab\xd3\xc2:\xcb\xd2R\xbc\x16'

ra_pub = base_point_mult(ra_priv)
rb_pub = base_point_mult(rb_priv)
ga_pub = base_point_mult(ga_priv)
gb_pub = base_point_mult(gb_priv)
bb_pub = base_point_mult(bb_priv)
ba_pub = base_point_mult(ba_priv)

shared_ra = multscalar(ra_priv, rb_pub) # a (bG)
shared_rb = multscalar(rb_priv, ra_pub) # b (aG)
shared_ga = multscalar(ga_priv, gb_pub)
shared_gb = multscalar(gb_priv, ga_pub)
shared_ba = multscalar(ba_priv, rb_pub)
shared_bb = multscalar(bb_priv, ra_pub)

shift_sequence_b = '020726307637632'
shift_sequence_g =  '570456632277222'
shift_sequence_r = '351115474513050'
#DNA-Encoding RULE #1 A = 00, C=01, G=10, T=11
dna = {}
dna["00"] = "A"
dna["01"] = "C"
dna["10"] = "G"
dna["11"] = "T"
dna["A"] = "00"
dna["C"] = "01"
dna["G"] = "10"
dna["T"] = "11"

#DNA subtraction
dna["GG"]=dna["CC"]=dna["AA"]=dna["TT"]="A"
dna["CA"]=dna["AT"]=dna["GC"]=dna["TG"]="C"
dna["GA"]=dna["CT"]=dna["TC"]=dna["AG"]="G"
dna["TA"]=dna["GT"]=dna["AC"]=dna["CG"]="T"
# dna["GG"]=dna["CC"]=dna["AA"]=dna["TT"]="A"
# dna["AC"]=dna["TA"]=dna["CG"]=dna["GT"]="C"
# dna["AG"]=dna["TC"]=dna["CT"]=dna["GA"]="G"
# dna["AT"]=dna["TG"]=dna["CA"]=dna["GC"]="T"
#Split image into RGB channels
def split_image_into_channel(img: np.ndarray):
    b,g,r = cv2.split(img)
    return b,g,r

#Bin string to dna
def bin_to_dna(bin:str):
    dna_enc = ""
    for i in range(0,len(bin),2):
        dna_enc += dna["{0}{1}".format(bin[i],bin[i+1])]
    return dna_enc

def process(b,g,r):
    #iterate through each pixel
    # for array in (b,g,r):
    b_bin = np.zeros(shape=(b.shape[0],b.shape[1]),dtype="object")
    g_bin = np.zeros(shape=(g.shape[0],g.shape[1]),dtype="object")
    r_bin = np.zeros(shape=(r.shape[0],r.shape[1]),dtype="object")
    
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            temp_b = str(format(int(b[i,j]), '08b'))
            temp_g = str(format(int(g[i,j]), '08b'))
            temp_r = str(format(int(r[i,j]), '08b'))
            b_bin[i][j] = bin_to_dna(temp_b)
            g_bin[i][j] = bin_to_dna(temp_g)
            r_bin[i][j] = bin_to_dna(temp_r)

    b_bin = b_bin.astype(str)
    g_bin = g_bin.astype(str)
    r_bin = r_bin.astype(str)
    return b_bin,g_bin,r_bin

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

shift_address = {0:"DR",1:"D",2:"DL",3:"L",4:"UL",5:"U",6:"UR",7:"R"}

def shift_array_right(img: np.ndarray,shift_amount: int):
    img = np.roll(img,shift_amount,axis=1)
    return img
def shift_array_left(img: np.ndarray,shift_amount: int):
    img = np.roll(img,-shift_amount,axis=1)
    return img
def shift_array_up(img: np.ndarray,shift_amount: int):
    img = np.roll(img,shift_amount,axis=0)
    return img
def shift_array_down(img: np.ndarray,shift_amount: int):
    img = np.roll(img,-shift_amount,axis=0)
    return img

shift_direction = {"R":shift_array_left,"L":shift_array_right,"U":shift_array_down,"D":shift_array_up}

def inverse_shift_array_with_octal_sequece(array: np.ndarray,shift_sequence: str,shared_key: str):
    shared_key = bytes_to_int(binascii.hexlify(shared_key.encode()))
    shift_order = [shift_address[int(num)] for num in shift_sequence]
    print(shift_order)
    index = len(shift_order)
    shift_order = reversed(shift_order)
    print(shift_order)

    for shift in shift_order:
        for direction in reversed(shift):
            array = shift_direction[direction](array,-int(str(shared_key)[index:index+2]))
        index = index -1
    return array

#Step 3
def dna_subtraction(b_enc,g_enc,r_enc):
    b,g,r = b_enc,g_enc,r_enc
    print(b.shape)
    m,n = b_enc.shape
    b_dna= np.zeros(shape=(b.shape[0],b.shape[1]),dtype="object")
    g_dna = np.zeros(shape=(g.shape[0],g.shape[1]),dtype="object")
    r_dna = np.zeros(shape=(r.shape[0],r.shape[1]),dtype="object")
    for i in range(m):
        for j in range(n):
            r_dna[i,j] = dna["{0}{1}".format(r[i,j][0],g[i,j][0])]+dna["{0}{1}".format(r[i,j][1],g[i,j][1])]+dna["{0}{1}".format(r[i,j][2],b[i,j][2])]+dna["{0}{1}".format(r[i,j][3],b[i,j][3])]
            g_dna[i,j] = dna["{0}{1}".format(g[i,j][0],b[i,j][0])]+dna["{0}{1}".format(g[i,j][1],b[i,j][1])]+dna["{0}{1}".format(g[i,j][2],b[i,j][2])]+dna["{0}{1}".format(g[i,j][3],b[i,j][3])]
            b_dna[i,j] = dna["{0}{1}".format(g_dna[i,j][0],b[i,j][0])]+dna["{0}{1}".format(g_dna[i,j][1],b[i,j][1])]+dna["{0}{1}".format(g_dna[i,j][2],b[i,j][2])]+dna["{0}{1}".format(g_dna[i,j][3],b[i,j][3])]
    b_dna = b_dna.astype(str)
    g_dna = g_dna.astype(str)
    r_dna = r_dna.astype(str)
    return b_dna,g_dna,r_dna

#DNA string to binary
def dna_str_to_binary(dna_str: str):
    binary = ""
    for i in range(len(dna_str)):
        binary+=dna[dna_str[i]]
    return binary

#Dna to binary
def dna_to_binary(dna: np.ndarray):
    m,n = dna.shape
    binary_dna = np.zeros(shape=(m,n),dtype="object")
    for i in range(m):
        for j in range(n):
            binary_dna[i,j] = dna_str_to_binary(dna[i,j])
    return binary_dna

#Binary to int
def binary_to_int(array: np.ndarray):
    m,n = array.shape
    int_array = np.zeros(shape=(m,n),dtype="int")
    for i in range(m):
        for j in range(n):
            int_array[i,j] = int(array[i,j],2)
    return int_array

if __name__== "__main__":
    b,g,r = split_image_into_channel(img)
    b_dec,g_dec,r_dec = process(b,g,r)
    b_deinterleaved,g_deinterleaved,r_deinterleaved = deinterleave_dna(b_dec,g_dec,r_dec)
    print(b_deinterleaved[:10,:10])

    #invershift
    b_shift = inverse_shift_array_with_octal_sequece(b_deinterleaved, shift_sequence_b, shared_ba)
    g_shift = inverse_shift_array_with_octal_sequece(g_deinterleaved, shift_sequence_g, shared_ga)
    r_shift = inverse_shift_array_with_octal_sequece(r_deinterleaved, shift_sequence_r, shared_ra)

    print(b_shift[:10,:10])

    b_dna,g_dna,r_dna = dna_subtraction(b_shift,g_shift,r_shift)
    print(b_dna[:10,:10])

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
    cv2.imwrite("decoded_image.jpg",image)
