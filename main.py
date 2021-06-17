
from PIL import Image
import numpy as np
import cv2
import os

from def_analysis import analysis
from transformation import srgb_cmyk, cmyk_srgb



def qrcode():
    import qrcode
    size = 2
    qr = qrcode.QRCode(box_size=size)
    qr.add_data('I am code CMYK')
    qr.make()
    img_qr = qr.make_image(fill_color="white", back_color="black")
    img_qr.save('qrcode.png')
    return size

def coder(name_img):

    size = qrcode()
    size *= 29
    img = srgb_cmyk(name_img)
    np_img = np.array(img)
    img_result = './result/CMYK' + name_img[8:-3] + 'tif'
    img.save(img_result)

    img_qr = Image.open('qrcode.png')
    img_qr = img_qr.convert('L')
    np_img_qr = np.array(img_qr)

    cord = analysis(name_img, size)
    layer = cord[0]
    cord_y = cord[1]
    cord_x = cord[2]
    for i in range(cord_x, size+cord_x):
        for j in range(cord_y, size+cord_y):
            z = np_img_qr[i-cord_x, j-cord_y]
            if z == 255:
                np_img[i, j, layer] = z

    new_img = Image.fromarray(np_img.astype('uint8'), 'CMYK')
    name_res = './result/result_CMYK' + name_img[8:-3] + 'tif'
    new_img.save(name_res)
    cmyk_srgb(name_res)
    print(cord)
    print('end coder')
    return cord

def decoder(cord, name_img):

    img = Image.open(name_img)

    np_img = np.array(img)
    np_img_qr = np.zeros((58,58))
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

def list_img (name_dir):
    arr = ['./' + name_dir + '/' + x for x in os.listdir('./' + name_dir) if x.endswith(".tiff") or x.endswith(".jpg") or x.endswith(".png") or x.endswith(".tif")]
    return arr

def test():
    name_dir = 'image'
    list_name_img = list_img(name_dir)
    for i in range(list_name_img.__sizeof__()):
        print(i)
        name_img = list_name_img[i]
        print(name_img)
        cord = coder(name_img)
        name_img = './result/result_CMYK' + name_img[8:-3] + 'tif'
        decoder(cord, name_img)

test()