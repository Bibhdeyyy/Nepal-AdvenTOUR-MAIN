import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load and prepare the dataset
hotels_data = pd.read_csv('data/hotels_in_nepali_city.csv')  # Adjust the path to the location of your CSV file

# Select and normalize relevant features: 'latitude', 'longitude', 'rating'
scaler = MinMaxScaler()
features = hotels_data[['latitude', 'longitude', 'rating']]
features_scaled = scaler.fit_transform(features)

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)"""
    R = 6371  # Radius of earth in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def get_similar_hotels(hotel_name, num_recommendations=5):
    """Find similar hotels based on geographic and rating similarity"""
    if hotel_name not in hotels_data['name'].values:
        return []

    idx = hotels_data.index[hotels_data['name'] == hotel_name].tolist()[0]
    hotel_lat, hotel_lon, hotel_rating = features_scaled[idx]
    distances = []
    for lat, lon, rating in features_scaled:
        geo_distance = haversine(hotel_lat, hotel_lon, lat, lon)
        rating_distance = np.abs(hotel_rating - rating)
        total_distance = geo_distance + (rating_distance * 100)  # Adjust weighting as needed
        distances.append(total_distance)

    hotel_indices = np.argsort(distances)[1:num_recommendations + 1]
    return hotels_data.iloc[hotel_indices][['name', 'address', 'rating']]
