WITH my_person AS(
    SELECT person_id
    FROM composition_persons_folder LEFT JOIN folders
    ON composition_persons_folder.folder_id = folders.folder_id
    AND folders.user_id = '6bf4a9ef-643e-4b9a-b91c-6d2cb051e563')
, my_role AS(
    SELECT composition_of_film_id
    FROM my_person JOIN composition_of_film
        ON my_person.person_id = composition_of_film.person_id AND
           composition_of_film.film_id = '0d00d2a6-6edc-4508-8b5f-f904756d0282')
SELECT COUNT(*) FROM my_role;

--Количество ролей занимаемых персонами в папке