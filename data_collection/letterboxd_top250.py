import pandas as pd

print("Letterboxd verisi yükleniyor...")

df = pd.read_csv('movie_data.csv', engine='python')

print(f"Toplam kayıt: {len(df)}")

# Temizle: puanı ve oy sayısı olmayanları at
df = df[df['vote_average'] > 0]
df = df[df['vote_count'] > 0]

# En az 1000 oy almış filmleri al (gürültüyü azaltmak için)
df = df[df['vote_count'] >= 1000]

# En yüksek puanlı 250 filmi al
top250 = df.nlargest(250, 'vote_average').reset_index(drop=True)
top250.index += 1

# Sadece işimize yarayacak kolonları tut
top250 = top250[[
    'movie_id', 'movie_title', 'year_released',
    'vote_average', 'vote_count', 'genres',
    'production_countries', 'imdb_id', 'tmdb_id'
]]

top250.columns = [
    'letterboxd_id', 'title', 'year',
    'rating', 'vote_count', 'genres',
    'production_countries', 'imdb_id', 'tmdb_id'
]

print(top250.head(10))
print(f"\nToplam film: {len(top250)}")

top250.to_csv('letterboxd_top250.csv', index_label='rank')
print("letterboxd_top250.csv kaydedildi!")