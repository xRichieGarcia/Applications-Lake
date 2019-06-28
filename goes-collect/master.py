"""
Second shot at making a video out of every object in s3 bucket.
This time I'm using aws s3 sync & ffmpeg
[update] promoted to master file
"""

import os
import boto3
import time

s3 = boto3.resource('s3')
video_bucket = s3.Bucket('bucket-name')

#download all existing files
command_1 = 'aws s3 sync s3://goes-east-photos-2/goes-conus goes-conus/'
os.system(command_1)

#make video out of them
video_num = sum(1 for _ in video_bucket.objects.all())
video_name = str(video_num).zfill(4) + '.mkv'
command_2 = 'ffmpeg -i goes-conus/%06d.jpg -framerate 20 {} -nostdin'.format(video_name)
os.system(command_2)

#move new video with others in DIFFERENT BUCKET (this will break goes-get)
video_raw = open(video_name)
video_bucket.put_object(Key=video_name, Body=video_raw)

#clean goes-collect/ and aws synced goes-conus/
os.system('rm {}'.format(video_name))
os.system('rm -r goes-conus/*')

#sync empty local goes-conus/ to s3://goes-east-photos-2/goes-conus
command_3 = 'aws s3 sync --delete goes-conus/ s3://goes-east-photos-2/goes-conus/'
os.system(command_3)
