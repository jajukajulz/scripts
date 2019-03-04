from random import randint
import os
import csv
import urllib.request as req
import time

#read list of urls rom csv
images_csv = '<filename>'

#directory to download to
file_path = '<download_directory>'

with open(images_csv, 'r') as f:
  reader = csv.reader(f)
  images_urls_list = list(reader)

n_images = 0

for image_url in images_urls_list:
    n_images += 1
    print(str(n_images))
    image_url = image_url[0]
    filename = image_url[image_url.rfind("/") + 1:]
    fullfilename = os.path.join(file_path, filename)
    req.urlretrieve(image_url, fullfilename)

    # Sleep for 1 or 2 seconds
    time.sleep(randint(1, 2))

print('Successfully downloaded {} images.'.format(n_images))
