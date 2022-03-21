import os
import binascii

def write_keys_to_file(file_name: str,**kwargs):
    with open(file_name,"w") as f:
        f.write("Private key R: {}\n".format(kwargs["r_priv"]))
        f.write("Private key G: {}\n".format(kwargs["g_priv"]))
        f.write("Private key B: {}\n".format(kwargs["b_priv"]))

        f.write("\n")
        f.write("Public key R: {}\n".format(binascii.hexlify(kwargs["r_pub"].encode())))
        f.write("Public key G: {}\n".format(binascii.hexlify(kwargs["g_pub"].encode())))
        f.write("Public key B: {}\n".format(binascii.hexlify(kwargs["b_pub"].encode())))

        f.write("\n")
        f.write("Shift sequence R: {}\n".format(kwargs["r_shift"]))
        f.write("Shift sequence G: {}\n".format(kwargs["g_shift"]))
        f.write("Shift sequence B: {}\n".format(kwargs["b_shift"]))