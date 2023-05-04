import os 

class Config:
    SECRET_KEY ='76b7dbec0285b9d18cee5f2902c4677f' # skall flyttas till environment variabler.
    SQLALCHEMY_DATABASE_URI ='sqlite:///site.db'#iprojektbiblioteket.

    #MAILkonfigurering
    MAIL_SERVER= 'send.one.com'
    MAIL_PORT = '465'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')