import argparse
import multiprocessing
import os
from pathlib import Path

import pandas as pd
import requests
import time

parser = argparse.ArgumentParser()

parser.add_argument("--num_proc",
                    default=4,
                    type=int,
                    help="How many cpu cores you want. default: 4")

parser.add_argument(
    "--save_dir",
    default='./gallery',
    type=str,
    help="The output directory where the imgs downloaded. default: ./gallery")

parser.add_argument(
    "--index_file",
    default='./imgs_list.csv',
    type=str,
    help="The file include urls about img address. default: ./imgs_list.csv")

parser.add_argument("--use_validator",
                    action='store_true',
                    help="Whether check img validation by cv2.imread()")

args = parser.parse_args()


def check_img_valid(img_path, ignore=True):
    if ignore:
        return True
    import cv2
    img = cv2.imread(img_path)
    if img is None:
        return False
    else:
        return True

def send_requests(url, api_token='', max_retries=3):
    header = {"Authorization": api_token}

    i = 1
    content = None
    while i <= max_retries:
        try:
            r = requests.get(url, headers=header, stream=True, timeout=10)
            content = r.content
            return content
        except Exception as e:
            print(f"send requests {url} has error, {e}")
            print(f"will try {max_retries}, current times: {i}")
            i += 1
    return content

def download_img(img_url,
                 img_name=None,
                 api_token='',
                 output_dir='./gallery',
                 max_retries=3):

    assert img_url is not None, "please input your img_url"

    if img_name:
        suffix = img_url.rsplit('.', 1)[-1]
        img_name = f'{img_name}.{suffix}'
    else:
        img_name = img_url.rsplit('/', 1)[-1]

    # create output dir
    Path(output_dir).mkdir(exist_ok=True)
    im_local_path = f'{output_dir}/{img_name}'

    img_content = send_requests(img_url)

    if img_content is None:
        return
    else:
        with open(im_local_path, 'wb') as f:
            f.write(img_content)

        # check imgage
        ignore = True if not args.use_validator else False
        if check_img_valid(im_local_path, ignore=False):
            img_tag, _ = img_name.rsplit('_', 1)
            return f'{im_local_path} {img_tag}'
        else:
            try:
                print(f"{im_local_path} has broken, will delete it.")
                os.remove(im_local_path)
            except Exception as e:
                print(f"delete {im_local_path} failed, {e}")
            return


if __name__ == '__main__':

    start_time = time.perf_counter()
    imgs_info = pd.read_csv(args.index_file,
                            sep=' ',
                            names=['name', 'url'],
                            header=0)
    temp = imgs_info.groupby('name').url.unique()
    print('current process {0}'.format(os.getpid()))
    p = multiprocessing.Pool(processes=args.num_proc)
    r = []
    for name, img_urls in zip(temp.index, temp):
        for i, img_url in enumerate(img_urls):
            new_name = f'{name}_{i}'
            r.append(p.apply_async(download_img, args=(img_url, new_name)))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All processes done!')

    # get results from ervery sub process
    res = []
    for i in r:
        sub_res = i.get()
        if sub_res:
            res.append(sub_res)

    # write downloaded data index
    with open('./data_file.txt', 'w+') as f:
        for line in res:
            f.write(f'{line}\n')

    end_time = time.perf_counter()
    spent_time = end_time - start_time
    print(f"total time spent: {spent_time}")
