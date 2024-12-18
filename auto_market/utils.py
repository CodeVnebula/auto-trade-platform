from better_profanity import profanity
from PIL import Image

profanity.load_censor_words()
def contains_prohibited_words(text):
    return profanity.contains_profanity(text)

# def add_watermark(original_image_path, 
#                   watermark_image_path,
#                   transparency=100,
#                   watermark_scale=0.5):
#     original = Image.open(original_image_path)
#     watermark = Image.open(watermark_image_path)
    
#     original_width, original_height = original.size
#     watermark_width, watermark_height = watermark.size

#     new_watermark_width = int(original_width * watermark_scale)
#     new_watermark_height = int(
#         (new_watermark_width / watermark_width) * watermark_height
#     )

#     watermark = watermark.resize(
#         (new_watermark_width, new_watermark_height), Image.LANCZOS
#     )

#     watermark = watermark.convert("RGBA")
#     watermark_with_transparency = Image.new("RGBA", watermark.size)
#     for x in range(watermark.width):
#         for y in range(watermark.height):
#             pixel = watermark.getpixel((x, y))
#             if pixel[3] > 0: 
#                 new_pixel = pixel[:3] + (transparency,)
#                 watermark_with_transparency.putpixel((x, y), new_pixel)
#             else:
#                 watermark_with_transparency.putpixel((x, y), pixel)  

#     original_width, original_height = original.size
#     watermark_width, watermark_height = watermark.size

#     position = (
#         (original_width - watermark_width) // 2,
#         (original_height - watermark_height) // 2
#     )

#     original.paste(
#         watermark_with_transparency, 
#         position,
#         watermark_with_transparency
#     )

#     return original
    
# def crop_and_resize_image(image_path, 
#                           target_width=600, 
#                           target_height=400):
#     original = Image.open(image_path)
#     original_width, original_height = original.size
    
#     original_aspect_ratio = original_width / original_height
#     target_aspect_ratio = target_width / target_height

#     if original_aspect_ratio > target_aspect_ratio:
#         new_width = int(original_height * target_aspect_ratio)
#         left = (original_width - new_width) // 2
#         right = left + new_width
#         top = 0
#         bottom = original_height
#     else:
#         new_height = int(original_width / target_aspect_ratio)
#         top = (original_height - new_height) // 2
#         bottom = top + new_height
#         left = 0
#         right = original_width

#     cropped_image = original.crop((left, top, right, bottom))

#     resized_image = cropped_image.resize(
#         (target_width, target_height), Image.LANCZOS
#     )

#     return resized_image
