from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pickle

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/recommendation": {"origins": "http://127.0.0.1:5500"}})
# Load preprocessing data
filtered_data = np.load('prep_data.npy', allow_pickle=True)
filtered_data_veg = np.load('prep_data_veg.npy', allow_pickle=True)
scaler = StandardScaler()
prep_data = scaler.fit_transform(filtered_data[:, 4:13])
prep_data_veg = scaler.fit_transform(filtered_data_veg[:, 4:13])

# Load NearestNeighbors model
with open('neigh_model.pkl', 'rb') as f:
    neigh = pickle.load(f)

with open('neigh_model_veg.pkl', 'rb') as v:
    neigh_veg = pickle.load(v)

# Define route for recommendation
@app.route('/recommendation', methods=['POST'])
def get_recommendation():
    try:
        # Process request data
        input_values = [float(request.form['calories']), float(request.form['fat']), float(request.form['saturated_fat']),
                  float(request.form['cholesterol']), float(request.form['sodium']), float(request.form['carbohydrate']),
                  float(request.form['fiber']), float(request.form['sugar']), float(request.form['protein'])]
        check=float(request.form['diet'])
        print("input_values:",input_values)
        # Preprocess input data
        input_scaled = scaler.transform([input_values])
        print("input_scaled:",input_scaled)
        # Get nearest neighbors indices using loaded NearestNeighbors model
        if(check==0):
            distances, indices = neigh.kneighbors(input_scaled)
            print("indices:",indices)
            # Get recommendations based on indices
            recommendations = filtered_data[indices[0]]
            print(recommendations)
            # Convert recommendations to dictionary records
            rec_dict = [{'RecipeId': int(rec[0]), 'Name': rec[1], 'RecipeIngredientParts': rec[2], 'Keywords': rec[3]} for rec in recommendations]
            print(rec_dict)
            return jsonify(rec_dict)
        else:
            distances, indices = neigh_veg.kneighbors(input_scaled)
            print("indices:",indices)
            # Get recommendations based on indices
            recommendations = filtered_data_veg[indices[0]]
            print(recommendations)
            # Convert recommendations to dictionary records
            rec_dict = [{'RecipeId': int(rec[0]), 'Name': rec[1], 'RecipeIngredientParts': rec[2], 'keywords': rec[3]} for rec in recommendations]
            print(rec_dict)
            return jsonify(rec_dict)

    except Exception as e:
         return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
