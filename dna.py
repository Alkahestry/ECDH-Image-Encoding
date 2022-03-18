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


#Convert each pixel value to binary number
def convert_to_binary(b,g,r):
    b = np.unpackbits(b,axis=1)
    g = np.unpackbits(g,axis=1)
    r = np.unpackbits(r,axis=1)
    return b,g,r

def encode_to_dna(b,g,r):
    m,n = b.shape
    b_enc= np.chararray((m,int(n/2)))
    g_enc= np.chararray((m,int(n/2)))
    r_enc= np.chararray((m,int(n/2)))
    for color,enc in zip([b,g,r],[b_enc,g_enc,r_enc]):
        for i in range(m):
            for j in range(int(n/2)):
                enc[i,j] = dna["{0}{1}".format(color[i][j*2:j*2+2][0],color[i][j*2:j*2+2][1])]
    b_enc = b_enc.astype(str)
    g_enc = g_enc.astype(str)
    r_enc = r_enc.astype(str)
    return b_enc,g_enc,r_enc
#Group 4 pixel together following axis 1
def group_4_pixel_together(img: np.ndarray):
    m,n = img.shape
    new_array = np.chararray((m,n//4))
    # img_grouped = np.chararray((m,n))
    for i in range(m):
        for j in range(n//4):
            new_array[i,j] = "{0}{1}{2}{3}".format(img[i,(j-1)*4],img[i,(j-1)*4+1],img[i,(j-1)*4+2],img[i,(j-1)*4+3])
    new_array = new_array.astype(str)
    return new_array
#Step 3
def dna_addition(b_enc,g_enc,r_enc):
    b,g,r = b_enc,g_enc,r_enc
    print(b.shape)
    m,n = b_enc.shape
    b_dna = np.chararray((m,n))
    g_dna = np.chararray((m,n))
    r_dna = np.chararray((m,n))
    for i in range(m):
        for j in range(n):
            r_dna[i,j] = dna["{0}{1}".format(r[i,j],g[i,j])]
            g_dna[i,j] = dna["{0}{1}".format(g[i,j],b[i,j])]
            b_dna[i,j] = dna["{0}{1}".format(g_dna[i,j].decode("utf-8"),b[i,j])]
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
    b_dna_interleaved = np.chararray((m,n))
    g_dna_interleaved = np.chararray((m,n))
    r_dna_interleaved = np.chararray((m,n))
    for i in range(m):
        for j in range(n):
            b_dna_interleaved[i,j] = b_dna[i,j]
            g_dna_interleaved[i,j] = g_dna[i,j]
            r_dna_interleaved[i,j] = r_dna[i,j]
    for i in range(m):
        for j in range(n):
            if j%2==0:
                b_dna_interleaved[i,j] = b_dna[i,j]
                g_dna_interleaved[i,j] = r_dna[i,j]
                r_dna_interleaved[i,j] = g_dna[i,j]
            else:
                b_dna_interleaved[i,j] = r_dna[i,j]
                g_dna_interleaved[i,j] = b_dna[i,j]
                r_dna_interleaved[i,j] = g_dna[i,j]
    b_dna_interleaved = b_dna_interleaved.astype(str)
    g_dna_interleaved = g_dna_interleaved.astype(str)
    r_dna_interleaved = r_dna_interleaved.astype(str)
    return b_dna_interleaved,g_dna_interleaved,r_dna_interleaved

    

if __name__ == "__main__":
    b,g,r = split_image_into_channel(img)
    print("Shape after split {0}".format(b.shape))
    b_enc,g_enc,r_enc = process(b,g,r)
    print("Shape after convert to binary {0}".format(b.shape))
    print(b_enc)
    print(b_enc[0])
    print(b_enc[0][0])
    # b_enc,g_enc,r_enc = encode_to_dna(b,g,r)
    print("Shape after encoded to dna {0}".format(b_enc.shape))
    # b_enc,g_enc,r_enc = group_4_pixel_together(b_enc),group_4_pixel_together(g_enc),group_4_pixel_together(r_enc)
    # print("Shape after group 4 pixel together {0}".format(b_enc.shape))
    # print(b_enc)
    # print(b_enc[0])
    # print(b_enc[0][1])
    
    b_dna,g_dna,r_dna = dna_addition(b_enc,g_enc,r_enc)
    print("Shape after dna addition{0}".format(b_dna.shape))
    # rgb_dna = interleave_dna(b_dna,g_dna,r_dna)
    # print("Shape after interleave {0}".format(rgb_dna[0].shape))

    # rgb = np.dstack((rgb_dna[0],rgb_dna[1],rgb_dna[2]))
    # print(rgb_dna[0])
    # b_dna,g_dna,r_dna = deinterleave_dna(rgb_dna[0],rgb_dna[1],rgb_dna[2])
    # print("Shape after deinterleave {0}".format(b_dna.shape))
    # shift_sequence = generate_random_octal_sequence()
    # img = shift_array_with_octal_sequece(img,shift_sequence,ai)

    # cv2.imshow("Image",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

