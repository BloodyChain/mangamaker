import sqlite3
from io import BytesIO

from FDataBase import FDataBase
from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g, make_response, send_file

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [{'url': './', 'title': 'Панель'},
        {'url': './list-users', 'title': 'Список пользователей'},
        {'url': './add_post', 'title': 'Добавить статью'},
        {'url': './logout', 'title': 'Выход'}]


db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT id, title, type, img FROM posts")
            list = cur.fetchall()

        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/index.html', title="Главная", menu = menu, list = list)


@admin.route('/login', methods=['POST', 'GET'])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == 'POST':
        if request.form['user'] == "Jeremy" and request.form['psw'] == "alterego":
            login_admin()
            return redirect(url_for(".index"))
        else:
            flash("Неверная пара логин/пароль", category="error")
    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('index'))


@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT id, name, email, status FROM users ORDER BY time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/listusers.html', title="Список пользователей", menu = menu, list = list)

@admin.route("/add_post", methods=["POST", "GET"])
def addPost():

    if not isLogged():
        return redirect(url_for('.login'))
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['type']) > 3:
            file = request.files.get('file', None)
            img = file.read()
            res = dbase.addPost(request.form['name'], request.form['type'], img)
            if not res:
                flash('Ошибка добавления статьи', category = 'error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('admin/add_post.html', menu = menu, title="Добавление статьи")

@admin.route('/get_image/<int:img_id>', methods=['GET'])
def get_image(img_id):
    cur = db.cursor()
    cur.execute(f"SELECT img FROM posts WHERE id LIKE '{img_id}'")
    sps = cur.fetchone()
    return send_file(BytesIO(sps[0]), mimetype='image/png')

@admin.route('/delete_post/<int:img_id>')
def delete_post(img_id):
    cur = db.cursor()
    cur.execute(f"DELETE FROM posts WHERE id LIKE '{img_id}'")
    db.commit()
    return redirect(url_for('.index'))

@admin.route('/block_user/<int:user_id>')
def block_user(user_id):
    cur = db.cursor()
    cur.execute(f"UPDATE users SET status = 'Blocked' WHERE id LIKE '{user_id}'")
    db.commit()
    return redirect(url_for('.listusers'))

@admin.route('/unblock_user/<int:user_id>')
def unblock_user(user_id):
    cur = db.cursor()
    cur.execute(f"UPDATE users SET status = 'Active' WHERE id LIKE '{user_id}'")
    db.commit()
    return redirect(url_for('.listusers'))