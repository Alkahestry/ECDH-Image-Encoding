import numpy as np
from crypto.shift import *
from crypto.dna_operation import dna_sub


#deinterleave dna
def deinterleave_dna_col(b_dna,g_dna,r_dna):
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

def deinterleave_dna_row(b_dna,g_dna,r_dna):
    m,n = b_dna.shape
    b_dna_deinterleaved = np.zeros(shape=(b_dna.shape[0],b_dna.shape[1]),dtype="object")
    g_dna_deinterleaved = np.zeros(shape=(g_dna.shape[0],g_dna.shape[1]),dtype="object")
    r_dna_deinterleaved = np.zeros(shape=(r_dna.shape[0],r_dna.shape[1]),dtype="object")
    for i in range(m):
        if i%3==0:
            b_dna_deinterleaved[i,:] = b_dna[i,:]
            g_dna_deinterleaved[i,:] = g_dna[i,:]
            r_dna_deinterleaved[i,:] = r_dna[i,:]
        elif i%3==1:
            b_dna_deinterleaved[i,:] = g_dna[i,:]
            g_dna_deinterleaved[i,:] = r_dna[i,:]
            r_dna_deinterleaved[i,:] = b_dna[i,:]
        else:
            b_dna_deinterleaved[i,:] = r_dna[i,:]
            g_dna_deinterleaved[i,:] = b_dna[i,:]
            r_dna_deinterleaved[i,:] = g_dna[i,:]

    return b_dna_deinterleaved,g_dna_deinterleaved,r_dna_deinterleaved

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