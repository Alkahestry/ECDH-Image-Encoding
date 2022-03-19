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
img = cv2.imread("gan.jpg")
# size_a,size_b,dim = img.shape   
#Private key
ra_priv = os.urandom(32)
rb_priv = os.urandom(32)
ga_priv = os.urandom(32)
gb_priv = os.urandom(32)
ba_priv = os.urandom(32)
bb_priv = os.urandom(32)
print("ra_priv =",ra_priv)
print("rb_priv = ",rb_priv)
print("ga_priv =",ga_priv)
print("gb_priv =",gb_priv)
print("bb_priv =",bb_priv)
print("ba_priv =",ba_priv)
#To int
# ai = bytes_to_int(a)
# bi = bytes_to_int(b)
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
#DNA addition
dna["CT"]=dna["TC"]=dna["GG"]=dna["AA"]="A"
dna["AC"]=dna["CA"]=dna["TG"]=dna["GT"]="C"
dna["AG"]=dna["GA"]=dna["TT"]=dna["CC"]="G"
dna["AT"]=dna["TA"]=dna["CG"]=dna["GC"]="T"
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

#Step 3
def dna_addition(b_enc,g_enc,r_enc):
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

#Step 4
#Generate random octal sequence
def generate_random_octal_sequence(length=15):
    return ''.join(secrets.choice(string.octdigits) for _ in range(length))

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

shift_direction = {"R":shift_array_right,"L":shift_array_left,"U":shift_array_up,"D":shift_array_down}

def shift_array_with_octal_sequece(array: np.ndarray,shift_sequence: str,shared_key: str):
    shared_key = bytes_to_int(binascii.hexlify(shared_key.encode()))
    shift_order = [shift_address[int(num)] for num in shift_sequence]
    
    index = 0
    print(shift_order)
    for shift in shift_order:
        for direction in shift:
            array = shift_direction[direction](array,int(str(shared_key)[index:index+2]))
        index = index + 1
    return array

# def write_keys_to_file(file_name: str,key_a: str,key_b: str):
#     with open(file_name,"w") as f:
#         f.write(key_a)
#         f.write("\n")
#         f.write(key_b)
#         f.write("\n")

#Step 5
#Interleave BBBGGGRRR to BGRBGRBGR
def interleave_dna(b_dna,g_dna,r_dna):
    m,n = b_dna.shape
    b_dna_interleaved = np.zeros(shape=(b_dna.shape[0],b_dna.shape[1]),dtype="object")
    g_dna_interleaved = np.zeros(shape=(g_dna.shape[0],g_dna.shape[1]),dtype="object")
    r_dna_interleaved = np.zeros(shape=(r_dna.shape[0],r_dna.shape[1]),dtype="object")
    # for i in range(m):
    for j in range(n):
        if j%3==0:
            b_dna_interleaved[:,j] = b_dna[:,j]
            g_dna_interleaved[:,j] = g_dna[:,j]
            r_dna_interleaved[:,j] = r_dna[:,j]
        elif j%3==1:
            b_dna_interleaved[:,j] = r_dna[:,j]
            g_dna_interleaved[:,j] = b_dna[:,j]
            r_dna_interleaved[:,j] = g_dna[:,j]
        else:
            b_dna_interleaved[:,j] = g_dna[:,j]
            g_dna_interleaved[:,j] = r_dna[:,j]
            r_dna_interleaved[:,j] = b_dna[:,j]

    return b_dna_interleaved,g_dna_interleaved,r_dna_interleaved

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
#inverse shifting with shift sequence


if __name__ == "__main__":
    b,g,r = split_image_into_channel(img)
    print("Shape after split {0}".format(b.shape))
    b_enc,g_enc,r_enc = process(b,g,r)
    print("Shape after encoded to dna {0}".format(b_enc.shape))
    
    b_dna,g_dna,r_dna = dna_addition(b_enc,g_enc,r_enc)
    print("Shape after dna addition{0}".format(b_dna.shape))

    shift_sequence_b = generate_random_octal_sequence()
    shift_sequence_g = generate_random_octal_sequence()
    shift_sequence_r = generate_random_octal_sequence()
    b_shift = shift_array_with_octal_sequece(b_dna,shift_sequence_b,shared_ba)
    g_shift = shift_array_with_octal_sequece(g_dna,shift_sequence_g,shared_ga)
    r_shift = shift_array_with_octal_sequece(r_dna,shift_sequence_r,shared_ra)
    print("Shift sequence shift_sequence_b {0}".format(shift_sequence_b))
    print("Shift sequence shift_sequence_g {0}".format(shift_sequence_g))
    print("Shift sequence shift_sequence_r {0}".format(shift_sequence_r))
    print("Shared key shared_ba {0}".format(shared_ba))
    print("Shared key shared_ga {0}".format(shared_ga))
    print("Shared key shared_ra {0}".format(shared_ra))
    

    b_dna_interleaved,g_dna_interleaved,r_dna_interleaved = interleave_dna(b_shift,g_shift,r_shift)
    print("Shape after interleave {0}".format(b_dna_interleaved.shape))


    b_bin = dna_to_binary(b_dna_interleaved)
    g_bin = dna_to_binary(g_dna_interleaved)
    r_bin = dna_to_binary(r_dna_interleaved)
    print("Shape after dna to binary {0}".format(b_bin.shape))


    b_int = binary_to_int(b_bin)
    g_int = binary_to_int(g_bin)
    r_int = binary_to_int(r_bin)
    print("Shape after binary to int {0}".format(b_int.shape))

    image = np.dstack((b_int,g_int,r_int))
    image = image.astype(np.uint8)
    print(image.shape)
    cv2.imshow("Image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("encoded_image.jpg",image)

