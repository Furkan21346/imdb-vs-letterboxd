import pandas as pd
from google.cloud import bigquery

PROJECT_ID = 'film-analysis-496919'
client = bigquery.Client(project=PROJECT_ID)

files = [
    ('imdb_top250.csv',        'raw.imdb_top250'),
    ('letterboxd_top250.csv',  'raw.letterboxd_top250'),
    ('tmdb_details.csv',       'raw.tmdb_details'),
    ('imdb_tmdb_mapping.csv',  'raw.imdb_tmdb_mapping'),
    ('films_master.csv',       'raw.films_master'),
]

for filename, table_id in files:
    print(f"Uploading {filename} -> {table_id}...")
    
    df = pd.read_csv(filename, engine='python')
    
    full_table_id = f"{PROJECT_ID}.{table_id}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )
    
    job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
    job.result()
    
    table = client.get_table(full_table_id)
    print(f"Done! {table.num_rows} rows uploaded.\n")

print("All tables uploaded successfully!")