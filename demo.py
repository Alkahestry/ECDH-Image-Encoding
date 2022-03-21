import cv2
import numpy as np
import os
from crypto import *
from utils import write_keys_to_file

#Read image
img_path = "gan.jpg"
img = cv2.imread(img_path)
output_folder = 'output'

#Generate private key
ra_priv,rb_priv,ga_priv,gb_priv,ba_priv,bb_priv = [os.urandom(32) for _ in range(6)]
private_keys = [ra_priv,rb_priv,ga_priv,gb_priv,ba_priv,bb_priv]
#Calculate public key from private key
ra_pub,rb_pub,ga_pub,gb_pub,ba_pub,bb_pub = [base_point_mult(key) for key in private_keys]
public_keys = [ra_pub,rb_pub,ga_pub,gb_pub,ba_pub,bb_pub]
#Calculate shared key from private key and other party's public key
shared_ra,shared_rb,shared_ga,shared_gb,shared_ba,shared_bb = [multscalar(key_priv,key_pub) for key_priv,key_pub in zip(private_keys,public_keys)]

#Define shift addresses
shift_address = {0:"DR",1:"D",2:"DL",3:"L",4:"UL",5:"U",6:"UR",7:"R"}
shift_direction = {"R":shift_array_right,"L":shift_array_left,"U":shift_array_up,"D":shift_array_down}
inverse_shift_direction = {"R":shift_array_left,"L":shift_array_right,"U":shift_array_down,"D":shift_array_up}

if __name__ == "__main__":
    print("Encoding image...")
    b,g,r = split_image_into_channel(img)

    b_enc,g_enc,r_enc = encode_to_dna(b,g,r)
    
    b_dna,g_dna,r_dna = dna_addition(b_enc,g_enc,r_enc)

    #Generate random octal sequence for shifting
    shift_sequence_b,shift_sequence_g,shift_sequence_r = [generate_random_octal_sequence() for _ in range(3)]

    b_shift = shift_array_with_octal_sequece(b_dna,shift_sequence_b,shared_ba)
    g_shift = shift_array_with_octal_sequece(g_dna,shift_sequence_g,shared_ga)
    r_shift = shift_array_with_octal_sequece(r_dna,shift_sequence_r,shared_ra)

    b_dna_interleaved,g_dna_interleaved,r_dna_interleaved = interleave_dna_col(b_shift,g_shift,r_shift)

    b_dna_interleaved,g_dna_interleaved,r_dna_interleaved = interleave_dna_row(b_dna_interleaved,g_dna_interleaved,r_dna_interleaved)

    b_bin,g_bin,r_bin = [dna_to_binary(dna_interleaved) for dna_interleaved in [b_dna_interleaved,g_dna_interleaved,r_dna_interleaved]]

    b_int,g_int,r_int = [binary_to_int(bin) for bin in [b_bin,g_bin,r_bin]] 
    
    image = np.dstack((b_int,g_int,r_int))
    image = image.astype(np.uint8)
    print("Encoding image done!")
    cv2.imshow("Enconded Image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(output_folder + "/encoded_image."+img_path.split('.')[1],image)
    
    print("Writing keys to file...")
    write_keys_to_file(output_folder + "/keys_1.txt",r_priv=ra_priv,g_priv=ga_priv,b_priv=ba_priv,r_pub=ra_pub,g_pub=ga_pub,b_pub=ba_pub,r_shift=shift_sequence_r,g_shift=shift_sequence_g,b_shift=shift_sequence_b)
    write_keys_to_file(output_folder + "/keys_2.txt",r_priv=rb_priv,g_priv=gb_priv,b_priv=bb_priv,r_pub=rb_pub,g_pub=gb_pub,b_pub=bb_pub,r_shift=shift_sequence_r,g_shift=shift_sequence_g,b_shift=shift_sequence_b)
    print("Decoding image...")
    #Decoder
    b,g,r = split_image_into_channel(image)
    b_dec,g_dec,r_dec = encode_to_dna(b,g,r)
    b_dec,g_dec,r_dec = deinterleave_dna_row(b_dec,g_dec,r_dec)
    b_deinterleaved,g_deinterleaved,r_deinterleaved = deinterleave_dna_col(b_dec,g_dec,r_dec)

    #invershift
    b_shift = inverse_shift_array_with_octal_sequece(b_deinterleaved, shift_sequence_b, shared_ba)
    g_shift = inverse_shift_array_with_octal_sequece(g_deinterleaved, shift_sequence_g, shared_ga)
    r_shift = inverse_shift_array_with_octal_sequece(r_deinterleaved, shift_sequence_r, shared_ra)

    b_dna,g_dna,r_dna = dna_subtraction(b_shift,g_shift,r_shift)

    b_dna_binary,g_dna_binary,r_dna_binary = [dna_to_binary(dna) for dna in [b_dna,g_dna,r_dna]]

    b_dna_int,g_dna_int,r_dna_int = [binary_to_int(dna_binary) for dna_binary in [b_dna_binary,g_dna_binary,r_dna_binary]]

    image = np.dstack((b_dna_int,g_dna_int,r_dna_int))
    image = image.astype(np.uint8)
    print("Decoding image done!")
    cv2.imshow("Image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
