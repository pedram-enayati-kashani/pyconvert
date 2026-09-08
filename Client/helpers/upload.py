import os
import datetime


def upload_image_to_path(instance, filename, sub_folder):
    name, ext = os.path.splitext(filename)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{name}_{timestamp}{ext}"
    return os.path.join(sub_folder, datetime.datetime.now().strftime('%Y/%m/%d'), new_filename)
