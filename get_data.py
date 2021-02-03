import requests
import os
import shutil
import datetime
import logging

def download_data(start_dt, end_dt, parent_dir, increment=60):
    if isinstance(increment, (int, float)):
        increment = int(increment)
        increment = datetime.timedelta(seconds=increment)
    i = 0
    base_url = 'https://api.data.gov.sg/v1/transport/traffic-images?date_time={}-{}-{}T{}%3A{}%3A{}%2B08%3A00'
    while start_dt < end_dt:
        i += 1
        print('Iteration no.', i)
        print('collecting data for', start_dt)
        dt_vars = start_dt.strftime('%Y %m %d %H %M %S').split()
        dt_id = start_dt.strftime('%Y%m%d_%H%M%S')
        print(dt_vars)
        url = base_url.format(*dt_vars)
        print('Url', url)
        get_images(url, parent_dir, dt_id)
        start_dt += increment


def dl_image(url, save_dir, dt_id):
    os.makedirs(save_dir, exist_ok=True)
    filename = '{}_{}'.format(dt_id, os.path.basename(url))
    r = requests.get(url)
    save_path = os.path.join(save_dir, filename)

    if r.status_code == 200:

        with open(save_path, 'wb+') as img:
            img.write(r.content)
        
        print('Downloaded Img', url)
    else:
        print('Image Doesn\'t Exist')




def get_images(url, parent_dir, dt_id):
    res = requests.get(url)
    json = res.json()
    print(json)
    for camera in json['items'][0]['cameras']:
        img_url = camera['image']
        location = camera['location']
        lat, long = location['latitude'], location['longitude']
        save_dir = os.path.join(parent_dir, f'({lat}, {long})')
        dl_image(img_url, save_dir, dt_id)

if __name__ == '__main__':
    # url = "https://api.data.gov.sg/v1/transport/traffic-images?date_time=2021-02-03T22%3A48%3A10%2B08%3A00"
    # img_url = 'https://images.data.gov.sg/api/traffic-images/2021/02/196bfcf5-7c64-45f2-b9e5-ee7622ef868b.jpg'
    # get_images(url, './data')

    start_dt = datetime.datetime(2020, 1, 1)
    end_dt = datetime.datetime(2021, 1, 1)
    download_data(start_dt, end_dt, './data')