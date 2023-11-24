from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import desc, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from datebase import History, Switches, engine, Man, Doing,Problem

all_page = Blueprint('all', __name__)


@all_page.route('/all', methods=['GET', 'POST'])
def katalog():
    Session = sessionmaker(bind=engine)
    session_1 = Session()

    # Значення за замовчуванням для діапазону дат
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2)

    if request.method == 'POST':
        # Отримайте дати з форми, якщо вони були відправлені
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        # Додайте один день до початкової дати, щоб включити її у фільтр
        start_date = start_date - timedelta(days=1)
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d') + timedelta(days=1)

    articles = session_1.query(History).filter(
        History.date >= start_date, History.date <= end_date,
        History.sw_off.isnot(None)).order_by(desc(History.sw_off)).all()
    mans = session_1.query(Man).all()
    doings = session_1.query(Doing).all()
    problems = session_1.query(Problem).all()
    return render_template('all.html', articles=articles, mans=mans, problems=problems, doings=doings, start_date=start_date, end_date=end_date)

@all_page.route('/all/edit/<int:id>/<field>', methods=['POST'])
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
    # Зберегти зміни у базі даних
    session_1.commit()
    session_1.close()
    
    return redirect(url_for('all.katalog'))