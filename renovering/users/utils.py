
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from renovering import mail 

def save_picture(form_picture):
    # randomisera filnamn på bild .
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) 
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture) # för mindres storlek på bilden.
    i.thumbnail(output_size)
    i.save(picture_path)
    # form_picture.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token(user)
    msg = Message('Password reset request', 
                  sender='noreply@demo.com', 
                  recipients=[user.email])
    msg.body = f'''To Reset your password please visit the following link:
{url_for('reset_token', token=token, _external=True)}

if you did not make this request, simply ignore it.
'''
    mail.send(msg)