'''
    WARNING: This python program is using Google's "YouTube Data API v3".
    In order to use this script you will need to get an api key, you can learn more at:
    https://developers.google.com/youtube/v3/getting-started
'''

import api_keys # You must create this file and place there a signle variable name 'youtube_data_v3_key'
                # Which will store your API key

import googleapiclient.discovery
import googleapiclient.errors

class Video:
    def __init__(self, url):
        self.url = url

        self.get_publish_date()
        self.get_likes_counter()
        self.get_comments_counter()
        self.get_views_counter()
        self.get_tags()
    
    def get_publish_date(self):
        self.publish_date = 0

    def get_likes_counter(self):
        self.likes = 0
    
    def get_comments_counter(self):
        self.comments = 0
    
    def get_views_counter(self):
        self.views = 0
    
    def get_tags(self):
        self.tags = []

def get_channel_id(youtube, channel_username):
    request = youtube.channels().list(
        part="id",
        forUsername=channel_username
    )

    response = request.execute()
    
    if response['pageInfo']['totalResults'] == 0:
        return "invalid"
    
    return response['items'][0]['id']

def main():
    channel_username = input("Type the username for the channle you want to analyze:")

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_keys.youtube_data_v3_key)

    channel_id = get_channel_id(youtube, channel_username)
    if channel_id == "invalid":
        print("Error: The username you have typed is invalid.")
        return
    
    print(channel_id)
    
main()