from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from datebase import History, engine, Man, Doing, Problem

sw_off_page = Blueprint('sw_off_page', __name__)


@sw_off_page.route('/sw_off_page')
def katalog():
    Session = sessionmaker(bind=engine)
    session_1 = Session()
    articles = session_1.query(History).filter(
    History.off_power.isnot(None),
    History.sw_off.isnot(None),
    History.sw_on.is_(None),
    ).order_by(desc(History.sw_off)).all()
    mans= session_1.query(Man).all()
    doings = session_1.query(Doing).all()
    problems = session_1.query(Problem).all()
    return render_template('sw_off.html', articles=articles, mans=mans, doings=doings, problems=problems)

@sw_off_page.route('/edit/<int:id>/<field>', methods=['POST'])
def edit_field(id, field):
    new_value = request.form.get(f'new_{field}')
    Session = sessionmaker(bind=engine)
    session_1 = Session()
    history_entry = session_1.query(History).filter_by(ID=id).first()
    
    # Перевірка, яке поле ви оновлюєте
    if field == 'man':
        history_entry.man = new_value
    elif field == 'doing':
        history_entry.doing = new_value
    elif field == 'comments':
        history_entry.comments = new_value
    elif field == 'problem':
        history_entry.problem = new_value

    session_1.commit()
    session_1.close()
    
    return redirect(url_for('sw_off_page.katalog'))