import secrets
import string  
from x25519 import base_point_mult,multscalar,bytes_to_int,int_to_bytes
import numpy as np
import binascii

shift_address = {0:"DR",1:"D",2:"DL",3:"L",4:"UL",5:"U",6:"UR",7:"R"}

def generate_random_octal_sequence(length=15):
    return ''.join(secrets.choice(string.octdigits) for _ in range(length))

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
    for shift in shift_order:
        for direction in shift:
            array = shift_direction[direction](array,int(str(shared_key)[index:index+2]))
        index = index + 1
    return array