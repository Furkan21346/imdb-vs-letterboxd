SELECT
    COALESCE(i.title, l.title)          AS title,
    COALESCE(i.release_year, l.release_year) AS release_year,
    i.imdb_rank,
    i.imdb_rating,
    i.imdb_vote_count,
    l.lb_rank,
    l.lb_rating,
    l.lb_vote_count,
    i.imdb_rating - l.lb_rating         AS rating_diff,
    COALESCE(i.genres, l.genres)        AS genres,
    l.production_countries,
    l.tmdb_id,
    CASE
        WHEN i.title IS NOT NULL AND l.title IS NOT NULL THEN 'Both'
        WHEN i.title IS NOT NULL THEN 'IMDb Only'
        ELSE 'Letterboxd Only'
    END                                 AS list_presence
FROM {{ ref('stg_imdb') }} i
FULL OUTER JOIN {{ ref('stg_letterboxd') }} l
    ON i.imdb_id = l.imdb_id