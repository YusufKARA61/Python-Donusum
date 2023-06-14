from flask import Flask, render_template
from config import UPLOAD_FOLDER

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Diğer front-end işlemleri devam eder...
