# Popular Paraguayan Songs Dataset Documentation

## General Description

This dataset contains detailed information about the 200 most popular songs listened to in Paraguay, according to data collected from streaming platforms. The main objective is to provide a dataset that allows for the analysis of musical characteristics and popularity metrics of songs that are successful in the Paraguayan market, enabling the study of musical patterns and trends in this region.

## Data Sources

### Data Sources Used

The dataset was built using multiple sources:

1. **Initial list of popular songs**: 
   - Source: [Kworb.net](https://www.kworb.net/spotify/country/py_daily.html)
   - Names of 200 popular songs and their corresponding artists were extracted from Paraguay's popular playlists.

2. **Song metadata and characteristics**:
   - Source: Spotify API
   - The spotipy library (Python) was used to access the Spotify API and obtain detailed information about each song, including album, release date, popularity, duration, and more.

3. **Audio features**:
   - Source: [songdata.io](https://songdata.io)
   - Audio features were extracted such as tempo (BPM), acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, and valence.

### Data Collection Process

1. **Phase 1: Initial List Extraction**
   - An initial list with two columns was extracted: "Track" and "Artist" from popular playlists in Paraguay on Kworb.net.

2. **Phase 2: Enrichment with Spotify API**
   - A Python script was developed using the spotipy library to query the Spotify API.
   - For each track-artist pair, detailed information was searched and extracted using Spotify's search endpoint.
   - Metadata such as popularity, release date, duration, album, etc. was extracted.
   - Derived features were created such as "decade", "years_since_release", and "popularity_category".

3. **Phase 3: Addition of Audio Features**
   - The data was complemented using songdata.io to obtain specific audio features.
   - These features include attributes such as tempo, acousticness, danceability, energy, etc.

4. **Phase 4: Data Cleaning and Validation**
   - The redundant 'all_artists' column was removed since it contained the same information as 'artist_name'
   - Missing values in the genres column were filled with the primary genre or "unknown"
   - The consistency of all numerical and categorical features was verified.

## Dataset Composition

### Size and Structure

- **Number of rows (songs)**: 200
- **Number of columns (features)**: 31

### Dataset Features

| Column | Data Type | Description |
|---------|--------------|-------------|
| track_name | String | Name of the song |
| artist_name | String | Name of the artist(s) |
| album_name | String | Name of the album |
| release_date | String | Release date (YYYY-MM-DD) |
| popularity | Integer | Spotify popularity index (0-100) |
| duration_ms | Integer | Duration in milliseconds |
| explicit | Integer | Explicit content indicator (0=No, 1=Yes) |
| album_type | String | Type of album (single, album, compilation) |
| total_tracks | Integer | Total number of tracks in the album |
| artists_count | Integer | Number of artists participating in the song |
| release_year | Integer | Year of release |
| release_month | Integer | Month of release |
| years_since_release | Integer | Years elapsed since release |
| decade | String | Decade of release (e.g., "2020s") |
| genres | String | Genres of the main artist, comma-separated |
| primary_genre | String | Main genre of the artist |
| artist_popularity | Integer | Popularity index of the main artist (0-100) |
| artist_followers | Integer | Number of followers of the main artist on Spotify |
| duration_minutes | Float | Duration in minutes |
| is_single | Integer | Indicator if it's a single (0=No, 1=Yes) |
| popularity_category | String | Popularity category (very_low, low, medium, high) |
| is_collaboration | Integer | Indicator of collaboration between multiple artists (0=No, 1=Yes) |
| bpm | Integer | Tempo of the song in beats per minute |
| acousticness | Float | Measure of acousticness (0.0-1.0) |
| danceability | Float | Measure of how danceable the song is (0.0-1.0) |
| energy | Integer | Energy level of the song (1-10) |
| instrumentalness | Float | Instrumental vs. vocal proportion (0.0-1.0) |
| liveness | Float | Detection of live audience presence (0.0-1.0) |
| loudness | Float | Overall volume in dB (typically between -60 and 0) |
| speechiness | Float | Presence of spoken words (0.0-1.0) |
| valence | Float | Musical positivity (0.0=negative, 1.0=positive) |

### Data Distribution

#### Popularity Categories
```
popularity_category
medium      91
high        84
low         22
very_low     3
```

#### Album Types
```
album_type
album          122
single          74
compilation      4
```

#### Top 10 Primary Genres
```
primary_genre
reggaeton         91
grupera           21
unknown           12
argentine trap     9
rkt                7
trap latino        7
cumbia             6
vallenato          5
k-pop              4
cumbia norteña     4
```

#### Decade Distribution
```
decade
2020s    125
2010s     49
2000s     19
1990s      7
```

### Numerical Features Statistics

| Feature | Minimum | Maximum | Mean |
|----------------|--------|--------|-------|
| popularity | 9 | 96 | 69.91 |
| duration_ms | 121,375 | 462,561 | 213,105.86 |
| bpm | 73 | 202 | 119.06 |
| acousticness | 0.00239 | 0.897 | 0.25 |
| danceability | 0.328 | 0.924 | 0.70 |
| energy | 1 | 10 | 6.70 |
| loudness | -26.802 | -2.055 | -6.17 |
| valence | 0.0337 | 0.971 | 0.62 |

## Sample Records

Below are some representative examples of records from the dataset:

```
track_name: +57
artist_name: KAROL G, Feid, DFZM, Ovy On The Drums, J Balvin, Maluma, Ryan Castro, Blessd
album_name: +57
release_date: 2024-11-08
popularity: 80
genres: reggaeton,latin,urbano latino
primary_genre: reggaeton
popularity_category: high
bpm: 92
danceability: 0.848
energy: 7
```

```
track_name: 30 Grados
artist_name: El Turko, Mandale Flow
album_name: 30 Grados
release_date: 2024-01-25
popularity: 60
genres: rkt,turreo,guaracha
primary_genre: rkt
popularity_category: medium
bpm: 98
danceability: 0.676
energy: 6
```

## Limitations and Considerations

1. **Regional Representativeness**: This dataset focuses specifically on popular songs in Paraguay, so it may not be representative of global music trends.

2. **Temporality**: The data reflects popularity at the time of collection (March 2025) and may change over time.

3. **Missing Genre Data**: 12 records initially had no genre information, which was filled using the primary genre or labeled as "unknown".

4. **API Limitations**: The extracted information depends on the availability and accuracy of the data in the Spotify API and songdata.io.

## Potential Applications

This dataset can be used for:

1. **Classification**: Predicting the popularity category based on audio features and metadata.

2. **Regression**: Predicting the numerical popularity value using audio features.

3. **Clustering**: Grouping similar songs based on audio characteristics to discover patterns.

4. **Trend Analysis**: Investigating which musical characteristics are associated with greater popularity in Paraguay.

5. **Regional Comparisons**: Comparing with similar datasets from other countries to identify regional preferences.

## References

1. Spotify API: https://developer.spotify.com/documentation/web-api
2. Kworb.net: https://www.kworb.net/spotify/country/py_daily.html
3. songdata.io: https://songdata.io
4. spotipy Library: https://spotipy.readthedocs.io/
