import googleapiclient.discovery
import logging
import os
from googleapiclient.errors import HttpError
from datetime import datetime

class YouTubeData:
    
    def __init__(self,api_service_name:str,api_version:str) -> None:
            DEVELOPER_KEY = os.environ['developer_key']
            self.youtube = googleapiclient.discovery.build(api_service_name,api_version,
                                                           developerKey=DEVELOPER_KEY)
            self.api_service_name = api_service_name
            self.api_version = api_version
            self.logger = logging.getLogger()
            self.youtube_comments = self.youtube.commentThreads()
            self.youtube_search = self.youtube.search()
            self.youtube_videos = self.youtube.videos()
    
    def list_comment_threads(self,videoId:str,pageToken=None):
        try:
             result = self.youtube_comments.list(
                            videoId=videoId,
                            part='snippet',
                            order='time',
                            textFormat='plainText',
                            maxResults=100,
                            pageToken=pageToken
                        ).execute()
             result = result.get('items', [])
             return result
        except HttpError as e:
            error_reason = e.error_details[0]['reason']
            error_log_str = f'{e.status_code},{videoId},{error_reason}'
            self.logger.error(error_log_str)
           
    def list_channel_videoId(self,channelId:str,date_before:datetime,date_after:datetime):
        try:
            result = self.youtube_search.list(
                            channelId=channelId,
                            part='snippet',
                            type='video',
                            maxResults=50,
                            publishedBefore=date_before.isoformat("T") + "Z",
                            publishedAfter=date_after.isoformat("T") + "Z",
                            order='date'
                        ).execute()
            result = result.get('items', [])
            return result
        except HttpError as e:
            error_reason = e.error_details[0]['reason']
            error_log_str = f'{e.status_code},{channelId},{error_reason}'
            self.logger.error(error_log_str)
        
    def list_video(self,videoId:str):
        try:
              result = self.youtube_videos.list(
                   part='snippet',
                   id=videoId
              ).execute()
              result = result.get('items', [])
              return result
        except HttpError as e:
            error_reason = e.error_details[0]['reason']
            error_log_str = f'{e.status_code},{videoId},{error_reason}'
            self.logger.error(error_log_str)
            