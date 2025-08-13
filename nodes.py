import math

import comfy


class ImageTransformerResizeToMaxPixels:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "max_pixels": ("INT", {"default": 1, "min": 1, "max": 999999999}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "resize_to_max_pixels"
    CATEGORY = "ImageTransformer"

    def resize_to_max_pixels(self, image, max_pixels):
        _, height, width, _ = image.shape

        cur_pixels = height * width
        if cur_pixels <= max_pixels:
            return (image,)

        scale = math.sqrt(max_pixels / cur_pixels)
        new_w = max(1, int(width * scale))
        new_h = max(1, int(height * scale))

        samples_chw = image.movedim(-1, 1)
        resized_chw = comfy.utils.common_upscale(
            samples_chw, new_w, new_h, "lanczos", "disabled"
        )
        resized_nhwc = resized_chw.movedim(1, -1)

        return (resized_nhwc,)


NODE_CLASS_MAPPINGS = {
    "ImageTransformerResizeToMaxPixels": ImageTransformerResizeToMaxPixels,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageTransformerResizeToMaxPixels": "Image Transformer - Resize to Max Pixels",
}
