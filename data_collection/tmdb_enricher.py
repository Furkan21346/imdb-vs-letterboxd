import requests # it is used to make HTTP requests to the TMDB API
import pandas as pd  # it is used for data manipulation and analysis
import time # it is used to add delays between API requests to avoid hitting rate limits
import os

# .env dosyasından API anahtarını oku
API_KEY = open('.env').read().strip().split('=')[1] #first open the .env file, read its content, strip any whitespace, split by '=', and take the second part as the API key

def get_movie_details(tmdb_id):
    """Bir film için TMDB'den detay çeker"""
    url = f"https://api.themoviedb.org/3/movie/{int(tmdb_id)}"
    params = {'api_key': API_KEY, 'language': 'en-US'}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'tmdb_id': tmdb_id,
            'budget': data.get('budget', 0),
            'revenue': data.get('revenue', 0),
            'original_language': data.get('original_language', ''),
            'production_countries': str([c['name'] for c in data.get('production_countries', [])]),
            'spoken_languages': str([l['english_name'] for l in data.get('spoken_languages', [])]),
        }
    else:
        return None

# Her iki listeyi oku
print("Listeler okunuyor...")
imdb = pd.read_csv('imdb_top250.csv')
letterboxd = pd.read_csv('letterboxd_top250.csv')

# İki listeden tüm benzersiz TMDB ID'lerini topla
imdb_ids = set(imdb['imdb_id'].dropna().tolist())
lb_tmdb_ids = letterboxd['tmdb_id'].dropna().tolist()
lb_tmdb_ids = [int(x) for x in lb_tmdb_ids]

# IMDb listesindeki filmler için TMDB ID'lerini bul
print("IMDb filmlerinin TMDB ID'leri aranıyor...")
imdb_tmdb_map = {}
for imdb_id in imdb_ids:
    url = "https://api.themoviedb.org/3/find/" + imdb_id
    params = {'api_key': API_KEY, 'external_source': 'imdb_id'}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        results = r.json().get('movie_results', [])
        if results:
            imdb_tmdb_map[imdb_id] = results[0]['id']
    time.sleep(0.1)

# Tüm benzersiz TMDB ID'lerini birleştir
all_tmdb_ids = set(lb_tmdb_ids) | set(imdb_tmdb_map.values()) 
print(f"Toplam sorgulanacak film: {len(all_tmdb_ids)}")

# Her film için detay çek
print("Film detayları çekiliyor...")
results = []
for i, tmdb_id in enumerate(all_tmdb_ids):
    details = get_movie_details(tmdb_id)
    if details:
        results.append(details)
    
    # Her 50 filmde bir ilerlemeyi göster
    if (i + 1) % 50 == 0:
        print(f"{i + 1}/{len(all_tmdb_ids)} film tamamlandı")
    
    time.sleep(0.1)  # Rate limit için bekle

# Sonuçları kaydet
tmdb_df = pd.DataFrame(results)
tmdb_df.to_csv('tmdb_details.csv', index=False)
print(f"\ntmdb_details.csv kaydedildi! ({len(tmdb_df)} film)")