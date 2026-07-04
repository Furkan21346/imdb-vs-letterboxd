SELECT
    CAST(tmdb_id AS INT64)          AS tmdb_id,
    CAST(budget AS INT64)           AS budget,
    CAST(revenue AS INT64)          AS revenue,
    original_language,
    production_countries,
    spoken_languages
FROM `film-analysis-496919.raw.tmdb_details`
WHERE tmdb_id IS NOT NULL