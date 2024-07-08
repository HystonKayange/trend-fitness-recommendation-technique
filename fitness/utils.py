import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, mean_absolute_error, mean_squared_error
from user.models import Profile

class RecommendationSystem:
    def __init__(self, df):
        self.df = df
        self.mlb = MultiLabelBinarizer()
        self.mlb.fit(df[['Primary Fitness Goal', 'Physical Activity Level', 'Nutritional Preferences', 'Fitness Environment', 'Time Commitment']].values.flatten())

    def collaborative_filtering(self, user_id, num_recommendations=5):
        user_profile = self.df.loc[self.df['Id'] == user_id]

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


        recommendations = {
            'Nutritional Preferences': list(set([tuple(x) if isinstance(x, list) else x for x in similar_users['Nutritional Preferences'].tolist()[:num_recommendations]])),
            'Fitness Environment': list(set([tuple(x) if isinstance(x, list) else x for x in similar_users['Fitness Environment'].tolist()[:num_recommendations]]))
        }        
        return recommendations

    def content_based_filtering(self, user_id, num_recommendations=5):
        user_profile = self.df.loc[self.df['Id'] == user_id]

        # Extract user preferences
        user_preferences = user_profile[['Primary Fitness Goal', 'Physical Activity Level', 'Nutritional Preferences', 'Fitness Environment', 'Time Commitment']]

        # Extract item features
        item_features = self.df[['Primary Fitness Goal', 'Physical Activity Level', 'Nutritional Preferences', 'Fitness Environment', 'Time Commitment']]

        # Encode user preferences and item features using the same fitted MultiLabelBinarizer
        user_features_encoded = self.mlb.transform(user_preferences.values.flatten().reshape(1, -1))
        item_features_encoded = self.mlb.transform(item_features.values.flatten().reshape(len(item_features), -1))

        # Compute similarity between items and user preferences
        similarities = cosine_similarity(user_features_encoded, item_features_encoded)

        # Sort items based on similarity and recommend top ones
        similar_items_indices = similarities.argsort()[0][::-1]
        
        recommendations = {
            'Fitness Environment': list(set([tuple(x) if isinstance(x, list) else x for x in self.df.iloc[similar_items_indices]['Fitness Environment'].tolist()[:num_recommendations]])),
            'Nutritional Preferences': list(set([tuple(x) if isinstance(x, list) else x for x in self.df.iloc[similar_items_indices]['Nutritional Preferences'].tolist()[:num_recommendations]])),
        }
        return recommendations

    def evaluate_recommendations(self, recommendations, actual_preferences):
        precision_list = []
        recall_list = []
        f1_list = []
        mae_list = []
        rmse_list = []

        for user_id, recommended in recommendations.items():
            actual = actual_preferences[actual_preferences['Id'] == user_id]

            # Convert to binary relevance (1 if present, 0 otherwise)
            actual_set = set(actual['Nutritional Preferences'].values)
            recommended_set = set(recommended['Nutritional Preferences'])

            binary_recommended = [1 if item in actual_set else 0 for item in recommended['Nutritional Preferences']]
            binary_actual = [1 if item in recommended_set else 0 for item in actual['Nutritional Preferences']]

            # Ensure binary_actual and binary_recommended are the same length
            length = max(len(binary_actual), len(binary_recommended))
            binary_actual.extend([0] * (length - len(binary_actual)))
            binary_recommended.extend([0] * (length - len(binary_recommended)))

            # Calculate metrics
            if len(binary_actual) > 0 and len(binary_recommended) > 0:
                precision = precision_score(binary_actual, binary_recommended, average='binary', zero_division=0)
                recall = recall_score(binary_actual, binary_recommended, average='binary', zero_division=0)
                f1 = f1_score(binary_actual, binary_recommended, average='binary', zero_division=0)
                mae = mean_absolute_error(binary_actual, binary_recommended)
                rmse = np.sqrt(mean_squared_error(binary_actual, binary_recommended))

                precision_list.append(precision)
                recall_list.append(recall)
                f1_list.append(f1)
                mae_list.append(mae)
                rmse_list.append(rmse)

        return {
            'precision': np.mean(precision_list) if precision_list else 0,
            'recall': np.mean(recall_list) if recall_list else 0,
            'f1': np.mean(f1_list) if f1_list else 0,
            'mae': np.mean(mae_list) if mae_list else 0,
            'rmse': np.mean(rmse_list) if rmse_list else 0
        }

def load_user_profiles():
    user_profiles = Profile.objects.all().values()
    df = pd.DataFrame(user_profiles)
    df.columns = [col.replace('_', ' ').title() for col in df.columns]  # Convert snake_case to Title Case
    return df