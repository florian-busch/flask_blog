import os
from flask import current_app as app


def is_allowed_file(sanitized_filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in sanitized_filename and sanitized_filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image, sanitized_filename):
    if is_allowed_file(sanitized_filename):
        try:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], sanitized_filename))
            return True
        except:
            print('Error')
    else:
         print('File typ not allowed')
