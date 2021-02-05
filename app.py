from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import threading
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogKuh.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fegBCXtf8denisfegBCXtf8'
db = SQLAlchemy(app)

the_name_of_the_site = 'Куринария всего мира.'
post_db = ''


def automatic_addition_of_articles():
    # Добавляем новые статьи на сайт.
    threading.Timer(3600, automatic_addition_of_articles).start()  # Добавляем новую статью
    # каждый 1 час.
    Article()  # Вызываем класс из другово модуля.


def random_number():
    number = random.randint(0, 22188)
    return number


class Post(db.Model):
    # Создаем колонки в базе данных.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    destinations = db.Column(db.String(100), nullable=False)
    integritty = db.Column(db.String(100), nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id


from parsim_articles import Article


def we_get_the_nickname_and_password_from_the_database():
    global post_db
    # Получаем полную информацию статей.
    # И добавляем из в список.
    post_db = Post.query.order_by(Post.date.desc()).all()


@app.route('/')
# Обрабаттываем главную страницу.
def name():
    we_get_the_nickname_and_password_from_the_database()  # Получаем все статьи с базы.
    automatic_addition_of_articles()  # Запускаем парсинг статьи в отдельном потоке.
    return render_template('base.html', title=f'Добро пожаловать на сайта '
                                              f'{the_name_of_the_site}', main=post_db)


@app.route('/post', methods=['GET', 'POST'])
# Обрабатываем страницу новой статьи.
def post():
    #  Если метод POST,тогда получаем данные из формы
    if request.method == 'POST':
        title_post = request.form['title']  # Получаем данные поля
        # title из формы через методом request
        info = request.form['info']  # Получаем данные поля
        # info из формы через методом request
        text = request.form['text']  # Получаем данные поля
        # text из формы через методом request

        # Добавляем статью в базу данных.
        new_post = Post(title=title_post, info=info, text=text)
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Статья добавлена.')
            return redirect('/')  # Перенаправляем на главную страницу.

        except ValueError:
            pass

        return render_template('base.html')
    else:
        # Если метод GET,тогда отображаем форму.
        return render_template('post.html', title='Новая статья.')


@app.route('/<int:id_post>')
# Обрабаттываем главную страницу.
def full_text_of_the_article(id_post):
    # Выполняем запрос к базе данных по определеному id
    info = Post.query.get(id_post)
    return render_template('full_text_of_the_article.html', info=info)


@app.route('/photo')
def photo():
    return render_template('404.html'), 404


@app.route('/news')
def news():
    return render_template('404.html'), 404


@app.errorhandler(404)
def mistake(error):
    # В этой функции обрабатываем ошибку 404
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
