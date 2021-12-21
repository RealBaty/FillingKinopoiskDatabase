import random
import string
import time

import psycopg2
import json


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
        self.folder_type = ["films", "persons", "reviews"]
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
        self.review_types = ["+", "-", "="]
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
        if a == 0:
            return None
        return random.sample(self.countries, a)

    def generate_random_country(self):
        return random.choice(self.countries)

    def generate_random_genres(self, a):
        if a == 0:
            return None
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

    def generate_random_roles(self, a):
        return random.sample(self.roles, a)


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
    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query, insert_elem=None):
    cursor = connection.cursor()
    try:
        if insert_elem:
            cursor.execute(query, insert_elem)
        else:
            cursor.execute(query)
    except Exception as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query, insert_elem=None):
    cursor = connection.cursor()
    try:
        if insert_elem:
            cursor.execute(query, insert_elem)
            result = cursor.fetchall()
            return result
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")


def generate_random_string(length1, length2):
    letters = string.ascii_lowercase
    length = random.randint(length1, length2)
    if length == 0:
        return None
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def generate_random_list(func, length1, length2):
    res = []
    length = random.randint(length1, length2)
    if length == 0:
        return None
    for i in range(length):
        res.append(func())
    return res


def generate_random_list_not_null(func, length1, length2):
    res = []
    length = random.randint(length1, length2)
    for i in range(length):
        res.append(func())
    return res


def generate_grade():
    return random.randint(0, 10)


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


def generate_timestamp():
    start = "1/1/1978 1:30 PM"
    end = "1/1/2021 4:50 AM"
    date_format = '%d-%m-%Y %I:%M:%S'
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


def fill_mpaa(sources, connection):
    for mpaa in sources.mpaas:
        execute_query(connection, f"INSERT INTO mpaa (mpaa_title, mpaa_description) VALUES (%s, %s)", mpaa)


def fill_films(sources, connection):
    for film in sources.films:
        inserts_elem = dict()
        inserts_elem["film_title"] = film
        inserts_elem["film_description"] = generate_random_string(0, 1000)
        inserts_elem["countries"] = sources.generate_random_countries(random.randint(1, 5))
        inserts_elem["production_date"] = generate_date()
        inserts_elem["slogan"] = generate_random_string(0, 400)
        inserts_elem["poster"] = generate_random_string(0, 200)
        inserts_elem["premiere"] = generate_date()
        inserts_elem["age_restrictions"] = random.randint(0, 18)
        inserts_elem["budget"] = random.uniform(0, 10000000000)
        inserts_elem["duration"] = generate_time()
        inserts_elem["mpaa"] = sources.generate_random_id("mpaa", "mpaa_id")
        inserts_elem["trailer"] = generate_random_string(0, 200)
        inserts_elem["grade"] = generate_random_list_not_null(generate_grade, 0, 1000000)
        inserts_elem["fees"] = random.uniform(0, 10000000000)
        inserts_elem["genres"] = sources.generate_random_genres(random.randint(0, 9))
        execute_query(connection, f"INSERT INTO films (film_title, film_description, countries, production_date, "
                                  f"slogan, poster, premiere, age_restrictions, budget, duration, mpaa, trailer, "
                                  f"grade, fees, genres) VALUES (%(film_title)s, %(film_description)s, "
                                  f"%(countries)s, %(production_date)s, %(slogan)s, %(poster)s, %(premiere)s, "
                                  f"%(age_restrictions)s, %(budget)s, %(duration)s, %(mpaa)s, %(trailer)s, "
                                  f"%(grade)s, %(fees)s, %(genres)s)", inserts_elem)


def fill_critics_reviews(sources, connection):
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["film_id"] = sources.generate_random_id('films', 'film_id')
        inserts_elem["review_type"] = random.choice(sources.review_types)
        inserts_elem["title"] = generate_random_string(1, 40)
        inserts_elem["content"] = generate_random_string(1, 400)
        inserts_elem["likes"] = random.randint(0, 1000000)
        inserts_elem["dislikes"] = random.randint(0, 1000000)
        inserts_elem["creation_date"] = generate_timestamp()
        inserts_elem["link"] = generate_random_string(7, 200)
        inserts_elem["critic"] = sources.generate_random_fcs()
        inserts_elem["resource"] = generate_random_string(1, 30)
        execute_query(connection, f"INSERT INTO critics_reviews (film_id, review_type, title, content, likes, "
                                  f"dislikes, creation_date, link, critic, resource) VALUES (%(film_id)s, "
                                  f"%(review_type)s, %(title)s, %(content)s, %(likes)s, %(dislikes)s, "
                                  f"%(creation_date)s, %(link)s, %(critic)s, %(resource)s)", inserts_elem)


def fill_persons(sources, connection):
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["FCs"] = sources.generate_random_fcs()
        inserts_elem["photo"] = generate_random_string(0, 200)
        inserts_elem["height"] = random.randint(70, 300)
        inserts_elem["birthdate"] = generate_date()
        inserts_elem["place_of_birth"] = random.choice(sources.countries)
        inserts_elem["spouses"] = generate_random_list(sources.generate_random_fcs, 0, 10)
        execute_query(connection, f"INSERT INTO persons (FCs, photo, height, birthdate, place_of_birth, "
                                  f"spouses) VALUES (%(FCs)s, %(photo)s, %(height)s, %(birthdate)s, "
                                  f"%(place_of_birth)s, %(spouses)s)", inserts_elem)


def fill_users(sources, connection):
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["FCs"] = sources.generate_random_fcs()
        inserts_elem["password"] = generate_random_string(8, 30)
        inserts_elem["number"] = generate_random_string(2, 14)
        inserts_elem["email"] = generate_random_string(5, 50)
        inserts_elem["avatar"] = generate_random_string(0, 200)
        inserts_elem["login"] = generate_random_string(2, 50)
        inserts_elem["interests"] = generate_random_string(0, 1000)
        inserts_elem["gender"] = sources.generate_random_gender()
        inserts_elem["birthdate"] = generate_date()
        inserts_elem["country"] = sources.generate_random_country()
        inserts_elem["city"] = generate_random_string(0, 30)
        inserts_elem["vk_link"] = generate_random_string(0, 50)
        inserts_elem["facebook_link"] = generate_random_string(0, 50)
        inserts_elem["twitter_link"] = generate_random_string(0, 50)
        execute_query(connection, f"INSERT INTO users (FCs, password, number, email, avatar, login, interests, "
                                  f"gender, birthdate, country, city, vk_link, facebook_link, twitter_link) VALUES ("
                                  f"%(FCs)s, %(password)s, %(number)s, %(email)s, %(avatar)s, %(login)s, "
                                  f"%(interests)s, %(gender)s, %(birthdate)s, %(country)s, %(city)s, %(vk_link)s, "
                                  f"%(facebook_link)s, %(twitter_link)s)", inserts_elem)


def fill_audience_reviews(sources, connection):
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["film_id"] = sources.generate_random_id('films', 'film_id')
        inserts_elem["user_id"] = sources.generate_random_id('users', 'user_id')
        inserts_elem["review_type"] = random.choice(sources.review_types)
        inserts_elem["title"] = generate_random_string(1, 40)
        inserts_elem["content"] = generate_random_string(1, 5000)
        inserts_elem["likes"] = random.randint(0, 100000000)
        inserts_elem["dislikes"] = random.randint(0, 100000000)
        inserts_elem["creation_date"] = generate_timestamp()
        inserts_elem["link"] = generate_random_string(7, 200)
        execute_query(connection, f"INSERT INTO audience_reviews (film_id, user_id, review_type, title, content, "
                                  f"likes, dislikes, creation_date, link) VALUES (%(film_id)s, %(user_id)s, "
                                  f"%(review_type)s, %(title)s, %(content)s, %(likes)s, %(dislikes)s, "
                                  f"%(creation_date)s, %(link)s)", inserts_elem)


def fill_friends(sources, connection):
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["first_friend_id"] = sources.generate_random_id('users', 'user_id')
        inserts_elem["second_friend_id"] = sources.generate_random_id('users', 'user_id')
        execute_query(connection, f"INSERT INTO friends (first_friend_id, second_friend_id) VALUES (%("
                                  f"first_friend_id)s, %(second_friend_id)s)", inserts_elem)


def fill_folders(sources, connection):
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["user_id"] = sources.generate_random_id('users', 'user_id')
        inserts_elem["title"] = generate_random_string(1, 40)
        inserts_elem["folder_type"] = sources.generate_random_folder_type()
        inserts_elem["sort"] = generate_random_string(1, 25)
        inserts_elem["description"] = generate_random_string(1, 400)
        inserts_elem["subscribe_to_updates"] = bool(random.randint(0, 1))
        execute_query(connection, f"INSERT INTO folders (user_id, title, folder_type, sort, description, "
                                  f"subscribe_to_updates) VALUES (%(user_id)s, %(title)s, %(folder_type)s,"
                                  f" %(sort)s, %(description)s, %(subscribe_to_updates)s)", inserts_elem)


def fill_composition_films_folder(sources, connection):
    folders = execute_read_query(connection, "SELECT DISTINCT folder_id FROM folders WHERE folder_type = 'films'")
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["film_id"] = sources.generate_random_id("films", "film_id")
        inserts_elem["folder_id"] = random.choice(folders)[0]
        execute_query(connection, f"INSERT INTO composition_films_folder (film_id, folder_id) VALUES (%(film_id)s,  "
                                  f"%(folder_id)s)", inserts_elem)


def fill_composition_persons_folder(sources, connection):
    folders = execute_read_query(connection, "SELECT DISTINCT folder_id FROM folders WHERE folder_type = 'persons'")
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["person_id"] = sources.generate_random_id("persons", "person_id")
        inserts_elem["folder_id"] = random.choice(folders)[0]
        execute_query(connection, f"INSERT INTO composition_persons_folder (person_id, folder_id) VALUES (%("
                                  f"person_id)s, %(folder_id)s)", inserts_elem)


def fill_composition_reviews_folder(sources, connection):
    folders = execute_read_query(connection, "SELECT DISTINCT folder_id FROM folders WHERE folder_type = 'reviews'")
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["audience_review_id"] = sources.generate_random_id("audience_reviews", "audience_review_id")
        inserts_elem["folder_id"] = random.choice(folders)[0]
        execute_query(connection, f"INSERT INTO composition_reviews_folder (audience_review_id, folder_id) VALUES ("
                                  f"%(audience_review_id)s, %(folder_id)s)", inserts_elem)


def fill_comments(sources, connection):
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["audience_review_id"] = sources.generate_random_id("audience_reviews", "audience_review_id")
        inserts_elem["user_id"] = sources.generate_random_id("users", "user_id")
        inserts_elem["title"] = generate_random_string(0, 50)
        inserts_elem["content"] = generate_random_string(1, 1000)
        inserts_elem["likes"] = random.randint(0, 1000000)
        inserts_elem["dislikes"] = random.randint(0, 1000000)
        inserts_elem["creation_date"] = generate_timestamp()
        execute_query(connection, f"INSERT INTO comments (audience_review_id, user_id, title, content, likes, "
                                  f"dislikes, creation_date) VALUES (%(audience_review_id)s, %(user_id)s, %(title)s,"
                                  f" %(content)s, %(likes)s, %(dislikes)s, %(creation_date)s)", inserts_elem)
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["critics_review_id"] = sources.generate_random_id("critics_reviews", "critics_review_id")
        inserts_elem["user_id"] = sources.generate_random_id("users", "user_id")
        inserts_elem["title"] = generate_random_string(0, 50)
        inserts_elem["content"] = generate_random_string(1, 1000)
        inserts_elem["likes"] = random.randint(0, 1000000)
        inserts_elem["dislikes"] = random.randint(0, 1000000)
        inserts_elem["creation_date"] = generate_date()
        execute_query(connection, f"INSERT INTO comments (critics_review_id, user_id, title, content, likes, "
                                  f"dislikes, creation_date) VALUES (%(critics_review_id)s, %(user_id)s, %(title)s, "
                                  f"%(content)s, %(likes)s, %(dislikes)s, %(creation_date)s)", inserts_elem)
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["references_comment_id"] = sources.generate_random_id("comments", "comment_id")
        inserts_elem["user_id"] = sources.generate_random_id("users", "user_id")
        inserts_elem["title"] = generate_random_string(0, 50)
        inserts_elem["content"] = generate_random_string(1, 1000)
        inserts_elem["likes"] = random.randint(0, 1000000)
        inserts_elem["dislikes"] = random.randint(0, 1000000)
        inserts_elem["creation_date"] = generate_date()
        execute_query(connection, f"INSERT INTO comments (references_comment_id, user_id, title, content, likes, "
                                  f"dislikes, creation_date) VALUES (%(references_comment_id)s, %(user_id)s, "
                                  f"%(title)s, %(content)s, %(likes)s, %(dislikes)s, %(creation_date)s)", inserts_elem)


def fill_composition_of_film(sources, connection):
    for i in range(1000):
        inserts_elem = dict()
        inserts_elem["film_id"] = sources.generate_random_id("films", "film_id")
        inserts_elem["person_id"] = sources.generate_random_id("persons", "person_id")
        inserts_elem["roles"] = random.choice(sources.roles)
        execute_query(connection, f"INSERT INTO composition_of_film (film_id, person_id, roles) VALUES (%(film_id)s, "
                                  f"%(person_id)s, %(roles)s)", inserts_elem)


def main():
    connection = create_connection("kinopoisk", "postgres", "u8d12255", "localhost", "5432")
    sources = KinopoiskData()
    '''fill_mpaa(sources, connection)
    fill_films(sources, connection)
    fill_critics_reviews(sources, connection)
    fill_persons(sources, connection)
    fill_users(sources, connection)
    fill_audience_reviews(sources, connection)'''
    fill_friends(sources, connection)
    '''fill_folders(sources, connection)
    fill_composition_films_folder(sources, connection)
    fill_composition_persons_folder(sources, connection)
    fill_composition_reviews_folder(sources, connection)
    fill_comments(sources, connection)
    fill_composition_of_film(sources, connection)'''


if __name__ == '__main__':
    main()
