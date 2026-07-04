import pandas as pd

print("Reading files...")
imdb = pd.read_csv('imdb_top250.csv')
letterboxd = pd.read_csv('letterboxd_top250.csv')
tmdb = pd.read_csv('tmdb_details.csv')
mapping = pd.read_csv('imdb_tmdb_mapping.csv')

# Add TMDB ID to IMDb list via mapping
imdb = imdb.merge(mapping, on='imdb_id', how='left')

# Convert tmdb_id to numeric across all dataframes
imdb['tmdb_id'] = pd.to_numeric(imdb['tmdb_id'], errors='coerce')
letterboxd['tmdb_id'] = pd.to_numeric(letterboxd['tmdb_id'], errors='coerce')
tmdb['tmdb_id'] = pd.to_numeric(tmdb['tmdb_id'], errors='coerce')

# Enrich IMDb list with TMDB details
imdb_enriched = imdb.merge(tmdb, on='tmdb_id', how='left')
imdb_enriched = imdb_enriched.rename(columns={
    'rating': 'imdb_rating',
    'vote_count': 'imdb_vote_count',
    'rank': 'imdb_rank'
})

# Enrich Letterboxd list with TMDB details
lb_enriched = letterboxd.merge(tmdb, on='tmdb_id', how='left')
lb_enriched = lb_enriched.rename(columns={
    'rating': 'lb_rating',
    'vote_count': 'lb_vote_count',
    'rank': 'lb_rank'
})

# Merge both lists via full outer join on TMDB ID
master = imdb_enriched.merge(
    lb_enriched[['tmdb_id', 'lb_rating', 'lb_vote_count', 'lb_rank', 'letterboxd_id']],
    on='tmdb_id',
    how='outer'
)

# Profit/loss calculation
master['studio_revenue'] = master['revenue'] * 0.5
master['total_cost'] = master['budget'] * 1.5
master['estimated_profit'] = master['studio_revenue'] - master['total_cost']
master['financial_status'] = master['estimated_profit'].apply(
    lambda x: 'PROFIT' if pd.notna(x) and x > 0
    else ('LOSS' if pd.notna(x) and x <= 0 else 'NO_DATA')
)

# Identify which list each film belongs to
master['list_presence'] = master.apply(
    lambda row: 'Both' if pd.notna(row.get('imdb_rank')) and pd.notna(row.get('lb_rank'))
    else ('IMDb Only' if pd.notna(row.get('imdb_rank'))
    else 'Letterboxd Only'), axis=1
)

print("\n--- SUMMARY ---")
print(f"Total unique films: {len(master)}")
print(f"\nList distribution:")
print(master['list_presence'].value_counts())
print(f"\nFinancial status:")
print(master['financial_status'].value_counts())
print(f"\nFirst 5 rows:")
print(master[['title', 'imdb_rating', 'lb_rating', 'budget', 'revenue', 'financial_status', 'list_presence']].head())

master.to_csv('films_master.csv', index=False)
print("\nfilms_master.csv saved!")