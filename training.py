import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import pickle

# Load dataset and preprocess it
data = pd.read_csv("recipes.csv")
columns = ['RecipeId', 'Name', 'RecipeIngredientParts', 'Keywords', 'Calories', 'FatContent', 'SaturatedFatContent',
           'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']
dataset = data[columns]

# Define maximum nutritional values
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
filtered_data.replace({np.nan: None}, inplace=True)

# Filter for vegetarian recipes (exclude 'meat' in Keywords)
veg_filter = filtered_data[~filtered_data['Keywords'].str.contains('meat', na=False, case=False)]

# Perform Standard Scaling on filtered datasets
scaler = StandardScaler()
prep_data = scaler.fit_transform(filtered_data.iloc[:, 4:13])
prep_data_veg = scaler.fit_transform(veg_filter.iloc[:, 4:13])

# Initialize NearestNeighbors models
neigh = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
neigh.fit(prep_data)

neigh_veg = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
neigh_veg.fit(prep_data_veg)

# Save NearestNeighbors instance and preprocessing data
with open('neigh_model.pkl', 'wb') as f:
    pickle.dump(neigh, f)

with open('neigh_model_veg.pkl', 'wb') as v:
    pickle.dump(neigh_veg, v)

np.save('prep_data.npy', filtered_data.to_numpy())
np.save('prep_data_veg.npy', veg_filter.to_numpy())
