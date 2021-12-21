-- персоны из папок в алфавитном порядке

WITH pers AS(
    SELECT person_id
    FROM folders JOIN composition_persons_folder
    ON folders.folder_id = composition_persons_folder.folder_id
    AND folders.user_id = '6bf4a9ef-643e-4b9a-b91c-6d2cb051e563')
SELECT fcs, pers.person_id
FROM persons join pers
ON pers.person_id = persons.person_id
ORDER BY fcs;