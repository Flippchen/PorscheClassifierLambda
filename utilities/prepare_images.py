import io
from PIL import Image, ImageOps, ImageFile
from rembg import remove, new_session
from PIL.Image import Image as PILImage

ImageFile.LOAD_TRUNCATED_IMAGES = True


def replace_background(im: PILImage, post_process_mask=False, session=None) -> PILImage:
    # if not isinstance(im, PILImage):
    #   im = Image.open(io.BytesIO(im))
    session = session or new_session("u2net")
    im = remove(im, post_process_mask=post_process_mask, session=session)
    im = resize_cutout(im)

    new_im = Image.new('RGBA', im.size, 'BLACK')
    new_im.paste(im, mask=im)

    bio = io.BytesIO()
    new_im.save(bio, format='PNG')
    im_bytes = bio.getvalue()
    image = Image.open(io.BytesIO(im_bytes))
    image = image.convert('RGB')

    return image


def get_bounding_box(im: PILImage) -> tuple:
    # Get the data of the image
    im_data = im.getdata()

    # Get the dimensions of the image
    width, height = im.size

    # Find the bounding box
    left, top, right, bottom = width, height, 0, 0
    for y in range(height):
        for x in range(width):
            if im_data[y * width + x][3] > 0:  # If the pixel is not fully transparent
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    return left, top, right, bottom


def resize_cutout(im: PILImage, size: tuple = (300, 300)) -> PILImage:
    # Get the bounding box of the non-transparent content
    left, top, right, bottom = get_bounding_box(im)

    # Crop the image to the bounding box
    im_cropped = im.crop((left, top, right, bottom))

    im_resized = resize_and_pad_image(im_cropped, size, )  # fill_color=(255, 255, 255, 255)

    return im_resized


def resize_and_pad_image(image: PILImage, target_size: tuple, fill_color=(0, 0, 0, 0)):
    # Calculate the aspect ratio of the image
    aspect_ratio = float(image.width) / float(image.height)

    # Calculate the dimensions of the new image
    if aspect_ratio > 1:
        new_width = target_size[0]
        new_height = int(target_size[1] / aspect_ratio)
    else:
        new_width = int(target_size[0] * aspect_ratio)
        new_height = target_size[1]

    # Resize the image while maintaining its aspect ratio
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Calculate padding
    padding_width = target_size[0] - new_width
    padding_height = target_size[1] - new_height

    # Calculate left and top padding to center the image
    left_padding = padding_width // 2
    top_padding = padding_height // 2

    # Pad the image to make it a square and center it
    padded_image = ImageOps.expand(resized_image, (left_padding, top_padding, padding_width - left_padding, padding_height - top_padding), fill=fill_color)

    return padded_image


def fix_image(image):
    # Convert image to RGB if not already
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Fix orientation if necessary
    image = ImageOps.exif_transpose(image)
    return image
