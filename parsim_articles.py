"""
В этом модуле парсим статьи с другово сайта(https://povar.ru)
 и добавляем в свою базу данных.
"""

from app import Post, db, random_number
from bs4 import BeautifulSoup
import requests

UPLOAD_FOLDER = 'C:/Users/dEniS/djangoPy/den/flaskProject3/static/uploaded'  # Путь по которому загружаем файлы.
inn = ''  # Список индигриентов.


def uploading_an_image(image_url, title_image):
    # Сохраняем полученый файл.
    try:
        resource = requests.get(image_url)  # Получаем картинку.
        with open(f'{UPLOAD_FOLDER}/{title_image}', 'wb')as file:  # Указываем путь для загрузки.
            file.write(resource.content)  # Записывает и закрываем файл.
    except ValueError:
        pass


def url_pages():
    # Формируем URL АДРЕС поста для парсинга информации.
    post = random_number()  # Получаем случайный номер поста.
    url = 'https://povar.ru/recipes/harcho_iz_govyadiny_po-gruzinski-' + f'{post}' + '.html'
    headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                              '(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    return url, headers


def string_den(ing):
    global inn
    # Обрабатываем переданаю строку и добавляем в список.
    try:
        ing_str = ing.text.strip()  # Убераем пробелы слева и справа.
        the_first_part = ing_str.find('  ')  # Первая часть
        the_second_part = ing_str.find('—')  # Вторая часть
        integritty = f'{ing_str[:the_first_part]}   {ing_str[the_second_part:-1]}'  # Получаем название индигриента и
        inn = inn + ',' + integritty
    except ValueError:
        pass


def new_post_db(source_inf0):
    global inn
    soup = BeautifulSoup(source_inf0.text, 'lxml')
    # Заголовок статьи.
    title = soup.find('h1', {'class': 'detailed'}).text
    # Краткое описание статьи.
    info = soup.find('span', {'class': 'detailed_full'}).text.strip()
    # Ингредиенты:
    ingredients = soup.find_all('li', {'itemprop': 'recipeIngredient'})
    for ing in ingredients:
        string_den(ing)
    # Назначения.
    destinations = soup.find_all('span', {'class': 'detailed_tags'})
    for i in destinations:
        qw = i.text
    des = qw.split('/')  # Преобразуем стоку в список.
    des = des[1:6]  # Получем срез нужных элементов
    des = ','.join(des)

    # Полное содержание статьи.
    text_s = soup.find_all('div', {'class': 'detailed_step_description_big'})
    text_post = ''
    for i in text_s:
        text_post = text_post + i.text

    links = soup.find_all('div', attrs={'class': 'bigImgBox'})  # Получаем все куски кода где есть ссылки.
    # В цикле перебираем полученые куски кода.
    for link in links:
        image_url = link.find('img').get('src', '-')  # Получаем ссылку на картинку с поста.
        # Получаем название картинки.(Ссылку разбиваем в список по сиволу '/'
        # и вырезаем последный элемент списка.
        title_image = image_url.split('/')[-1]

    # Передаем ссылку и названия файла для загрузки.
    uploading_an_image(image_url, title_image)

    # Добавляем статью в базу данных.
    new_post = Post(title=title,  # Заголовок статьи.
                    destinations=des,
                    integritty=inn,
                    image_name=title_image,  # Имя картинки
                    info=info,  # Короткая информация о статье.
                    text=text_post)  # Полный текст статьи.
    try:
        db.session.add(new_post)
        db.session.commit()

    except ValueError:
        pass


class Article:
    def __init__(self):
        url, headers = url_pages()
        source_inf0 = requests.get(url, headers=headers, params=None)
        try:
            if source_inf0.status_code == 200:
                new_post_db(source_inf0)
            else:
                pass
        except ConnectionError:
            pass