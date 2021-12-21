WITH my_friends AS (
    SELECT second_friend_id
    FROM friends WHERE first_friend_id = '6bf4a9ef-643e-4b9a-b91c-6d2cb051e563')
, user_rew AS(
SELECT second_friend_id, user_id, film_id
FROM my_friends JOIN audience_reviews
ON (my_friends.second_friend_id = audience_reviews.user_id
       AND audience_reviews.film_id = '0d00d2a6-6edc-4508-8b5f-f904756d0282'))
SELECT users.user_id, users.fcs FROM users JOIN user_rew ON users.user_id = user_rew.second_friend_id;

-- Друзья написавшие к фильму ревью

