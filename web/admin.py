from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from datebase import AdminUser, History, Switches, session_1, Man,Doing, Problem

admin_page = Blueprint('login', __name__)
login_manager = LoginManager(admin_page)


@login_manager.user_loader
def load_user(user_id):
    return session_1.query(AdminUser).get(int(user_id))

@admin_page.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session_1.query(AdminUser).filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@admin_page.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return super(MyAdminIndexView, self).index()



models = [Switches, AdminUser,History, Man,Doing, Problem]
admin = Admin(admin_page, name='Adminka', template_mode='bootstrap3',  index_view=MyAdminIndexView())
for model in models:
    admin.add_view(ModelView(model, session_1))

