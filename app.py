from models import *
import db

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app_screen = LogInScreen()


