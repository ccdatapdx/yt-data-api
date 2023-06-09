from datetime import datetime
from datetime import timedelta
import json
import os
import boto3
from botocore.exceptions import ClientError
import logging

class DateManual:

    def __init__(self,start_date,end_date) -> None:
        self.str_format = '%m.%d.%Y'
        self.start_date = datetime.strptime(start_date,self.str_format)
        self.end_date = datetime.strptime(end_date,self.str_format)

    def date_to_str(self,for_json=bool):
        if for_json is True:
            return f'{self.start_date}-{self.end_date}.json'
        else:
            return f'{self.start_date}-{self.end_date}'

class DateAuto:

    def __init__(self,date_unit:str,date_back:int) -> None:
        self.date_unit = date_unit.lower()
        self.date_back = date_back
        self.days_delta = timedelta(days=date_back)
        self.weeks_delta = timedelta(weeks=date_back)
        self.end_date = datetime.now()
        self.str_format = '%m.%d.%Y'
        self.start_day_date = self.end_date-self.days_delta
        self.start_week_date = self.end_date-self.weeks_delta

    def date_to_json_str(self,channel_name:str,for_raw_data:bool):
        start_day_date = datetime.strftime(self.start_day_date,self.str_format)
        start_week_date = datetime.strftime(self.start_week_date,self.str_format)
        end_date =  datetime.strftime(self.end_date,self.str_format)
        if self.date_unit == 'days':
            if for_raw_data is True:
                return f'{channel_name}_raw_{start_day_date}-{end_date}.json'
            else:
                return f'{channel_name}_spacy_{start_day_date}-{end_date}.json'
        if self.date_unit == 'weeks':
            if for_raw_data is True:
                return f'{channel_name}_raw_{start_week_date}-{end_date}.json'
            else:
                return f'{channel_name}_spacy_{start_week_date}-{end_date}'

class DateAutoVideo:

    def __init__(self,published_date:datetime) -> None:
        self.today = datetime.now()
        self.published_date = datetime.strptime(published_date,'%Y-%m-%dT%H:%M:%SZ').date()
        self.str_format = '%m.%d.%Y'
    
    def video_to_str(self):
        today = datetime.strftime(self.today,self.str_format)
        published_date = datetime.strftime(self.published_date,self.str_format)
        return f'{today}-{published_date}.json'

class FileProcess:

    def __init__(self,json_str:str) -> None:
        self.json_str=json_str
        self.logger=logging.getLogger()
        self.file_path='/tmp'

    def open_json(self,return_metadata=bool) -> json:
        with open(self.json_str) as f:
            json_file = json.load(f)
        if return_metadata is True:
            metadata = json_file['metadata']
            meta_ids = metadata['video_ids']
            meta_dates = metadata['video_date']
            meta_titles = metadata['video_titles']
            meta_keys = list(zip(meta_ids,meta_dates,meta_titles))
            meta_names = ['video_ids','video_dates','video_titles']
            video_metadata = {'meta_keys':meta_keys,'meta_names':meta_names}
            return video_metadata
        else:
            return json_file
             
    def write_json(self,data) -> json:
        os.makedirs(self.file_path,exist_ok=True)
        with open(os.path.join(self.file_path,self.json_str),'w') as f:
            json.dump(data,f)
                    
    def write_S3(self):
        try:
           s3 = boto3.client('s3') 
           s3.upload_file(f'{self.file_path}/{self.json_str}','yt-channel-comments',self.json_str)
           self.logger.setLevel('INFO')
           self.logger.info('into S3!')
        except ClientError as e:
           self.logger.error(e)
