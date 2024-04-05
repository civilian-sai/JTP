from flask import Flask, request, render_template
import pandas as pd
import numpy as np  # Import NumPy

# Rest of the code remains the same...

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Load dataset and preprocess it
data = pd.read_csv("recipes.csv")
columns = ['RecipeId','Name','RecipeIngredientParts','Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent','RecipeInstructions']
dataset = data[columns]
max_Calories = 2000
max_daily_fat = 100
max_daily_Saturatedfat = 13
max_daily_Cholesterol = 300
max_daily_Sodium = 2300
max_daily_Carbohydrate = 325
max_daily_Fiber = 40
max_daily_Sugar = 40
max_daily_Protein = 200
max_list = [max_Calories,max_daily_fat,max_daily_Saturatedfat,max_daily_Cholesterol,max_daily_Sodium,max_daily_Carbohydrate,max_daily_Fiber,max_daily_Sugar,max_daily_Protein]
extracted_data = dataset.copy()
for column, maximum in zip(extracted_data.columns[3:12], max_list):
    extracted_data = extracted_data[extracted_data[column] < maximum]

# Define functions for scaling, nearest neighbors algorithm, and recommendation
def scaling(dataframe):
    scaler = StandardScaler()
    prep_data = scaler.fit_transform(dataframe.iloc[:, 3:12].to_numpy())
    return prep_data, scaler

def nn_alg_predict(prep_data):
    neigh = NearestNeighbors(metric='cosine', algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def filter_data(dataframe, ingredient_filter, max_nutritional_values):
    extracted_data = dataframe.copy()
    if ingredient_filter is not None:
        for ingredient in ingredient_filter:
            extracted_data = extracted_data[extracted_data['RecipeIngredientParts'].str.contains(ingredient, regex=False)]
    return extracted_data

def recommendation(dataframe, _input, max_nutritional_values, ingredient_filter=None):
    extracted_data = filter_data(dataframe, ingredient_filter, max_nutritional_values)
    prep_data, scaler = scaling(extracted_data)
    neigh = nn_alg_predict(prep_data)
    distances, indices = neigh.kneighbors(_input)
    recommendations = extracted_data.iloc[indices[0]]
    return recommendations

# Initialize Flask application
app = Flask(__name__)

# Define route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Define route for recommendation page
@app.route('/recommendation', methods=['POST'])
def get_recommendation():
    # Get inputs from form
    test_input = [float(request.form['calories']), float(request.form['fat']), float(request.form['saturated_fat']),
                  float(request.form['cholesterol']), float(request.form['sodium']), float(request.form['carbohydrate']),
                  float(request.form['fiber']), float(request.form['sugar']), float(request.form['protein'])]
    ingredient_filter = request.form['ingredient_filter'].split(',')

    # Convert inputs to numpy array
    test_input = np.array([test_input])

    # Get recommendation
    rec = recommendation(extracted_data, test_input, max_list, ingredient_filter)
    return rec.to_html()

if __name__ == '__main__':
    app.run(debug=True)
