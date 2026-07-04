# IMDb vs Letterboxd: Top 250 Analysis

A data engineering project comparing IMDb and Letterboxd Top 250 film lists, 
analyzing rating differences, genre distributions, and box office performance.

## 🔍 Research Questions

- Do IMDb and Letterboxd users agree on the best films?
- Which genres dominate each platform?
- Are critically acclaimed films also commercially successful?
- Which highly-rated films actually lost money at the box office?

## 📊 Key Findings

- Only **130 films** appear in both lists (~35% overlap)
- IMDb ratings average **0.19 points higher** than Letterboxd
- **64 films** in the top lists lost money at the box office
- Drama dominates both platforms, but Letterboxd favors Animation more
- High ratings show no clear correlation with box office revenue

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| Data Collection | Python, BeautifulSoup, Requests |
| Data Warehouse | Google BigQuery |
| Transformation | dbt |
| Visualization | Looker Studio |
| Version Control | GitHub |

## 📁 Project Structure
├── data_collection/
│   ├── imdb_top250.py          # IMDb dataset processing
│   ├── letterboxd_top250.py    # Letterboxd data extraction
│   ├── tmdb_enricher.py        # TMDB API enrichment
│   ├── fix_imdb_tmdb_map.py    # IMDb to TMDB ID mapping
│   └── create_master.py        # Master dataset creation
├── film_analysis/              # dbt project
│   └── models/
│       ├── staging/            # Data cleaning layer
│       └── mart/               # Analysis layer
└── README.md
## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/Furkan21346/imdb-vs-letterboxd.git
cd imdb-vs-letterboxd
```

### 2. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas requests beautifulsoup4 google-cloud-bigquery dbt-bigquery
```

### 3. Set up environment variables
```bash
echo "TMDB_API_KEY=your_api_key_here" > .env
```

### 4. Run data collection
```bash
python data_collection/imdb_top250.py
python data_collection/letterboxd_top250.py
python data_collection/tmdb_enricher.py
python data_collection/fix_imdb_tmdb_map.py
python data_collection/create_master.py
python data_collection/upload_to_bigquery.py
```

### 5. Run dbt models
```bash
cd film_analysis
dbt run
```

## 📈 Dashboard

[View Live Dashboard] (https://datastudio.google.com/reporting/c78f9f4f-01be-4c12-8382-f24f1d015a6f)

## 📦 Data Sources

- **IMDb** — Official Non-Commercial Dataset (datasets.imdbws.com)
- **Letterboxd** — Kaggle community dataset
- **TMDB** — API for budget, revenue, and metadata