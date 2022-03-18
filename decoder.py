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
img = cv2.imread("encoded_image.jpg")

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
def dna_subtraction(b_enc,g_enc,r_enc):
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