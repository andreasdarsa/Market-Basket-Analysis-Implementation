from flask import Flask
from routes import routes_blueprint

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)