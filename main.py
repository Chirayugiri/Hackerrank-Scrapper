from flask import Flask, jsonify, request
from flask_cors import CORS
from scrapper import (
    start_driver, open_chrome, change_view_per_page, extract_data,
    move_to_next_page, close_driver, leaderboard_data
)
from cleaner import clean_csv
from combiner import combine_files
import pandas as pd
import numpy as np
import os
from io import StringIO, BytesIO
from collections import OrderedDict

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def read_uploaded_file(file):
    """Reads the uploaded file and converts it into a pandas DataFrame."""
    if file.filename.endswith('.csv'):
        return pd.read_csv(StringIO(file.read().decode('utf-8')))
    elif file.filename.endswith('.xlsx'):
        return pd.read_excel(BytesIO(file.read()))
    else:
        raise ValueError("Unsupported file type")

def scrape_leaderboard_data(hacker_rank_url):
    """Scrapes leaderboard data from the given HackerRank URL."""
    start_driver()
    open_chrome(hacker_rank_url)
    change_view_per_page()
    
    for _ in range(2):  # Scraping two pages
        extract_data()
        move_to_next_page(_)
    
    close_driver()
    return pd.DataFrame(leaderboard_data, columns=["HackerRank ID", "Score"])

def merge_data(cleaned_df, leaderboard_df):
    """Merges the cleaned file data with leaderboard data and removes duplicates."""
    merged_df = combine_files(cleaned_df, leaderboard_df)
    merged_df = merged_df.replace({np.nan: None})
    return merged_df.drop_duplicates(subset=['HackerRank ID'], keep='first')

@app.route('/upload', methods=['POST'])
def upload_csv():
    try:
        hacker_rank_url = request.form.get('hackerRankUrl')
        if not hacker_rank_url:
            return jsonify({"error": "HackerRank URL is required"}), 400

        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        df = read_uploaded_file(file)
        cleaned_df = clean_csv(df)
        leaderboard_df = scrape_leaderboard_data(hacker_rank_url)
        merged_df = merge_data(cleaned_df, leaderboard_df)

        ordered_json = [OrderedDict(row) for row in merged_df.to_dict(orient='records')]
        return jsonify(ordered_json)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Using Render's assigned PORT
    app.run(host="0.0.0.0", port=port)