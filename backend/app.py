from flask import Flask
from routes import back_bp, front_bp
from flask_cors import CORS
import webbrowser
from threading import Timer

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
CORS(app)
app.register_blueprint(back_bp, url_prefix='/api')
app.register_blueprint(front_bp)

if __name__ == "__main__":
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
    app.run(debug=True)