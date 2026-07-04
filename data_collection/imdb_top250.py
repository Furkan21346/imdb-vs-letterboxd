import pandas as pd

print("Basics yükleniyor (chunk modunda)...")

chunks = []
for chunk in pd.read_csv('title.basics.tsv.gz', sep='\t', na_values='\\N', 
                          low_memory=False, chunksize=100000):
    # Her chunk'tan sadece filmleri al, gerisi belleğe alınmasın
    movies_chunk = chunk[chunk['titleType'] == 'movie']
    chunks.append(movies_chunk)

basics = pd.concat(chunks, ignore_index=True)
print(f"Film sayısı: {len(basics)}")

print("Ratings yükleniyor...")
ratings = pd.read_csv('title.ratings.tsv.gz', sep='\t', na_values='\\N')

merged = basics.merge(ratings, on='tconst')

top250 = merged[merged['numVotes'] >= 25000] \
    .nlargest(250, 'averageRating') \
    .reset_index(drop=True)

top250.index += 1
top250 = top250[['tconst', 'primaryTitle', 'startYear', 'genres', 'runtimeMinutes', 'averageRating', 'numVotes']]
top250.columns = ['imdb_id', 'title', 'year', 'genres', 'runtime_min', 'rating', 'vote_count']

print(top250.head(10))
print(f"\nToplam film: {len(top250)}")

top250.to_csv('imdb_top250.csv', index_label='rank')
print("imdb_top250.csv kaydedildi!")