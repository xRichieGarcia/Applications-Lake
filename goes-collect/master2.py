"""
When ran, this function will go to the beginning of today, and look through the 
S3 bucket for files all files created that day. It then stiches each frame to 
the master video file. Uses cv2 instead of ffmpeg
"""

import datetime
import boto3
import requests
import cv2

# left off here https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object


s3 = boto3.resource('s3')
bucket_name= 'bucket-name'

# 1500x2500 px images in RGB space
height = 1500
width = 2500
layers = 3
video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('M','J','P','G'), \
                        1,(width, height))

today_beginning = datetime.datetime.combine(datetime.date.today(), datetime.time())
day_one = datetime.date(today_beginning.year, 1, 1)
day_n = (today_beginning.date() - day_one).days + 1

for h in range(24):
    for m in range(60):
        t_stamp = str(today_beginning.year) + str(day_n) + \
            str(h).zfill(2) + str(m).zfill(2)
        s3_image_filename = 'goes-conus/' + t_stamp + '-2500x1500.jpg'
        try:
            image = s3.Object(bucket_name, s3_image_filename)
            # add stiching here
        except:
            pass


"""
img1 = cv2.imread('1.jpg')
img2 = cv2.imread('2.jpg')
img3 = cv2.imread('3.jpg')


video = cv2.VideoWriter('video.avi',-1,1,(width,height))

video.write(img1)
video.write(img2)
video.write(img3)

cv2.destroyAllWindows()
video.release()
"""
