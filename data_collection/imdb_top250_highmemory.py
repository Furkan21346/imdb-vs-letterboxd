import pandas as pd

print("IMDb data are loading")

basics = pd.read_csv('title.basics.tsv.gz', sep='\t', na_values='\\N', low_memory=False)
ratings = pd.read_csv('title.ratings.tsv.gz', sep='\t', na_values='\\N')

# Just take movies
movies = basics[basics['titleType'] == 'movie']

# Merge it with ratings
merged = movies.merge(ratings, on='tconst')

# From the movies whose rankings are above 25000, take the largest 250 ones
top250 = merged[merged['numVotes'] >= 25000] \
    .nlargest(250, 'averageRating') \
    .reset_index(drop=True)

top250.index += 1  # Let ranking begin by 0

# The columns we need most will be hold
top250 = top250[['tconst', 'primaryTitle', 'startYear', 'genres', 'runtimeMinutes', 'averageRating', 'numVotes']]
top250.columns = ['imdb_id', 'title', 'year', 'genres', 'runtime_min', 'rating', 'vote_count']

print(top250.head(10))
print(f"\nTotal film: {len(top250)}")

top250.to_csv('imdb_top250.csv', index_label='rank')
print("imdb_top250.csv has been saved!")
