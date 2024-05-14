import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer


class RecommendationSystem:
    def __init__(self, df):
        self.df = df

    def collaborative_filtering(self, user_id, num_recommendations=5):
        user_profile = self.df.loc[self.df['User ID'] == user_id]

        # Extract relevant features for collaborative filtering
        user_features = user_profile[['Primary Fitness Goal', 'Physical Activity Level']]
        all_features = self.df[['Primary Fitness Goal', 'Physical Activity Level']]

        # Concatenate user features with all features
        concatenated_features = pd.concat([user_features, all_features])

        # Encode categorical variables
        encoder = OneHotEncoder(drop='first', handle_unknown='ignore')
        encoded_features = encoder.fit_transform(concatenated_features)

        # Split encoded features back into user and all features
        user_features_encoded = encoded_features[:1]
        all_features_encoded = encoded_features[1:]

        # Compute similarity between the target user and all users
        similarities = cosine_similarity(user_features_encoded, all_features_encoded)[0]

        # Find most similar users
        similar_users_indices = similarities.argsort()[::-1][1:]  # Exclude the target user
        similar_users = self.df.iloc[similar_users_indices]

        # Generate recommendations based on similar users' preferences
        recommendations = {
            'Nutritional Preferences': similar_users['Nutritional Preferences'].tolist()[:num_recommendations],
            'Fitness Environment': similar_users['Fitness Environment'].tolist()[:num_recommendations]
        }
        return recommendations

    def content_based_filtering(self, user_id, num_recommendations=5):
        user_profile = self.df.loc[self.df['User ID'] == user_id]

        # Extract user preferences
        user_preferences = user_profile[['Primary Fitness Goal', 'Physical Activity Level', 'Nutritional Preferences', 'Fitness Environment', 'Time Commitment']]

        # Extract item features
        item_features = self.df[['Primary Fitness Goal', 'Physical Activity Level', 'Nutritional Preferences', 'Fitness Environment', 'Time Commitment']]

        # Encode user preferences
        mlb = MultiLabelBinarizer()
        user_features_encoded = mlb.fit_transform(user_preferences.values)

        # Encode item features
        item_features_encoded = mlb.transform(item_features.values)

        # Compute similarity between items and user preferences
        similarities = cosine_similarity(user_features_encoded, item_features_encoded)

        # Sort items based on similarity and recommend top ones
        similar_items_indices = similarities.argsort()[0][::-1]
        recommendations = {
            'Fitness Environment': self.df.iloc[similar_items_indices]['Fitness Environment'].tolist()[:num_recommendations],
            'Nutritional Preferences': self.df.iloc[similar_items_indices]['Nutritional Preferences'].tolist()[:num_recommendations],
        }

        return recommendations
