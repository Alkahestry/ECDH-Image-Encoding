import cv2
import numpy as np
from crypto.dna_operation import dna
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

def encode_to_dna(b,g,r):
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