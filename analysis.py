from PIL import Image


def get_qr_coordinates(img, size_qr):
    width, height = img.size[0], img.size[1]
    print(width, height)
    square_value = -1
    layer = -1  # номер слоя, на который будет внедряться код(0 - с, 1 - m и тд)
    x_qr, y_qr = 0, 0  # координаты x, y для внедрения qr-кода
    pix = img.load()

    for i in range(0, width, size_qr):
        for j in range(0, height, size_qr):
            if i + size_qr < width and j + size_qr < height:
                value_c, value_m, value_y = 0, 0, 0
                coor_x, coor_y = i, j
                for a in range(coor_x, coor_x + size_qr):
                    for b in range(coor_y, coor_y + size_qr):
                        c = pix[a, b][0]
                        m = pix[a, b][1]
                        y = pix[a, b][2]

                        value_c += (c - m + y)
                        value_m += (m - c + y)
                        value_y += (y - c + m)
            
                if value_c >= value_m and value_c >= value_y:
                    if value_c > square_value:
                        square_value = value_c
                        layer = 0
                        x_qr, y_qr = coor_x, coor_y

                elif value_m >= value_c and value_m >= value_y:
                    if value_m > square_value:
                        square_value = value_m
                        layer = 1
                        x_qr, y_qr = coor_x, coor_y

                else:
                    if value_y > square_value:
                        square_value = value_y
                        layer = 2
                        x_qr, y_qr = coor_x, coor_y

    return {"layer": layer, "x_qr": x_qr, "y_qr": y_qr}
