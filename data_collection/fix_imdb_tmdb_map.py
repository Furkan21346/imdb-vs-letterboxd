import requests
import pandas as pd
import time

API_KEY = open('.env').read().strip().split('=')[1]

imdb = pd.read_csv('imdb_top250.csv')

print("Finding TMDB IDs for IMDb films...")
rows = []
for i, imdb_id in enumerate(imdb['imdb_id'].dropna()):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}"
    params = {'api_key': API_KEY, 'external_source': 'imdb_id'}
    r = requests.get(url, params=params)
    
    if r.status_code == 200:
        results = r.json().get('movie_results', [])
        if results:
            rows.append({
                'imdb_id': imdb_id,
                'tmdb_id': results[0]['id']
            })
        else:
            rows.append({'imdb_id': imdb_id, 'tmdb_id': None})
    
    if (i + 1) % 50 == 0:
        print(f"{i + 1}/250 done")
    
    time.sleep(0.1)

mapping = pd.DataFrame(rows)
mapping.to_csv('imdb_tmdb_mapping.csv', index=False)
print(f"Saved! {len(mapping)} films mapped.")
print(f"Missing TMDB ID: {mapping['tmdb_id'].isna().sum()}")