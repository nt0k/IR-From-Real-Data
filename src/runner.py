import json
import requests
from googleapiclient.discovery import build

from src.helper_functions import fetch_video_info

with open("../data/personal.json") as file:
    personal_data = json.load(file)

with open("../data/throw-away.json") as file:
    throw_data = json.load(file)

with open("../data/westmont.json") as file:
    westmont_data = json.load(file)

count = 0
erased_count = 0
title_array = []
data = []

for record in personal_data:
    title = record["title"]
    if "https" in title:
        erased_count += 1
    else:
        title_array.append(title)
        count += 1
        data.append(record)

for record in throw_data:
    title = record["title"]
    if "https" in title:
        erased_count += 1
    else:
        title_array.append(title)
        count += 1
        data.append(record)

for record in westmont_data:
    title = record["title"]
    if "https" in title:
        erased_count += 1
    else:
        title_array.append(title)
        count += 1
        data.append(record)

with open("../data/data.json", "w") as file:
    json.dump(data, file, indent=2)

print(f"{data}")
# print(f"You have records on a total of {count} videos watched.")
# print(f"{erased_count} videos were erased or removed! That is {erased_count / (erased_count + count) * 100}%")


api_key = 'AIzaSyAtB7cu0ikP0LwA27o6JTlffkzLdQWDuDo'

# Replace 'path/to/your/json/file.json' with the actual path to your JSON file
json_file_path = '../data/personal.json'

# Fetch video information and store the documents in a list
all_docs = fetch_video_info(api_key, json_file_path)

with open("../data/final_data.json", "w") as file:
    json.dump(all_docs, file, indent=2)

# Print or process the list of documents as needed
for video_doc in all_docs:
    print(json.dumps(video_doc, indent=2))
    print('-' * 50)
