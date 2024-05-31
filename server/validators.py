from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_image_size(image):
    if image:
        with Image.open() as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f'the maximum size of image is allowed is 70 * 70 size of image you uplaoded is {image.size}'
                )


def validate_image_file_extensions(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    if extension.lower() not in valid_extensions:
        raise ValidationError(f'file you uploaded  with  {extension} 
                              extension is not valid image file extensiion  valid extensions is {valid_extensions} ')