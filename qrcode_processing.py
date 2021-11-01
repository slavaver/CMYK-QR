from PIL import Image
import numpy as np
import cv2

import qrcode
from analysis import get_qr_coordinates


def qrcode_generator(msg):
    qr = qrcode.QRCode()
    qr.add_data(msg)
    img = qr.make_image()
    return img


def coder(img):
    img_qr = qrcode_generator('Some data here')
    np_img_qr = np.asarray(img_qr)
    size = np_img_qr.shape[0]
    np_img = np.array(img)

    coord = get_qr_coordinates(img, size)
    layer = coord["layer"]
    coord_x = coord["x_qr"]
    coord_y = coord["y_qr"]

    for i in range(coord_y, size + coord_y):
        for j in range(coord_x, size + coord_x):
            z = np_img_qr[i-coord_y, j-coord_x]
            if z:
                np_img[i, j, layer] = 255

    return Image.fromarray(np_img.astype('uint8'), 'CMYK')


def decoder(cord, name_img):

    img = Image.open(name_img)

    np_img = np.array(img)
    np_img_qr = np.zeros((58, 58))
    np_img_qr.fill(255)

    size = 58
    layer = cord[0]
    cord_y = cord[1]
    cord_x = cord[2]

    for i in range(cord_x, size + cord_x):
        for j in range(cord_y, size + cord_y):

            z = np_img[i, j, layer]

            if z == 255:
                z = 0
                np_img_qr[i - cord_x, j - cord_y] = z

    new_img_qr = Image.fromarray(np_img_qr.astype('uint8'), 'L')
    new_img_qr.save('result_qr.png')

    img_qr = cv2.imread("result_qr.png")
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(img_qr)

    file_name = 'result_test.txt'
    file_result = open(file_name, 'a')

    if vertices_array is not None:
        print("QRCode data:", data)

        string_data = "Img_name - " + name_img + " , Result - true , Data - " + data + " , Cord QRCode - " + str(cord) + " \n"
        file_result.write(string_data)
    else:
        print("There was some error")
        string_data = 'Img_name - ' + name_img + ' , Result - false , Data - null , Cord QRCode - ' + str(cord) + ' \n'
        file_result.write(string_data)

    file_result.close()
    print("end decoder")
