# ECDH-Image-Encoding

This is a Python implementation based on M. Kumar et al.'s algorithm for image security using ECC diversified with DNA encoding. In this method, the authors first encode the RGB image using DNA encoding followed by asymmetric encryption based on elliptic curve Diffie-Hellman encryption.

## Installation


```cmd
git clone https://github.com/Alkahestry/ECDH-Image-Encoding.git
```

## Usage


This repository is a half-finish image cryptography algorithm hence it serves as a template for any image cryptography algorithm, please make the most use out of it.


## Algorithm


This algorithm includes the following steps:
+ DNA encoding on RGB image
+ DNA addition for further scrambling the image
+ Unique random shift sequences for each dimension with amount based on ECDH shared keys.
+ Interleaving the RGB dimensions


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Original paper
[A new RGB image encryption algorithm based on DNA encoding and elliptic curve Diffie–Hellman cryptography](https://www.researchgate.net/publication/293329501_A_new_RGB_image_encryption_algorithm_based_on_DNA_encoding_and_elliptic_curve_Diffie-Hellman_cryptography)