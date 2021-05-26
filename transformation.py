from PIL import Image, ImageCms

SRGB = "SRGB.icm"
CMYK = "CMYK.icc"

def srgb_cmyk():
    t = ImageCms.buildTransform(SRGB, CMYK, "RGB", "CMYK")
    
    img = Image.open("02_CYYY.tif")
    img_cmyk = ImageCms.applyTransform(img, t)
    img_cmyk.save('02_CYYY_CMYK.tif')

def cmyk_srgb():
    t = ImageCms.buildTransform(CMYK, SRGB, "CMYK", "RGB")
    
    img = Image.open("02_CYYY_CMYK.tif")
    img_srgb = ImageCms.applyTransform(img, t)
    img_srgb.save('02_CYYY_SRGB.tif')

srgb_cmyk()
cmyk_srgb()
