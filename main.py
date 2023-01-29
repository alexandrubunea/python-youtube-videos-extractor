'''
    WARNING: This python program is using Google's "YouTube Data API v3".
    In order to use this script you will need to get an api key, you can learn more at:
    https://developers.google.com/youtube/v3/getting-started
'''

import api_keys # You must create this file and place there a signle variable name 'youtube_data_v3_key'
                # Which will store your API key

import googleapiclient.discovery
import googleapiclient.errors

import xlsxwriter
import time

class Video:
    def __init__(self, video_http_data):
        self.title = video_http_data['items'][0]['snippet']['title']
        self.publish_date = video_http_data['items'][0]['snippet']['publishedAt']
        self.like_count = video_http_data['items'][0]['statistics']['likeCount']
        self.comment_count = video_http_data['items'][0]['statistics']['commentCount']
        self.view_count = video_http_data['items'][0]['statistics']['viewCount']
        
        try:
            self.tags = [video_http_data['items'][0]['snippet']['tags']]
        except:
            self.tags = []
    
    def get_title(self):
        return self.title

    def get_publish_date(self):
        return self.publish_date

    def get_like_count(self):
        return self.like_count
    
    def get_comment_count(self):
        return self.comment_count
    
    def get_view_count(self):
        return self.view_count
    
    def get_tags(self):
        return self.tags

def get_channel_id(youtube, channel_username):
    request = youtube.channels().list(
        part="id",
        forUsername=channel_username
    )

    response = request.execute()
    
    if response['pageInfo']['totalResults'] == 0:
        return "invalid"
    
    return response['items'][0]['id']

def get_videos_ids_from_channel(youtube, channle_id, limit):
    request = youtube.search().list(
        part="snippet",
        channelId=channle_id,
        maxResults=limit,
        order="date",
        type="video"
    )

    response = request.execute()

    result = []
    for video in response['items']:
        result.append(video['id']['videoId'])

    return result

def get_videos_data(youtube, videos_ids):
    result = []

    for video_id in videos_ids:
        request = youtube.videos().list(
            part="snippet, statistics",
            id=video_id
        )
        
        response = request.execute()
        result.append(Video(response))
    return result

def create_excel_file(channel_username, videos_data):
    file_name = channel_username + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx"

    workbook = xlsxwriter.Workbook('output/' + file_name)
    worksheet = workbook.add_worksheet("Sheet1")
    
    worksheet.write(0, 0, "#")
    worksheet.write(0, 1, "Title")
    worksheet.write(0, 2, "Publish Date")
    worksheet.write(0, 3, "Views")
    worksheet.write(0, 4, "Likes")
    worksheet.write(0, 5, "Comments")
    worksheet.write(0, 6, "Tags")

    index = 1
    for video_data in videos_data:
        worksheet.write(index, 0, index)
        worksheet.write(index, 1, video_data.get_title())
        worksheet.write(index, 2, video_data.get_publish_date())
        worksheet.write(index, 3, video_data.get_view_count())
        worksheet.write(index, 4, video_data.get_like_count())
        worksheet.write(index, 5, video_data.get_comment_count())

        index += 1
    
    workbook.close()

def main():
    channel_username = input("Type the username for the channle you want to analyze: ")

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_keys.youtube_data_v3_key)

    channel_id = get_channel_id(youtube, channel_username)
    if channel_id == "invalid":
        print("Error: The username you have typed is invalid.")
        return
    
    number_of_videos = int(input("Enter the number of videos you want to analye(from the newest uploded)(Limit: 50): "))
    if number_of_videos > 50:
        number_of_videos = 50
    elif number_of_videos < 0:
        number_of_videos = 0

    videos_ids = get_videos_ids_from_channel(youtube, channel_id, number_of_videos)

    videos_data = get_videos_data(youtube, videos_ids)

    create_excel_file(channel_username, videos_data)

    return
main()