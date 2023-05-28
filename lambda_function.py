from file_processing import DateAuto,FileProcess
from yt_comments import YouTubeComments
import os

def main_api_data(date_unit=str,date_back=str,channel_id=str):
    date_auto = DateAuto(date_unit,int(date_back))
    json_str = date_auto.date_to_str(for_json=True)
    start_date = date_auto.start_day_date
    end_date = date_auto.end_date
    data = YouTubeComments(channel_id,end_date,start_date)
    data = data.get_channel_comments()
    file_processing = FileProcess(json_str)
    file_processing.write_json(data)
    file_processing.write_S3()
    
date_unit = os.environ['date_unit']
date_back = os.environ['date_back']
channel_id = os.environ['channel_id']

def lambda_handler(event,context):
     event = main_api_data(date_unit,date_back,channel_id)
     return event
