from file_processing import DateAuto,FileProcess
from yt_comments import YouTubeComments
import os

#date_unit = os.environ['date_unit']
#date_back = os.environ['date_back']
#channel_id = os.environ['channel_id']
#channel_name = os.environ['channel_name']

date_unit = 'days'
date_back = 7
channel_id = 'UCXuqSBlHAE6Xw-yeJA0Tunw'
channel_name = 'Linus Tech Tips'

def main_api_data(date_unit:str,date_back:str,channel_name:str,channel_id:str):
    date_auto = DateAuto(date_unit,int(date_back))
    json_str = date_auto.date_to_json_str(channel_name,for_raw_data=True)
    start_date = date_auto.start_day_date
    end_date = date_auto.end_date
    data = YouTubeComments(channel_id,end_date,start_date)
    data = data.get_channel_comments()
    file_processing = FileProcess(json_str)
    file_processing.write_json(data)
    file_processing.write_S3()
    

def lambda_handler(event,context):
     event = main_api_data(date_unit,date_back,channel_name,channel_id)
     return event
