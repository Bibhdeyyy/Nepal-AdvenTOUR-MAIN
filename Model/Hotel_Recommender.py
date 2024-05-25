import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

#Load the dataset
file_path = '/content/hotels_in_nepali_city.csv'
hotels_df = pd.read_csv(file_path)
hotels_df

#Display the first few rows of the dataset
hotels_df.head()

#Check for missing values and data types
hotels_df.info()

#Display summary statistics
hotels_df.describe()

#Normalize the ratings
scaler = MinMaxScaler()
hotels_df['normalized_rating'] = scaler.fit_transform(hotels_df[['rating']])

#Log-transform the total ratings to handle skewness
hotels_df['log_total_ratings'] = np.log1p(hotels_df['total_ratings'])

#Display the updated dataframe with new features
hotels_df.head()

#Define a function to recommend hotels based on content-based filtering
def recommend_hotels_content_based(hotel_name, df, top_n=5):
    # Extract relevant features for similarity computation
    features = df[['normalized_rating', 'log_total_ratings']]

    #Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(features, features)

    #Get the index of the hotel
    idx = df[df['name'] == hotel_name].index[0]

    #Get the pairwise similarity scores for the hotel
    sim_scores = list(enumerate(cosine_sim[idx]))

    #Sort the hotels based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #Get the indices of the top-n most similar hotels
    sim_indices = [i[0] for i in sim_scores[1:top_n+1]]

    #Return the top-n most similar hotels
    return df.iloc[sim_indices][['name', 'city', 'rating', 'total_ratings']]

#Example: Recommend hotels similar to "Hotel Shanker Kathmandu"
recommendations = recommend_hotels_content_based("Hotel Shanker Kathmandu", hotels_df)
recommendations

def recommend_hotels_item_based(hotel_name, df, top_n=5):
    # Extract relevant features for similarity computation
    features = df[['latitude', 'longitude', 'rating', 'total_ratings']]

    #Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(features, features)

    #Get the index of the hotel
    idx = df[df['name'] == hotel_name].index[0]

    #Get the pairwise similarity scores for the hotel
    sim_scores = list(enumerate(cosine_sim[idx]))

    #Sort the hotels based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #Get the indices of the top-n most similar hotels
    sim_indices = [i[0] for i in sim_scores[1:top_n+1]]

    #Return the top-n most similar hotels
    return df.iloc[sim_indices][['name', 'city', 'rating', 'total_ratings']]

    #Example: Recommend hotels similar to "Hotel Shanker Kathmandu" using item-based collaborative filtering

item_based_recommendations = recommend_hotels_item_based("Hotel Shanker Kathmandu", hotels_df)
item_based_recommendations