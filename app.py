# Importing the necessary modules and libraries
from flask import Flask


def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_object('config')  # Configuring from Python Files
    return app


app = create_app()  # Creating the app


if __name__ == '__main__':  # Running the app
    app.run()