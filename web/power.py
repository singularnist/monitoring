from flask import Blueprint, render_template
from sqlalchemy.orm import sessionmaker

from datebase import Switches, engine

power_page = Blueprint('power', __name__)

@power_page.route('/power')
def katalog():
    return render_template('power.html')
