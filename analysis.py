from PIL import Image

SIZE = 100 # размер QR-кода
square_value = -1 
layer = -1 # номер слоя, на который будет внедряться код(0 - с, 1 - m и тд)
a, b = 0, 0 # координаты для внедрения кода 

def assignment(sq_value, lay, x, y):
    global square_value, layer, a, b
    square_value = sq_value
    layer = lay
    a, b = x, y

def square_analysis(pix, coor_x, coor_y):
    value_c = 0
    value_m = 0
    value_y = 0
    for i in range(coor_x, coor_x + SIZE):
        for j in range(coor_y, coor_y + SIZE):
            c = pix[i, j][0]
            m = pix[i, j][1]
            y = pix[i, j][2]

            value_c += (c - m + y)
            value_m += (m - c + y)
            value_y += (y - c + m)
            
    if value_c >= value_m and value_c >= value_y:
        if value_c > square_value:
            assignment(value_c, 0, coor_x, coor_y)

    elif value_m >= value_c and value_m >= value_y:
        if value_m > square_value:
            assignment(value_m, 1, coor_x, coor_y)

    else:
        if value_y > square_value:
            assignment(value_y, 2, coor_x, coor_y)


image = Image.open("02_CYYY_CMYK.tif")
width, height = image.size[0], image.size[1]
pix = image.load()

for i in range(0, width, SIZE):
    for j in range(0, height, SIZE):
        if i + SIZE < width and j + SIZE < height:
            square_analysis(pix, i, j)

print('layer =', layer)
print('x =', a, 'y =', b)
