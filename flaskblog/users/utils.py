import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # we are splitting the ext (file type) from the file name (f_name)
    # we can store the filename in the _ variable that we will NOT use
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # app.root.path gives us the full path up to the package directory

    output_size = (125, 125)    # tuple specifying dimension in px
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# _external=True gives us an absolute URL rather than a relative URL
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='dzc117@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)