from flask import Flask, request,render_template,Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import datetime





core = Blueprint('core', __name__, template_folder='templates')


@core.route("/")
def home():
    return  render_template('index.html') 