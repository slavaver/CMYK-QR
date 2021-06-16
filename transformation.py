from PIL import Image, ImageCms

SRGB = "SRGB.icm"
CMYK = "CMYK.icc"

def srgb_cmyk(name):
    t = ImageCms.buildTransform(SRGB, CMYK, "RGB", "CMYK")
    img = Image.open(name)
    img_cmyk = ImageCms.applyTransform(img, t)
    img_cmyk.save('test_CMYK.tif')
    return img_cmyk

def cmyk_srgb(name):
    t = ImageCms.buildTransform(CMYK, SRGB, "CMYK", "RGB")
    img = Image.open(name)
    img_srgb = ImageCms.applyTransform(img, t)
    img_srgb.save('result_sRGB.png')

