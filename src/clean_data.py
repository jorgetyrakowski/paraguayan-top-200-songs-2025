import pandas as pd
import numpy as np

def clean_dataset(input_file_path, output_file_path):
    """
    Cleans the popular songs dataset from Paraguay by fixing specific issues:
    1. Removes the redundant 'all_artists' column
    2. Fills missing genres with the primary genre or 'unknown'
    
    Args:
        input_file_path: Path to the input CSV file
        output_file_path: Path where the cleaned CSV will be saved
    """
    # Load the dataset
    print(f"Loading dataset from {input_file_path}")
    df = pd.read_csv(input_file_path)
    
    # Display initial information
    print(f"Original dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 1. Remove the redundant 'all_artists' column if it exists
    if 'all_artists' in df.columns:
        print("Removing redundant 'all_artists' column")
        df = df.drop('all_artists', axis=1)
    
    # 2. Fill missing genres
    null_genres_before = df['genres'].isna().sum()
    print(f"Songs with missing genres: {null_genres_before}")
    
    if null_genres_before > 0:
        # For each row with null genre, use the primary genre or 'unknown'
        for idx, row in df[df['genres'].isna()].iterrows():
            if pd.notna(row['primary_genre']) and row['primary_genre'] != 'unknown':
                df.at[idx, 'genres'] = row['primary_genre']
            else:
                df.at[idx, 'genres'] = 'unknown'
    
    null_genres_after = df['genres'].isna().sum()
    print(f"Songs with missing genres after correction: {null_genres_after}")
    
    # Save the cleaned dataset
    print(f"Saving cleaned dataset to {output_file_path}")
    df.to_csv(output_file_path, index=False)
    
    # Display final information
    print(f"Cleaned dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print("Cleaning completed successfully.")
    
    return df

if __name__ == "__main__":
    # File paths - adjust as needed
    input_file = "dataset_completo.csv"
    output_file = "dataset_completo_clean.csv"
    
    # Run the cleaning process
    clean_df = clean_dataset(input_file, output_file)
    
    # Show first rows of the cleaned dataset
    print("\nFirst 5 rows of the cleaned dataset:")
    print(clean_df.head())