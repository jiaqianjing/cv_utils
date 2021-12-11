import argparse
import multiprocessing
import os
from pathlib import Path

import pandas as pd
import requests

parser = argparse.ArgumentParser()

parser.add_argument("--num_proc",
                    default=4,
                    type=int,
                    help="How many cpu cores you want. default: 4")

parser.add_argument("--save_dir",
                    default='./gallery',
                    type=str,
                    help="The output directory where the imgs downloaded. default: ./gallery")

parser.add_argument("--index_file",
                    default='./imgs_list.csv',
                    type=str,
                    help="The file include urls about img address. default: ./imgs_list.csv")

args = parser.parse_args()


def download_img(img_url, img_name=None, api_token='', output_dir='./gallery'):

    assert img_url is not None, "please input your img_url"

    if img_name:
        suffix = img_url.rsplit('.', 1)[-1]
        img_name = f'{img_name}.{suffix}' 
    else:
        img_name = img_url.rsplit('/', 1)[-1]

    # create output dir
    Path(output_dir).mkdir(exist_ok=True)

    header = {"Authorization": api_token}
    r = requests.get(img_url, headers=header, stream=True)
    if r.status_code == 200:
        open(f'{output_dir}/{img_name}', 'wb').write(r.content)
    del r
    img_tag, _ = img_name.rsplit('_', 1)
    return f'{output_dir}/{img_name} {img_tag}'


if __name__ == '__main__':

    imgs_info = pd.read_csv(args.index_file, sep=' ', names=['name', 'url'], header=0)
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

    # 获取每个进程的结果
    res = []
    for i in r:
        res.append(i.get())
    
    # write downloaded data index
    with open('./data_file.txt', 'w+') as f:
        for line in res:
            f.write(f'{line}\n')
