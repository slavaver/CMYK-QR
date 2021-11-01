from PIL import Image, ImageCms


class ProfileConverter:

    def __init__(self, profile_path_srgb, profile_path_cmyk):
        self.transformer_cmyk_rgb = ImageCms.buildTransform(profile_path_cmyk, profile_path_srgb, "CMYK", "RGB")
        self.transformer_rgb_cmyk = ImageCms.buildTransform(profile_path_srgb, profile_path_cmyk, "RGB", "CMYK")

    def convert_to_profile(self, original_img, destination_space):
        if destination_space not in ['RGB', 'CMYK']:
            raise ValueError('Wrong destination space. Should be RGB or CMYK.')
        else:
            if destination_space == 'RGB':
                img = ImageCms.applyTransform(original_img, self.transformer_cmyk_rgb)
            elif destination_space == 'CMYK':
                img = ImageCms.applyTransform(original_img, self.transformer_rgb_cmyk)
        return img
