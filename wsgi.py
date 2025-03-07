from flaskr import create_app
from flaskr.config.default import DevConfig
from flaskr.database import db
# from flaskr.commands.command_seed import register_commands

app = create_app(DevConfig)

# register_commands(app)

# with app.app_context():
#     db.create_all()
#     print("Databse update sucessfully.")

if __name__=="__main__":
    app.run()