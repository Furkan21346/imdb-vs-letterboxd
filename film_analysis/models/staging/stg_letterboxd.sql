SELECT
    rank                         AS lb_rank,
    letterboxd_id,
    title,
    CAST(year AS INT64)             AS release_year,
    genres,
    CAST(rating AS FLOAT64)         AS lb_rating,
    CAST(vote_count AS INT64)       AS lb_vote_count,
    imdb_id,
    CAST(tmdb_id AS INT64)          AS tmdb_id,
    production_countries
FROM `film-analysis-496919.raw.letterboxd_top250`
WHERE title IS NOT NULL