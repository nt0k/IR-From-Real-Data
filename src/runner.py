import json
import requests
from googleapiclient.discovery import build

with open("../data/personal.json") as file:
    personal_data = json.load(file)

with open("../data/throw-away.json") as file:
    throw_data = json.load(file)

with open("../data/westmont.json") as file:
    westmont_data = json.load(file)

count = 0
erased_count = 0
title_array = []

for record in personal_data:
    title = record["title"]
    if "https" in title:
        erased_count += 1
    else:
        title_array.append(title)
        count += 1

for record in throw_data:
    title = record["title"]
    if "https" in title:
        erased_count += 1
    else:
        title_array.append(title)
        count += 1

for record in westmont_data:
    title = record["title"]
    if "https" in title:
        erased_count += 1
    else:
        title_array.append(title)
        count += 1

#print(title_array)
print(f"You have records on a total of {count} videos watched.")
print(f"{erased_count} videos were erased or removed! That is {erased_count / (erased_count + count) * 100}%")

# Set your API key
api_key = 'AIzaSyAtB7cu0ikP0LwA27o6JTlffkzLdQWDuDo'

# Replace this with the YouTube video URL you want to get data for
video_url = 'https://www.youtube.com/watch?v=FfMeHzVtnfs'

# Extract video ID from the URL
video_id = video_url.split('v=')[1]

# Initialize the YouTube Data API
youtube = build('youtube', 'v3', developerKey=api_key)

# Request video details
video_request = youtube.videos().list(part='snippet,contentDetails,statistics', id=video_id)
video_response = video_request.execute()

# Extract relevant information
video_details = video_response['items'][0]
title = video_details['snippet']['title']
description = video_details['snippet']['description']
views = video_details['statistics']['viewCount']
likes = video_details['statistics']['likeCount']
#dislikes = video_details['statistics']['dislikeCount']

# Print the information
print(f'Title: {title}')
print(f'Views: {views}')
print(f'Likes: {likes}')
#print(f'Dislikes: {dislikes}')