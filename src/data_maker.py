import json
from src.helper_functions import fetch_video_info

__author__ = "Nathan Kirk"
__credits__ = ["Nathan Kirk"]
__license__ = "GPL-3.0 license"
__email__ = "nkirk@westmont.edu"


with open("../data/combined_raw.json", 'r') as file:
    total_data = json.load(file)

api_key = 'AIzaSyAtB7cu0ikP0LwA27o6JTlffkzLdQWDuDo'

# Replace 'path/to/your/json/file.json' with the actual path to your JSON file
json_file_path = '../data/combined_raw.json'

# Fetch video information and store the documents in a list
all_docs = fetch_video_info(api_key, json_file_path)

with open("../data/final_data.json", "w") as file:
    json.dump(all_docs, file, indent=2)
