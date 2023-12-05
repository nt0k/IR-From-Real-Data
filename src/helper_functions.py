import json
from googleapiclient.discovery import build

__author__ = "Nathan Kirk"
__credits__ = ["Nathan Kirk"]
__license__ = "GPL-3.0 license"
__email__ = "nkirk@westmont.edu"


def fetch_video_info(api_key, json_file_path):
    # Initialize the YouTube Data API
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Initialize a list to store video documents
    all_video_docs = []
    count = 0
    # Iterate through videos in the JSON file
    for video_info in data:
        # Extract video ID from titleUrl
        video_url = video_info.get('titleUrl', '')
        video_id = video_url.split('v=')[-1]

        # Request video details using the YouTube API
        video_request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        video_response = video_request.execute()

        # Extract relevant information from the API response
        if 'items' in video_response and video_response['items']:
            video_details = video_response['items'][0]['snippet']
            title = video_details.get('title', '')
            channel = video_details.get('channelTitle', '')
            description = video_details.get('description', '')
            tags = video_details.get('tags', [])
            publication_date = video_details.get('publishedAt', '')

            # Create a document with extracted information
            video_doc = {
                "title": title,
                "channel": channel,
                "description": description,
                "tags": tags,
                "publication_date": publication_date
            }

            # Add the document to the list
            all_video_docs.append(video_doc)
            count += 1
            if count % 1000 == 0:
                print(f'Processed {count} documents!')

    # Return the list of all video documents
    return all_video_docs
