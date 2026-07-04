SELECT
    f.title,
    f.release_year,
    f.imdb_rating,
    f.lb_rating,
    f.list_presence,
    t.budget,
    t.revenue,
    ROUND(t.revenue * 0.5, 0)                    AS studio_revenue,
    ROUND(t.budget * 1.5, 0)                     AS total_cost,
    ROUND((t.revenue * 0.5) - (t.budget * 1.5), 0) AS estimated_profit,
    CASE
        WHEN t.budget IS NULL OR t.budget = 0 THEN 'NO_DATA'
        WHEN (t.revenue * 0.5) > (t.budget * 1.5) THEN 'PROFIT'
        ELSE 'LOSS'
    END                                          AS financial_status,
    t.original_language,
    t.production_countries
FROM {{ ref('film_comparison') }} f
LEFT JOIN {{ ref('stg_tmdb') }} t
    ON f.tmdb_id = t.tmdb_id