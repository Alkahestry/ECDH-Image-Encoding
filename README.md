# Table of contents
* [ECDH-Image-Encoding](#ECDH-Image-Encoding)
* [Installation](#Installation)
* [Algorithm](#Algorithm)
* [Result](#result)
* [Original paper](#original-paper)

# ECDH-Image-Encoding

This is a Python implementation based on M. Kumar et al.'s algorithm for image security using ECC diversified with DNA encoding. In this method, the authors first encode the RGB image using DNA encoding followed by asymmetric encryption based on elliptic curve Diffie-Hellman encryption.



## Installation


```cmd
git clone https://github.com/Alkahestry/ECDH-Image-Encoding.git
```

## Usage


This repository is a half-finish image cryptography algorithm hence it serves as a template for any image cryptography algorithm, please make the most use out of it.


## Algorithm


Highlights:
+ DNA encoding on RGB image.
+ DNA addition.
+ Circular shifting with unique random octal shift sequences for each dimension and shift amount based on ECDH shared keys.
+ The dimensions are interleaved.
+ Use Bernstein's curve25519 at ECDHE for fast encryption
+ Decoding requires 3 shared keys (calculated from 3 private keys and 3 other party's public keys) along with 3 octal shift sequences.


## Result


![alt text](https://github.com/Alkahestry/ECDH-Image-Encoding/blob/main/resources/combine_images.jpg)

The encoder yeilds an average result for encrypting multicolored and complicated images, but to encode a much more simple image, the algorithm is still far from the finish line. I would recommend adding extra encoding steps for a more secured cryptographic system.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Original paper
[A new RGB image encryption algorithm based on DNA encoding and elliptic curve Diffie–Hellman cryptography](https://www.researchgate.net/publication/293329501_A_new_RGB_image_encryption_algorithm_based_on_DNA_encoding_and_elliptic_curve_Diffie-Hellman_cryptography)