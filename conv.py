import numpy as np
import sympy as sp
import imageio

KEYSIZE = 3

def inv3x3(key):
    try:
        s = sp.Matrix(key)
        return np.array(s.inv_mod(256)).astype(int)
    except:
        return None

if __name__ == '__main__':
    # load and crop image
    raw_img = imageio.imread('stock-photo-model.jpg')

    gray = raw_img[:, :, 0]

    crop = gray[:KEYSIZE*(gray.shape[0]//KEYSIZE), :]
    print(crop.shape)
    print()

    # generate invertible matrix
    key = None
    key_inv = None
    while key_inv is None:
        key = np.random.randint(256, size=(KEYSIZE,KEYSIZE))
        key_inv = inv3x3(key)

    print("encryption key: ")
    print(key)
    print()

    print("decryption key: ")
    print(key_inv)
    print()

    encr = None
    for i in range(0, crop.shape[0]//KEYSIZE):
        rows = crop[KEYSIZE*i:KEYSIZE*(i+1)]
        m = (key @ rows) % 256

        try:
            encr = np.append(encr, m, axis=0)
        except:
            encr = m
    imageio.imwrite('encrypted.jpg', encr)

    # decrypt image
    decr = None
    for i in range(0, encr.shape[0]//KEYSIZE):
        rows = encr[KEYSIZE*i:KEYSIZE*(i+1)]
        m = (key_inv @ rows) % 256

        try:
            decr = np.append(decr, m, axis=0)
        except:
            decr = m
    imageio.imwrite('decrypted.jpg', decr)
