
# from flaskblog import app
from renovering import create_app

app = create_app() # här kan man stoppa in en anpassad

if __name__ == "__main__":
    # db.create_all()
    app.debug = True
    app.run()
    
