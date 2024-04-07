import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
data = pd.read_csv("recipes.csv")
columns = ['RecipeId', 'Name', 'RecipeIngredientParts', 'Calories', 'FatContent', 'SaturatedFatContent',
           'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']
dataset = data[columns]

max_values = {
    'Calories': 2000,
    'FatContent': 100,
    'SaturatedFatContent': 13,
    'CholesterolContent': 300,
    'SodiumContent': 2300,
    'CarbohydrateContent': 325,
    'FiberContent': 40,
    'SugarContent': 40,
    'ProteinContent': 200
}

# Filter dataset based on maximum nutritional values
filtered_data = dataset.copy()
for column, max_value in max_values.items():
    filtered_data = filtered_data[filtered_data[column] < max_value]

def scaling(dataframe):
    scaler = StandardScaler()
    prep_data = scaler.fit_transform(dataframe.iloc[:, 3:12])
    return prep_data, scaler

def nn_alg_predict(prep_data):
    neigh = NearestNeighbors(metric='cosine', algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def filter_data(dataframe, ingredient_filter):
    filtered = dataframe.copy()
    if ingredient_filter:
        filtered = filtered[filtered['RecipeIngredientParts'].str.contains('|'.join(ingredient_filter), case=False, na=False)]
    return filtered

def recommendation(dataframe, input_values, ingredient_filter):
    filtered_data = filter_data(dataframe, ingredient_filter)
    print(filtered_data.head(1))
    prep_data, scaler = scaling(filtered_data)
    
    neigh = nn_alg_predict(prep_data)
    print(input_values)
    distances, indices = neigh.kneighbors(input_values)
    print(indices)
    recommendations = filtered_data.iloc[indices[0]]
    print(recommendations)
    return recommendations.to_dict(orient='records')

test_input = filtered_data.iloc[0:1, 3:12].to_numpy()
ingredient_filter = ["egg"]
recommendation(filtered_data, test_input,ingredient_filter)