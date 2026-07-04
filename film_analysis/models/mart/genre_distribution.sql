SELECT
    TRIM(genre)                                                                   AS genre,
    COUNT(CASE WHEN list_presence IN ('Both', 'IMDb Only') THEN 1 END)           AS imdb_count,
    COUNT(CASE WHEN list_presence IN ('Both', 'Letterboxd Only') THEN 1 END)     AS lb_count,
    ROUND(AVG(CASE WHEN imdb_rating IS NOT NULL THEN imdb_rating END), 2)        AS avg_imdb_rating,
    ROUND(AVG(CASE WHEN lb_rating IS NOT NULL THEN lb_rating END), 2)            AS avg_lb_rating
FROM {{ ref('film_comparison') }},
UNNEST(SPLIT(REPLACE(REPLACE(REPLACE(genres, '[', ''), ']', ''), '"', ''), ',')) AS genre
WHERE genres IS NOT NULL
GROUP BY genre
ORDER BY imdb_count DESC