import datetime
import boto3
import requests
"""
example link:
https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/
20191290511
_GOES16-ABI-CONUS-GEOCOLOR-2500x1500.jpg
"""

# Uses the creds in ~/.aws/credentials
s3 = boto3.resource('s3')
bucket_name_to_upload_image_to = 'bucket-name' #enter bucket name

t = datetime.datetime.utcnow()
day_one = datetime.date(t.year, 1, 1)

def handler(event, context):
    offset = 10
    while (offset <=15):
        t_past = t - datetime.timedelta(minutes=offset)
        day_n = (t_past.date() - day_one).days + 1
        t_stamp = str(t_past.year) + str(day_n) + \
            str(t_past.hour).zfill(2) + str(t_past.minute).zfill(2)
        
        internet_image_url = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/' + \
            t_stamp + '_GOES16-ABI-CONUS-GEOCOLOR-2500x1500.jpg'
        s3_image_filename = 'goes-conus/' + t_stamp + '-2500x1500.jpg'
    
        # Given an Internet-accessible URL, download the image and upload it to S3,
        # without needing to persist the image to disk locally
        req_for_image = requests.get(internet_image_url, stream=True)
        if req_for_image:
            file_object_from_req = req_for_image.raw
            req_data = file_object_from_req.read()
            
            # Do the actual upload to s3
            s3.Bucket(bucket_name_to_upload_image_to).put_object(Key=s3_image_filename, Body=req_data)
        offset += 1
    return
