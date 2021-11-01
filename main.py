import os
from PIL import Image
from qrcode_processing import coder, decoder
from transformation import ProfileConverter


def get_file_list(name_dir):
    extensions = [".tif", ".tiff", ".jpg", ".png"]
    file_list = []
    for root, directories, filenames in os.walk(name_dir):
        for filename in filenames:
            if any(ext in filename for ext in extensions):
                file_list.append(os.path.join(root, filename))
    return file_list


def main():
    profile_path_srgb = "./profiles/SRGB.icm"
    profile_path_cmyk = "./profiles/CMYK.icc"
    name_dir = 'image'

    list_name_img = get_file_list(name_dir)

    converter = ProfileConverter(profile_path_srgb, profile_path_cmyk)

    for file in list_name_img[:1]:
        img = Image.open(file)
        img_cmyk = converter.convert_to_profile(img, "CMYK")
        img_cmyk_qr = coder(img_cmyk)
        img_cmyk_qr.save(f"{os.path.split(file)[1]}.tif")
        # decoder(cord, name_img)


if __name__ == "__main__":
    main()
