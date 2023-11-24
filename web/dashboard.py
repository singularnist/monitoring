from flask import Blueprint, render_template
from sqlalchemy.orm import sessionmaker
import plotly.express as px
import plotly.io as pio
from datebase import Switches, engine

dash_board = Blueprint('dash_board', __name__)

@dash_board.route('/')
def katalog():
    Session = sessionmaker(bind=engine)
    session_1 = Session()

    row_count = session_1.query(Switches).count()
    row_count_with_stat_0 = session_1.query(Switches).filter(Switches.stat == 0).count()
    row_count_with_stat_1 = session_1.query(Switches).filter(Switches.stat == 1).count()
    
    
    row_count_km = 'В процесі'
    with_stat_0_km = 'В процесі'
    res_km = 100

    session_1.close()
    data = {'labels': ['Включені', 'Вимкнені'],
            'values': [row_count_with_stat_1, row_count_with_stat_0]}
    fig = px.pie(data, names='labels', values='values', title='Вінниця')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',  # Колір тексту
        title_font_color='white'  # Колір тексту заголовку
    )
    plot = pio.to_html(fig, full_html=False)

    data_km = {'labels': ['Включені', 'Вимкнені'],
            'values': [1000, 0]}
    fig_km = px.pie(data_km, names='labels', values='values', title='Хмельницький')
    fig_km.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',  # Колір тексту
        title_font_color='white'  # Колір тексту заголовку
    )
    plot_km = pio.to_html(fig_km, full_html=False)



    return render_template('dashboard.html', plot=plot,plot_km=plot_km,  row_count=row_count, with_stat_0=row_count_with_stat_0,
    row_count_km=row_count_km, with_stat_0_km=with_stat_0_km, res_km=res_km)
