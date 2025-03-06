import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import datetime
import os

# Spotify API credentials
client_id = ''
client_secret = ''

# Configure authentication with Spotify
print("Configuring Spotify authentication...")
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, 
    client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
print("Authentication configured successfully.")

# Load the initial dataset with two columns: Track and Artist
print("Loading the original dataset...")
try:
    input_df = pd.read_csv('dataset.csv')
    print(f"Loaded {len(input_df)} songs")
    print("First 5 rows:")
    print(input_df.head())
except Exception as e:
    print(f"Error loading the file: {e}")
    exit(1)

def get_available_features(artist, track):
    """
    Extract available features for a song using the Spotify API.
    
    This function avoids using endpoints that return 403 errors (audio_features and audio_analysis)
    and instead focuses on metadata, popularity metrics, and derived features.
    
    Args:
        artist (str): Artist name
        track (str): Track name
        
    Returns:
        dict: Dictionary containing all extracted features, or None if the track was not found
    """
    try:
        # Search for the song
        query = f"artist:{artist} track:{track}"
        search_results = sp.search(q=query, type='track', limit=1)
        
        # Check if results were found
        if not search_results['tracks']['items']:
            print(f"Not found: {artist} - {track}")
            return None
        
        # Extract basic data
        track_info = search_results['tracks']['items'][0]
        track_id = track_info['id']
        
        # Build dictionary with available data
        features = {
            # Basic metadata
            'track_name': track,
            'artist_name': artist,
            'album_name': track_info['album']['name'],
            'release_date': track_info['album']['release_date'],
            'popularity': track_info['popularity'],
            'duration_ms': track_info['duration_ms'],
            'explicit': 1 if track_info['explicit'] else 0,
            
            # Album info
            'album_type': track_info['album']['album_type'],
            'total_tracks': track_info['album']['total_tracks'],
            
            # Artist collaboration details
            'artists_count': len(track_info['artists'])
        }
        
        # Process release date and create derived features
        try:
            release_date = track_info['album']['release_date']
            precision = track_info['album']['release_date_precision']
            
            if precision == 'day':
                features['release_year'] = int(release_date.split('-')[0])
                features['release_month'] = int(release_date.split('-')[1])
            elif precision == 'month':
                features['release_year'] = int(release_date.split('-')[0])
                features['release_month'] = int(release_date.split('-')[1])
            elif precision == 'year':
                features['release_year'] = int(release_date)
                features['release_month'] = 1  # Default to January when only year is available
            
            # Calculate age in years
            current_year = datetime.datetime.now().year
            features['years_since_release'] = current_year - features['release_year']
            
            # Categorize by decade
            decade = (features['release_year'] // 10) * 10
            features['decade'] = f"{decade}s"
        except Exception as e:
            print(f"  ℹ️ Error processing release date: {str(e)}")
            features['release_year'] = 0
            features['release_month'] = 0
            features['years_since_release'] = 0
            features['decade'] = 'unknown'
        
        # Get artist data
        try:
            primary_artist_id = track_info['artists'][0]['id']
            artist_info = sp.artist(primary_artist_id)
            
            # Genres
            genres = artist_info.get('genres', [])
            features['genres'] = ','.join(genres) if genres else ''
            
            if genres:
                features['primary_genre'] = genres[0]
            else:
                features['primary_genre'] = 'unknown'
                
            # Popularity and followers
            features['artist_popularity'] = artist_info.get('popularity', 0)
            features['artist_followers'] = artist_info.get('followers', {}).get('total', 0)
        except Exception as e:
            print(f"  ℹ️ Error getting artist data: {str(e)}")
            features['genres'] = ''
            features['primary_genre'] = 'unknown'
            features['artist_popularity'] = 0
            features['artist_followers'] = 0
        
        # Create additional derived features
        features['duration_minutes'] = round(features['duration_ms'] / 60000, 2)
        features['is_single'] = 1 if features['album_type'] == 'single' else 0
        
        # Create popularity categories for supervised learning
        if features['popularity'] >= 75:
            features['popularity_category'] = 'high'
        elif features['popularity'] >= 50:
            features['popularity_category'] = 'medium'
        elif features['popularity'] >= 25:
            features['popularity_category'] = 'low'
        else:
            features['popularity_category'] = 'very_low'
            
        # Create a feature for whether the song is by multiple artists
        features['is_collaboration'] = 1 if features['artists_count'] > 1 else 0
        
        return features
    
    except Exception as e:
        print(f"Error processing {artist} - {track}: {str(e)}")
        return None

def build_enriched_dataset(input_df):
    """
    Build the complete dataset from the input DataFrame
    """
    all_tracks_data = []
    
    # Counter for showing progress
    total_tracks = len(input_df)
    
    for idx, row in input_df.iterrows():
        artist = row['Artist']
        track = row['Track']
        
        # Show progress
        print(f"\nProcessing {idx+1}/{total_tracks}: {artist} - {track}")
        
        # Get data
        track_data = get_available_features(artist, track)
        
        if track_data:
            all_tracks_data.append(track_data)
            print(f"Data successfully obtained")
            
        # Pause to avoid API rate limits
        time.sleep(1)
    
    # Convert to DataFrame and return
    return pd.DataFrame(all_tracks_data)

# Build the dataset
print("\n=== STARTING DATASET ENRICHMENT PROCESS ===")
print("Note: You can add lyrics data to this dataset later")
dataset = build_enriched_dataset(input_df)

# Save final dataset
print("\n=== SAVING FINAL DATASET ===")
dataset.to_csv('enriched_spotify_dataset.csv', index=False)

# Also save as Excel for easier viewing
try:
    dataset.to_excel('enriched_spotify_dataset.xlsx', index=False)
    print("Dataset also saved as Excel file")
except Exception as e:
    print(f"Could not save as Excel: {e}")

# Display dataset statistics
print("\n=== DATASET CREATED SUCCESSFULLY ===")
print(f"Total songs processed: {len(dataset)}")
print(f"Available columns: {dataset.columns.tolist()}")

# Show some basic statistics
print("\nBasic statistics for key features:")
numeric_columns = ['popularity', 'duration_minutes', 'artist_popularity', 'artist_followers']
print(dataset[numeric_columns].describe())

# Show distribution of categorical features
print("\nDistribution of popularity categories:")
print(dataset['popularity_category'].value_counts())

print("\nDistribution of album types:")
print(dataset['album_type'].value_counts())

print("\nTop 10 primary genres:")
print(dataset['primary_genre'].value_counts().head(10))

print("\nProcess completed. The enriched dataset is available in 'enriched_spotify_dataset.csv'")