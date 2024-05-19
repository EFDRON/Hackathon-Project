from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

def generate_graphs(year, emirate):
    try:
        year = int(year)
    except ValueError:
        return {'error': 'Invalid year format. Year must be an integer.'}
    # Read data from Excel file
    data = pd.read_excel('data/my_analysis.xlsx')

    # Filter data for the selected year and emirate
    filtered_data = data[(data['Year'] == year) & (data['Emirates'] == emirate)]

    # Extract disability categories and corresponding counts
    disability_categories = ['Mentality', 'Auditory', 'Autism', 'Physical', 'Multiple',
                             'Visual', 'Psychological', 'Communication', 'Audio-visual',
                             'Lack of attention and excessive activity']
    disability_counts = filtered_data[disability_categories].sum().values.astype(int).tolist()

    # Extract male and female counts
     # Extract male and female counts
    male_count = int(filtered_data['Male'].sum())
    female_count = int(filtered_data['Female'].sum())
    # Prepare data for graphs
    disability_graph_data = {
        'categories': disability_categories,
        'counts': disability_counts
    }
    gender_graph_data = {
        'categories': ['Male', 'Female'],
        'counts': [male_count, female_count]
    }

    return {'disability_graph': disability_graph_data, 'gender_graph': gender_graph_data}

@app.route('/graphs', methods=['POST'])
def get_graphs():
    # Get parameters from the request
    year = int(request.json['year'])
    emirate = request.json['emirate']

    # Generate graphs data
    graphs_data = generate_graphs(year, emirate)

    return jsonify(graphs_data)

@app.route('/')
def index():
    return render_template('index3.html')

if __name__ == '__main__':
    app.run(debug=True)
