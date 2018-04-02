import sys
import numpy as np
import sympy as sp
import imageio

KEYSIZE = 3

def inv_matrix(key):
    try:
        s = sp.Matrix(key)
        return np.array(s.inv_mod(256)).astype(int)
    except:
        return None

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(len(sys.argv))
        print("USAGE: e/d in_name out_name key_file")
        exit(0)

    decrypt_mode = sys.argv[1] == 'd'
    file_in = sys.argv[2]
    file_out = sys.argv[3]
    key_file = sys.argv[4]

    # load and crop image
    raw_img = imageio.imread(file_in)

    crop = raw_img[:KEYSIZE*(raw_img.shape[0]//KEYSIZE), :, :]

    key = None
    key_inv = None
    if not decrypt_mode:
       # generate invertible key
       while key_inv is None:
           key = np.random.randint(256, size=(KEYSIZE,KEYSIZE))
           key_inv = inv_matrix(key)

       np.savetxt(key_file, key, fmt='%3i')
    else:
        key = np.loadtxt(key_file, dtype=int)
        key = inv_matrix(key)

    print("KEY: ")
    print(key)

    encr_color = None
    for z in range(0, crop.shape[2]):
        layer = crop[:,:,z]

        encr = None
        for i in range(0, layer.shape[0]//KEYSIZE):
            rows = layer[KEYSIZE*i:KEYSIZE*(i+1)]

            m = (key @ rows) % 256

            try:
                encr = np.append(encr, m, axis=0)
            except:
                encr = m
        try:
            encr_color = np.dstack((encr_color, encr))
        except:
            encr_color = encr

    encr_color = encr_color.astype(np.uint8)

    imageio.imwrite(file_out, encr_color)
