# Table of contents
* [ECDH-Image-Encoding](#ECDH-Image-Encoding)
* [Installation](#Installation)
* [Highlights](#Highlights)
* [Result](#result)
* [Original paper](#original-paper)

# ECDH-Image-Encoding

This is a Python implementation based on M. Kumar et al.'s algorithm for image security using ECC diversified with DNA encoding. In this method, the authors first encode the RGB image using DNA encoding followed by asymmetric encryption based on elliptic curve Diffie-Hellman encryption.



## Installation


```cmd
git clone https://github.com/Alkahestry/ECDH-Image-Encoding.git
```

## Usage

Change the image path at line 8 in demo.py and run. You will get an encoded image and a decoded image with 2 text files contain necessary information for decoding and it should be sent to each party.
This repository is not a fully completed image cryptography algorithm hence it serves as a template for any image cryptography algorithm, please make the most use out of it.


## Highlights


+ DNA encoding on RGB image.
+ DNA addition.
+ Circular shifting with unique random octal shift sequences for each dimension and shift amount based on ECDH shared keys.
+ The dimensions are interleaved.
+ Use Bernstein's curve25519 at ECDHE for fast encryption
+ Decoding requires 3 shared keys (calculated from 3 private keys and 3 other party's public keys) along with 3 octal shift sequences.


We didn't implement extra encoding step between 2 interleaving steps because the authors didn't describe the process specifically. Which makes our algorithm different and less secured from the proposed algorithm in the paper.

## Results


![alt text](https://github.com/Alkahestry/ECDH-Image-Encoding/blob/main/resources/combine_images.jpg)

## Conclusion


The encoder yeilds an average result for encrypting multicolored and complicated images, but to encode a much more simple image, the algorithm is still far from the finish line. I would recommend adding extra encoding steps for a more secured cryptographic system.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Original paper
[A new RGB image encryption algorithm based on DNA encoding and elliptic curve Diffie–Hellman cryptography](https://www.researchgate.net/publication/293329501_A_new_RGB_image_encryption_algorithm_based_on_DNA_encoding_and_elliptic_curve_Diffie-Hellman_cryptography)


## License
[MIT](https://choosealicense.com/licenses/mit/)


