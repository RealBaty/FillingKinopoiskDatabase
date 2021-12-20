import random
import string
import time

import psycopg2
import json
import io
from psycopg2 import OperationalError


class KinopoiskData:
    mpaas = []
    films = []
    countries = []
    genres = []
    review_types = []
    roles = []
    names = []
    surnames = []
    gender = []
    cash_id = {}
    folder_type = []

    def __init__(self):
        self.folder_type = ["film", "person", "reviews"]
        self.mpaas = [
            ("G", "Фильм демонстрируется без ограничений. Данный рейтинг показывает, что оценённый фильм "
                  "не содержит ничего, что большинство родителей могло бы посчитать неприемлемым для "
                  "просмотра или прослушивания даже самыми маленькими детьми. Обнажение, сексуальные "
                  "сцены и сцены приёма наркотиков отсутствуют; насилие минимально; могут употребляться "
                  "выражения, выходящие за пределы вежливой беседы, но только те, которые постоянно "
                  "встречаются в повседневной речи. Более грубая лексика в фильмах с рейтингом G "
                  "употребляться не может."),
            ("PG", "Детям рекомендуется смотреть фильм с родителями. Некоторые материалы могут "
                   "не подходить для детей. Этот рейтинг показывает, что родители могут найти "
                   "некоторые из сцен в фильме неподходящими для детей и что родителям "
                   "рекомендуется посмотреть фильм, прежде чем показывать его детям. Явные "
                   "сексуальные сцены и сцены употребления наркотиков отсутствуют; нагота, "
                   "если присутствует, только в очень ограниченной степени, могут быть "
                   "использованы лёгкие ругательства и представлены сцены насилия, но только в "
                   "очень умеренных количествах."),
            ("PG-13",
             "Просмотр не желателен детям до 13 лет. Данный рейтинг показывает, что оценённый фильм может быть "
             "неподходящим для детей. Родители должны быть особенно осторожны, разрешая своим маленьким детям "
             "просмотр. Может присутствовать умеренное или грубое насилие; могут присутствовать сцены с наготой; "
             "возможны ситуации с сексуальным контекстом; могут присутствовать некоторые сцены употребления "
             "наркотиков; можно услышать единичные употребления грубых ругательств. "),
            ("R",
             "Лица, не достигшие 17-летнего возраста, допускаются на фильм только в сопровождении одного из "
             "родителей, либо законного представителя. Данный рейтинг показывает, что оценочная комиссия заключила, "
             "что некоторый материал оценённого фильма предназначается только для взрослых. Родители должны больше "
             "узнать о фильме, прежде чем взять на его просмотр подростков. Рейтинг R может быть назначен из-за "
             "частого употребления непристойной лексики продолжительных сцен насилия, полового акта или употребления"
             " наркотиков. "),
            ("NC-17", "Лица 17-летнего возраста и младше на фильм не допускаются. Данный рейтинг показывает, "
                      "что оценочная комиссия полагает, что по мнению большинства родителей фильм явно для взрослых, "
                      "и детей до 17 лет нельзя допускать до просмотра. Фильм может содержать явные сексуальные сцены, "
                      "большое количество непристойной и сексуальной лексики, или сцен чрезмерного насилия. Рейтинг "
                      "NC-17, однако, ещё не означает, что данный фильм является непристойным или порнографическим, "
                      "как в повседневном, так и в юридическом смысле этих слов. ")
        ]
        self.films = open("films.txt", "r", encoding="utf-8").read().split("\n\n")
        for i in range(0, len(self.films)):
            self.films[i] = self.films[i].split(" / ")[0]
        self.countries = ["Россия", "Китай", "Япония", "США", "Великобритания", "Испания", "Италия", "Индия",
                          "Республика Корея", "Белорусь", "Украина", "Франция"]
        self.genres = ["коммедия", "боевик", "драмма", "экшн", "мелодрамма", "исторический", "документальный",
                       "ограбление", "криминал", "фантастика", "спортивный"]
        self.review_types = ["+", "-", "+-"]
        self.roles = ["режисер", "актер", "сценарист", "художник", "композитор", "главный редактор", "звукорежессер",
                      "продюссер", "оператор", "монтаж"]
        with open("russian_names.json", "r", encoding='utf-8-sig') as read_file:
            convert_json = json.load(read_file)
        self.names = []
        for name in convert_json:
            self.names.append(name['Name'])
        with open("russian_surnames.json", "r", encoding='utf-8-sig') as read_file:
            convert_json = json.load(read_file)
        self.surnames = []
        for surname in convert_json:
            self.surnames.append(surname['Surname'])
        self.gender = ["Мужской", "Женский"]
        self.cash_id = {}

    def generate_random_folder_type(self):
        return random.choice(self.folder_type)

    def generate_random_countries(self, a):
        return random.sample(self.countries, a)

    def generate_random_country(self):
        return random.choice(self.countries)

    def generate_random_genres(self, a):
        return random.sample(self.genres, a)

    def generate_random_gender(self):
        return random.choice(self.gender)

    def generate_random_fcs(self):
        return f"{random.choice(self.surnames)} {random.choice(self.names)}"

    def generate_random_fcs_list(self, a):
        res = []
        for i in range(a):
            res.append(f"{random.choice(self.surnames)} {random.choice(self.names)}")
        return res

    def generate_random_id(self, table, table_id):
        if not (table in self.cash_id):
            connection = create_connection("kinopoisk", "postgres", "u8d12255", "localhost", "5432")
            cursor = connection.cursor()
            cursor.execute(f"SELECT DISTINCT {table_id} FROM {table}")
            self.cash_id[table] = cursor.fetchall()
        if self.cash_id[table]:
            return random.choice(self.cash_id[table])[0]
        return None


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        connection.autocommit = True
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def generate_random_string(length1, length2):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(random.randint(length1, length2)))
    return rand_string


def generate_random_array(func, length1, length2):
    res = ""
    length = random.randint(length1, length2)
    if length == 0:
        return "None"
    for i in func(length):
        if res != "":
            res = res + ", "
        res = res + '"' + i + '"'
    res = "{" + res + "}"
    return res


def generate_random_array_of_str(func, length1, length2):
    res = ""
    length = random.randint(length1, length2)
    if length == 0:
        return "None"
    for i in range(length):
        if res != "":
            res = res + ", "

        res = res + func()
    res = "{" + res + "}"
    return res


def generate_date():
    start = "1/1/1978 1:30 PM"
    end = "1/1/2021 4:50 AM"
    date_format = '%d-%m-%Y'
    date_format1 = '%m/%d/%Y %I:%M %p'
    prop = random.random()
    stime = time.mktime(time.strptime(start, date_format1))
    etime = time.mktime(time.strptime(end, date_format1))
    ptime = stime + prop * (etime - stime)
    return time.strftime(date_format, time.localtime(ptime))


def generate_time():
    start = "1/1/1978 1:30 PM"
    end = "1/1/2021 4:50 AM"
    date_format = '%I:%M'
    date_format1 = '%m/%d/%Y %I:%M %p'
    prop = random.random()
    stime = time.mktime(time.strptime(start, date_format1))
    etime = time.mktime(time.strptime(end, date_format1))
    ptime = stime + prop * (etime - stime)
    return time.strftime(date_format, time.localtime(ptime)) + ":00"


def generate_many():
    return str(random.randint(0, 10000000000)) + "." + str(random.randint(0, 9)) + str(random.randint(0, 9))


def generate_grade():
    return str(random.randint(0, 10))


def main():
    connection = create_connection("kinopoisk", "postgres", "u8d12255", "localhost", "5432")
    cursor = connection.cursor()
    sources = KinopoiskData()
    for mpaa in sources.mpaas:
        cursor.execute(f"INSERT INTO mpaa (mpaa_title, mpaa_description) VALUES (%s, %s)", mpaa)
    for film in sources.films:
        cursor.execute(f"INSERT INTO films (film_title, film_description, countries, production_date, slogan, "
                       f"poster, premiere, age_restrictions, budget, duration, mpaa, trailer, grade, fees, "
                       f"genres) VALUES ('{film}', '{generate_random_string(30, 100)}', "
                       f"'{generate_random_array_of_str(sources.generate_random_countries, 1, 5)}', '"
                       f"{generate_date()}', '{generate_random_string(30, 100)}', "
                       f"'{generate_random_string(30, 100)}', '{generate_date()}', {random.randint(0, 18)}, "
                       f"{generate_many()}, '{generate_time()}', '{sources.generate_random_id('mpaa', 'mpaa_id')}', '"
                       f"{generate_random_string(5, 40)}', '{generate_random_array(generate_grade, 1, 100)}', "
                       f"{generate_many()}, '{generate_random_array_of_str(sources.generate_random_genres, 1, 9)}')")
        '''cursor.execute(f"INSERT INTO films (film_title, film_description, countries, production_date, slogan, "
                       f"poster, premiere, age_restrictions, budget, duration, mpaa, trailer, grade, fees, "
                       f"genres) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (film, 
                                                                                                        generate_random_string(30, 100), ))'''
    for i in range(1000):
        cursor.execute(f"INSERT INTO critics_reviews (film_id, review_type, title, content, likes, dislikes, "
                       f"creation_date, link, critic, resource) VALUES ('"
                       f"{sources.generate_random_id('films', 'film_id')}', "
                       f"'{random.choice(sources.review_types)}', '{generate_random_string(1, 40)}', "
                       f"'{generate_random_string(1, 400)}', {random.randint(0, 1000000)}, "
                       f"{random.randint(0, 1000000)}, '{generate_date()}', '{generate_random_string(5, 50)}', "
                       f"'{sources.generate_random_fcs()}', '{generate_random_string(3, 30)}')")
    for i in range(2000):
        cursor.execute(f"INSERT INTO persons (FCs, photo, height, birthdate, place_of_birth, spouses) VALUES ('"
                       f"{sources.generate_random_fcs()}', '{generate_random_string(2, 50)}', "
                       f"{random.randint(90, 250)}, '{generate_date()}', '"
                       f"{generate_random_array_of_str(sources.generate_random_countries, 1, 5)}', "
                       f"'{generate_random_array_of_str(sources.generate_random_fcs_list, 1, 5)}')")
    for i in range(2000):
        cursor.execute(f"INSERT INTO users (FCs, password, number, email, avatar, login, interests, gender, "
                       f"birthdate, country, city, vk_link, facebook_link, twitter_link) VALUES ('"
                       f"{sources.generate_random_fcs()}', '{generate_random_string(8, 30)}', "
                       f"'{generate_random_string(6, 8)}', '{generate_random_string(4, 30)}', "
                       f"'{generate_random_string(2, 50)}', '{generate_random_string(4, 50)}', "
                       f"'{generate_random_string(1, 200)}', '{sources.generate_random_gender()}', '"
                       f"{generate_date()}', '{sources.generate_random_country()}', '{generate_random_string(4, 30)}', "
                       f"'{generate_random_string(4, 40)}', '{generate_random_string(4, 40)}', "
                       f"'{generate_random_string(4, 40)}')")
    for i in range(1000):
        cursor.execute(f"INSERT INTO audience_reviews (film_id, user_id, review_type, title, content, likes, dislikes, "
                       f"creation_date, link) VALUES ('"
                       f"{sources.generate_random_id('films', 'film_id')}', "
                       f"'{sources.generate_random_id('users', 'user_id')}', "
                       f"'{random.choice(sources.review_types)}', '{generate_random_string(1, 40)}', "
                       f"'{generate_random_string(1, 400)}', {random.randint(0, 1000000)}, "
                       f"{random.randint(0, 1000000)}, '{generate_date()}', '{generate_random_string(5, 50)}')")
    for i in range(1000):
        cursor.execute(f"INSERT INTO friends (first_friend_id, second_friend_id) VALUES ('"
                       f"{sources.generate_random_id('users', 'user_id')}', '"
                       f"{sources.generate_random_id('users', 'user_id')}')")
    for i in range(1000):
        cursor.execute(f"INSERT INTO folders (user_id, title, folder_type, sort, description, subscribe_to_updates) "
                       f"VALUES ('{sources.generate_random_id('users', 'user_id')}', '"
                       f"{generate_random_string(1, 30)}', '{sources.generate_random_folder_type()}', "
                       f"'{generate_random_string(1,25)}', '{generate_random_string(1, 300)}', "
                       f"{random.choice(['true', 'false'])})")



if __name__ == '__main__':
    main()
