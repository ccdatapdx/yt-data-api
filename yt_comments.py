from yt_channel_api_data import YouTubeData
from datetime import datetime
from itertools import chain

class YouTubeComments:

    def __init__(self,channel_id:str,date_before:datetime,date_after:datetime) -> None:
        self.channel_comments_list = []
        self.channel_all_comments_list = []
        self.channel_no_comments = []
        self.channel_title_list = []
        self.channel_date_list = []
        self.channel_video_id_list = []
        self.all_comments_list = []
        self.channel_id = channel_id
        self.date_before = date_before
        self.date_after = date_after

    def get_video_title(self,videoId:str)->str:
        results = YouTubeData('youtube','v3').list_video(videoId)
        for result in results:
            result_title = result['snippet']['title']
        return result_title

    def get_video_date(self,videoId:str)->str:
        results = YouTubeData('youtube','v3').list_video(videoId)
        for result in results:
            result_date = result['snippet']['publishedAt']
        return result_date

    def get_channel_ids(self)->list:
        results = YouTubeData('youtube','v3').list_channel_videoId(self.channel_id,
                                                                   self.date_before,
                                                                   self.date_after)
        for result in results:
            if result['snippet']['liveBroadcastContent'] == 'live':
                continue
            self.channel_video_id_list.append(result['id']['videoId'])
        return self.channel_video_id_list
    
    def get_video_comments(self,videoId:str)->dict:
        results = YouTubeData('youtube','v3').list_comment_threads(videoId)
        video_comments_list = []
        video_comments_ids_list = []
        video_comments_dates_list = []
        video_comment_reply_counts_list = []
        if results:
            while results:
                for result in results:
                    topLevelComment = result['snippet']['topLevelComment']
                    comment = topLevelComment['snippet']['textDisplay']
                    comment_id = topLevelComment['id']
                    comment_date = topLevelComment['snippet']['updatedAt']
                    comment_reply_count = result['snippet']['totalReplyCount']
                    video_comments_list.append(comment)
                    video_comments_ids_list.append(comment_id)
                    video_comments_dates_list.append(comment_date)
                    video_comment_reply_counts_list.append(comment_reply_count)
                    comments_final = {'comment_text':video_comments_list,
                                      'comment_id':video_comments_ids_list,
                                      'comment_date':video_comments_dates_list,
                                      'comment_reply_counts':video_comment_reply_counts_list}
                if 'nextPageToken' in results:
                    pageToken = results.get('nextPageToken',False)
                    results = YouTubeData('youtube','v3').list_comment_threads(videoId,pageToken)
                else:
                    break
            return comments_final
        else:
            return None

    def get_channel_comments(self)->dict:
        channel_ids = self.get_channel_ids()
        for id in channel_ids:
            comment_data = self.get_video_comments(id)
            if comment_data:
                self.channel_comments_list.append(comment_data)
                self.channel_all_comments_list.append(comment_data['comment_text'])
                self.all_comments_list = list(chain.from_iterable(self.channel_all_comments_list))
                title_data = self.get_video_title(id)
                self.channel_title_list.append(title_data)
                date_data = self.get_video_date(id)
                self.channel_date_list.append(date_data)
            else:
                self.channel_no_comments.append(f'{id} not available')
        date_titles = {'metadata':
                                  {"video_date":self.channel_date_list,
                                   "video_titles":self.channel_title_list,
                                   "video_ids":self.channel_video_id_list,
                                   "no_comments":self.channel_no_comments}
                                                                          }
        
        comments = {"comments":dict(zip(self.channel_video_id_list,
                                        self.channel_comments_list)),
                    "all_comments":self.all_comments_list}
        comments.update(date_titles)
        return comments
    