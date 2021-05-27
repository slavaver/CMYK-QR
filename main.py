import qrcode
from PIL import Image
import numpy as np

size = 2
qr = qrcode.QRCode(box_size=size)
qr.add_data('Hello World!')
qr.make()
img_qr = qr.make_image(fill_color="white", back_color="black")

size *= 29

img = Image.open('test.png')
img = img.convert('CMYK')
np_img = np.array(img)
img.save('test_cmyk.tif')

img_qr.save('qrcode.png')
img_qr = img_qr.convert('L')
np_img_qr = np.array(img_qr)

cord_x = 110
cord_y = 10

for i in range(cord_x, size+cord_x):
    for j in range(cord_y, size+cord_y):

        z = np_img_qr[i-cord_x, j-cord_y]
        if z == 255:
            np_img[i, j, 1] = z

new_img = Image.fromarray(np_img.astype('uint8'), 'CMYK')
new_img.save('result.tif')
print('end')