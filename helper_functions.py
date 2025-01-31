import os
from flask import current_app as app


def save_image(image, sanitized_filename):
    try:
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], sanitized_filename))
        return True
    except FileExistsError:
        print('FileExistsError')
        return False
