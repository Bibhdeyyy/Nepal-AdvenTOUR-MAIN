import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
file_path = 'login/CSVs/hotels_in_nepali_city.csv'
hotels_df = pd.read_csv(file_path, encoding = 'latin1')

# Ensure 'id' is present
if 'id' not in hotels_df.columns:
    hotels_df['id'] = range(1, len(hotels_df) + 1)

# Normalize the ratings
scaler = MinMaxScaler()
hotels_df['normalized_rating'] = scaler.fit_transform(hotels_df[['rating']])

# Log-transform the total ratings to handle skewness
hotels_df['log_total_ratings'] = np.log1p(hotels_df['total_ratings'])

def recommend_hotels_content_based(hotel_name, top_n=5):
    if hotel_name not in hotels_df['name'].values:
        return []  # Return an empty list if the hotel name is not found
    
    features = hotels_df[['normalized_rating', 'log_total_ratings']]
    cosine_sim = cosine_similarity(features, features)
    idx = hotels_df[hotels_df['name'] == hotel_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_indices = [i[0] for i in sim_scores[1:top_n+1]]
    return hotels_df.iloc[sim_indices]['id'].tolist()  # Return list of IDs


def recommend_hotels_item_based(hotel_name, top_n=5):
    # Normalize the hotel name for comparison
    hotel_name = hotel_name.lower()
    
    # Check if the hotel name exists in the DataFrame
    if hotel_name not in hotels_df['name'].str.lower().values:
        return []

    # Find the hotel with the given name
    hotel = hotels_df[hotels_df['name'].str.lower() == hotel_name].iloc[0]
    
    # Exclude the current hotel
    other_hotels = hotels_df[hotels_df['place_id'] != hotel['place_id']]
    
    # Normalize the features
    other_hotels['rating_normalized'] = (other_hotels['rating'] - other_hotels['rating'].min()) / (other_hotels['rating'].max() - other_hotels['rating'].min())
    hotel_rating_normalized = (hotel['rating'] - other_hotels['rating'].min()) / (other_hotels['rating'].max() - other_hotels['rating'].min())

    # Calculate the distance (example, assuming 'latitude' and 'longitude' columns exist)
    hotel_location = np.array([hotel['latitude'], hotel['longitude']])
    other_hotels['distance'] = other_hotels.apply(lambda row: np.linalg.norm(hotel_location - np.array([row['latitude'], row['longitude']])), axis=1)
    other_hotels['distance_normalized'] = (other_hotels['distance'] - other_hotels['distance'].min()) / (other_hotels['distance'].max() - other_hotels['distance'].min())
    
    # Calculate the similarity score (example weights: rating - 0.5, distance - 0.5)
    rating_weight = 0.5
    distance_weight = 0.5
    other_hotels['similarity_score'] = rating_weight * (1 - np.abs(other_hotels['rating_normalized'] - hotel_rating_normalized)) + distance_weight * (1 - other_hotels['distance_normalized'])
    
    # Sort by similarity score
    recommended_hotels = other_hotels.sort_values(by='similarity_score', ascending=False).head(top_n)

    return recommended_hotels[['name', 'place_id', 'rating', 'phone_number', 'distance']]