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
size_a,size_b,dim = img.shape   
#Private key
a = os.urandom(32)
b = os.urandom(32)
#To int
ai = bytes_to_int(a)
bi = bytes_to_int(b)
#Public key
a_pub = base_point_mult(a)
b_pub = base_point_mult(b)
#Shared key
k_a = multscalar(a, b_pub) # a (bG)
k_b = multscalar(b, a_pub) # b (aG)
#DNA-Encoding RULE #1 A = 00, C=01, G=10, T=11
dna = {}
dna["00"] = "A"
dna["01"] = "C"
dna["10"] = "G"
dna["11"] = "T"
dna["A"] = [0,0]
dna["C"] = [0,1]
dna["G"] = [1,0]
dna["T"] = [1,1]
#DNA xor
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
            r_dna[i,j] = dna["{0}{1}".format(r[i,j][0],g[i,j][1])]+dna["{0}{1}".format(r[i,j][1],g[i,j][1])]+dna["{0}{1}".format(r[i,j][2],b[i,j][2])]+dna["{0}{1}".format(r[i,j][3],b[i,j][3])]
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
    shift_order = [shift_address[int(num)] for num in shift_sequence]
    shift_amount = int(str(shared_key)[:2])
    print(shift_order)
    for shift in shift_order:
        for direction in shift:
            array = shift_direction[direction](array,shift_amount)
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

#Decode the image

if __name__ == "__main__":
    b,g,r = split_image_into_channel(img)
    print("Shape after split {0}".format(b.shape))
    b_enc,g_enc,r_enc = process(b,g,r)
    print("Shape after encoded to dna {0}".format(b_enc.shape))
    
    b_dna,g_dna,r_dna = dna_addition(b_enc,g_enc,r_enc)
    print("Shape after dna addition{0}".format(b_dna.shape))

    shift_sequence = generate_random_octal_sequence()
    b_shift = shift_array_with_octal_sequece(b_dna,shift_sequence,ai)
    g_shift = shift_array_with_octal_sequece(g_dna,shift_sequence,ai)
    r_shift = shift_array_with_octal_sequece(r_dna,shift_sequence,ai)

    print(b_shift[:10,:10])
    print(g_shift[:10,:10])
    print(r_shift[:10,:10])
    b_dna_interleaved,g_dna_interleaved,r_dna_interleaved = interleave_dna(b_shift,g_shift,r_shift)
    print("Shape after interleave {0}".format(b_dna_interleaved.shape))
    print(b_dna_interleaved[:10,:10])
    print(g_dna_interleaved[:10,:10])
    print(r_dna_interleaved[:10,:10])

    # cv2.imshow("Image",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

