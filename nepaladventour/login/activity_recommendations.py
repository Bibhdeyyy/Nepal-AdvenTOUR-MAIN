import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from .models import Activity

# Load the dataset for activities in Nepal
activities_file_path = 'login/CSVs/activities_in_nepal.csv'
activities_df = pd.read_csv(activities_file_path)

activities_df.replace('Not available', np.nan, inplace=True)

# Preprocess the data
def preprocess_activities_data(df):
    # Handle missing values and data types
    df['address'].fillna('Unknown', inplace=True)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['total_ratings'] = pd.to_numeric(df['total_ratings'], errors='coerce')
    df['rating'].fillna(df['rating'].mean(), inplace=True)
    df['total_ratings'].fillna(df['total_ratings'].mean(), inplace=True)
    
    # Drop rows with missing values
    df.dropna(inplace=True)
    
    # Normalize the ratings
    scaler = MinMaxScaler()
    df['normalized_rating'] = scaler.fit_transform(df[['rating']])
    
    # Log-transform the total ratings to handle skewness
    df['log_total_ratings'] = np.log1p(df['total_ratings'])

    activities_df.dropna(inplace=True)


# Define a function to recommend activities based on content-based filtering
def recommend_activities_content_based(activity_name, top_n=5):
    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(activities_df[['normalized_rating', 'log_total_ratings']], 
                                    activities_df[['normalized_rating', 'log_total_ratings']])

    # Get the index of the activity
    idx = activities_df[activities_df['name'] == activity_name].index[0]

    # Get the pairwise similarity scores for the activity
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the activities based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top-n most similar activities
    sim_indices = [i[0] for i in sim_scores[1:top_n+1]]

    # Return the top-n most similar activities
    return activities_df.iloc[sim_indices][['name', 'city', 'activity', 'rating', 'total_ratings']]




# Define a function to recommend activities based on item-based collaborative filtering
def recommend_activities_item_based(activity_name, activities_queryset, top_n=5):
    # Convert queryset to DataFrame
    activities_df = pd.DataFrame(list(activities_queryset.values()))

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(activities_df[['latitude', 'longitude', 'rating']], 
                                    activities_df[['latitude', 'longitude', 'rating']])

    # Get the index of the activity
    idx = activities_df[activities_df['name'] == activity_name].index[0]

    # Get the pairwise similarity scores for the activity
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the activities based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top-n most similar activities
    sim_indices = [i[0] for i in sim_scores[1:top_n+1]]

    # Return the top-n most similar activities
    return activities_df.iloc[sim_indices][['name', 'city', 'rating']]





