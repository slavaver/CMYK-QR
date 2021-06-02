def coder():
    import qrcode
    from PIL import Image
    import numpy as np

    size = 2
    qr = qrcode.QRCode(box_size=size)
    qr.add_data('I am code CMYK')
    qr.make()
    img_qr = qr.make_image(fill_color="white", back_color="black")

    img = Image.open('test.png')
    img = img.convert('CMYK')
    np_img = np.array(img)
    img.save('test_cmyk.tif')

    img_qr.save('qrcode.png')
    img_qr = img_qr.convert('L')
    np_img_qr = np.array(img_qr)

    size *= 29
    cord_x = 100
    cord_y = 10

    for i in range(cord_x, size+cord_x):
        for j in range(cord_y, size+cord_y):

            z = np_img_qr[i-cord_x, j-cord_y]
            if z == 255:
                np_img[i, j, 1] = z

    new_img = Image.fromarray(np_img.astype('uint8'), 'CMYK')
    new_img.save('result.tif')
    print('end coder')

def decoder():
    import cv2
    from PIL import Image
    import numpy as np

    img = Image.open('result.tif')
    np_img = np.array(img)

    np_img_qr = np.zeros((58,58))
    np_img_qr.fill(255)

    size = 58
    cord_x = 100
    cord_y = 10

    for i in range(cord_x, size + cord_x):
        for j in range(cord_y, size + cord_y):

            z = np_img[i, j, 1]
            if z == 255:
                z = 0
                np_img_qr[i - cord_x, j - cord_y] = z

    new_img_qr = Image.fromarray(np_img_qr.astype('uint8'), 'L')
    new_img_qr.save('result_qr.png')

    img_qr = cv2.imread("result_qr.png")
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(img_qr)
    if vertices_array is not None:
        print("QRCode data:", data)
    else:
        print("There was some error")

    print("end decoder")

coder()
decoder()