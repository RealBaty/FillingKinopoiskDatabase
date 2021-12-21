SELECT fcs
FROM composition_of_film JOIN persons
ON composition_of_film.person_id = persons.person_id AND
   composition_of_film.film_id = 'deef7771-b529-487d-acfb-eeeea1e037fc'