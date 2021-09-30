"""
Contains function that do specific tasks and can be reused
"""
from products.constants import IMAGES_PATH


def image_path(instance, filename):
    """
    Returns the path to store the image file at
    Args:
        instance(Product): Value containing product data
        filename(str): Value containing image filename
    Returns:
        (str): Value containing location to store file
    """
    return f"{IMAGES_PATH}{instance.name}_{filename}"
