from flask import Flask
from flask_babel import Babel

from web import (admin, admin_page, all_page, dash_board, login_manager,
                 power_page, sw_off_page)

app = Flask('aps')

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['BABEL_DEFAULT_LOCALE'] = 'uk'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Kiev'
babel = Babel(app)


#Дашборд
app.register_blueprint(dash_board)

#Вимкнені комутатори
app.register_blueprint(sw_off_page)

app.register_blueprint(power_page)

app.register_blueprint(all_page)

#Адмін панель
app.register_blueprint(admin_page)
login_manager.init_app(app)
admin.init_app(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
