SELECT
    rank                        AS imdb_rank,
    imdb_id,
    title,
    CAST(year AS INT64)         AS release_year,
    genres,
    CAST(runtime_min AS INT64)  AS runtime_min,
    CAST(rating AS FLOAT64)     AS imdb_rating,
    CAST(vote_count AS INT64)   AS imdb_vote_count
FROM `film-analysis-496919.raw.imdb_top250`
WHERE title IS NOT NULL