CREATE TABLE IF NOT EXISTS public."mpaa"
(
    mpaa_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    mpaa_title varchar(10) CHECK ( mpaa_title in ('G', 'PG', 'PG-13', 'R', 'NC-17') )NOT NULL ,
    mpaa_description text
);

CREATE TABLE IF NOT EXISTS public."films"
(
    film_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    film_title varchar(150) NOT NULL ,
    film_description text ,
    countries varchar(150)[] NOT NULL ,
    production_date date ,
    slogan text ,
    poster text ,
    premiere date ,
    age_restrictions integer ,
    budget money ,
    duration time ,
    mpaa uuid REFERENCES mpaa(mpaa_id) ,
    trailer text ,
    grade smallint[] NOT NULL ,
    fees money ,
    genres varchar(15)[]
);

CREATE TABLE IF NOT EXISTS public."critics_reviews"
(
    critics_review_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    film_id uuid REFERENCES films(film_id) NOT NULL ,
    review_type varchar(10) CHECK ( review_type in ('+', '-', '=') ) NOT NULL ,
    title text NOT NULL ,
    content text NOT NULL ,
    likes integer CHECK ( likes >= 0 ) NOT NULL ,
    dislikes integer CHECK ( dislikes >= 0 ) NOT NULL ,
    creation_date timestamp NOT NULL ,
    link text NOT NULL ,
    critic text NOT NULL ,
    resource text NOT NULL
);

CREATE TABLE IF NOT EXISTS public."persons"
(
    person_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    FCs text NOT NULL ,
    photo text ,
    height smallint CHECK ( ( height is NULL ) OR ( height > 0 AND height < 500 )) ,
    birthdate date ,
    place_of_birth text ,
    spouses text[]
);

CREATE TABLE IF NOT EXISTS public."users"
(
    user_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    FCs text NOT NULL ,
    password text NOT NULL ,
    number varchar(14) ,
    email text NOT NULL ,
    avatar text ,
    login text NOT NULL ,
    interests text ,
    gender varchar(10) ,
    birthdate date ,
    country varchar(50) ,
    city varchar(50) ,
    vk_link text ,
    facebook_link text ,
    twitter_link text ,
    UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public."audience_reviews"
(
    audience_review_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    film_id uuid REFERENCES films(film_id) NOT NULL ,
    user_id uuid REFERENCES users(user_id) NOT NULL ,
    review_type varchar(10) CHECK ( review_type in ('+', '-', '=') ) NOT NULL ,
    title text NOT NULL ,
    content text NOT NULL ,
    likes integer CHECK ( likes >= 0 ) NOT NULL ,
    dislikes integer CHECK ( dislikes >= 0 ) NOT NULL ,
    creation_date timestamp NOT NULL ,
    link text NOT NULL
);

CREATE TABLE IF NOT EXISTS public."friends"
(
    friends_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    first_friend_id uuid REFERENCES users(user_id) NOT NULL ,
    second_friend_id uuid REFERENCES users(user_id) NOT NULL,
    UNIQUE (first_friend_id, second_friend_id)
);

CREATE TABLE IF NOT EXISTS public."folders"
(
    folder_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    user_id uuid REFERENCES users(user_id) NOT NULL ,
    title text NOT NULL ,
    folder_type varchar(25) NOT NULL ,
    sort text ,
    description text NOT NULL ,
    subscribe_to_updates boolean NOT NULL ,
    UNIQUE (user_id, title, folder_type)
);

CREATE TABLE IF NOT EXISTS public."composition_films_folder"
(
    composition_films_folder_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    film_id uuid REFERENCES films(film_id) NOT NULL ,
    folder_id uuid REFERENCES folders(folder_id) NOT NULL ,
    UNIQUE (film_id, folder_id)
);

CREATE TABLE IF NOT EXISTS public."composition_persons_folder"
(
    composition_person_folders_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    person_id uuid REFERENCES persons(person_id) NOT NULL ,
    folder_id uuid REFERENCES folders(folder_id) NOT NULL ,
    UNIQUE (person_id, folder_id)
);

CREATE TABLE IF NOT EXISTS public."composition_reviews_folder"
(
    composition_reviews_folder_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    audience_review_id uuid REFERENCES audience_reviews(audience_review_id) NOT NULL ,
    folder_id uuid REFERENCES folders(folder_id) NOT NULL ,
    UNIQUE (audience_review_id, folder_id)
);

CREATE TABLE IF NOT EXISTS public."comments"
(
    comment_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    audience_review_id uuid REFERENCES audience_reviews(audience_review_id) ,
    critics_review_id uuid REFERENCES critics_reviews(critics_review_id) ,
    references_comment_id uuid REFERENCES comments(comment_id) ,
    user_id uuid REFERENCES users(user_id) NOT NULL ,
    title text ,
    content text NOT NULL ,
    likes integer CHECK ( likes >= 0 ) NOT NULL ,
    dislikes integer CHECK ( dislikes >= 0 ) NOT NULL ,
    creation_date timestamp NOT NULL ,
    CONSTRAINT check_one_parent CHECK ( (audience_review_id IS NOT NULL AND critics_review_id IS NULL AND
                                         references_comment_id IS NULL) OR (audience_review_id IS NULL AND
                                                                             critics_review_id IS NOT NULL AND
                                                                            references_comment_id IS NULL) OR
                                        (audience_review_id IS NULL AND critics_review_id IS NULL AND
                                         references_comment_id IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS public."composition_of_film"
(
    composition_of_film_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY ,
    film_id uuid REFERENCES films(film_id) NOT NULL ,
    person_id uuid REFERENCES persons(person_id) NOT NULL ,
    roles varchar(25) NOT NULL ,
    UNIQUE (film_id, person_id, roles)
);