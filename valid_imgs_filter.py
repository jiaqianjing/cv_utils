import argparse
import multiprocessing
import os
import cv2
import time

parser = argparse.ArgumentParser()

parser.add_argument("--num_proc",
                    default=4,
                    type=int,
                    help="How many cpu cores you want. default: 4")

parser.add_argument(
    "--index_file",
    default='./data_file.txt',
    type=str,
    help="The file include local path about img. default: ./data_file.txt")

args = parser.parse_args()


# 筛选有效图片
def get_valid_imgs(records):
    valid_data = []
    for record in records:
        im_file, im_name = record
        img = cv2.imread(im_file)
        if img is not None:
            valid_data.append(f'{im_file} {im_name}')
    return valid_data


# 组 batch
def get_batch(list_temp, batch_size):
    for i in range(0, len(list_temp), batch_size):
        yield list_temp[i:i + batch_size]


def text2list(index_file_name, sep=' '):
    raw_file_list = []
    with open(index_file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            im_file, im_name = line.strip().split(sep)
            raw_file_list.append((im_file, im_name))
    return raw_file_list


def list2text(temp_list, output_file_name):
    with open(output_file_name, 'w+') as f:
        for line in temp_list:
            f.write(f'{line}\n')


def file_rename(src_name, tgt_name):
    try:
        os.rename(src_name, tgt_name)
    except Exception as e:
        print(f"{src_name} rename {tgt_name} has error, {e}")


if __name__ == '__main__':

    start_time = time.perf_counter()
    n_process = args.num_proc

    raw_file_list = text2list(args.index_file)
    batch_size = len(raw_file_list) // n_process
    print(f"batch_size: {batch_size}, n_process: {n_process}")

    print('current process {0}'.format(os.getpid()))
    p = multiprocessing.Pool(processes=n_process)
    r = []
    for batch in get_batch(raw_file_list, batch_size):
        r.append(p.apply_async(get_valid_imgs, (batch, )))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All processes done!')

    total_valid_imgs = []
    for i in r:
        total_valid_imgs.extend(i.get())

    file_rename(args.index_file, f'{args.index_file}.bak')
    list2text(total_valid_imgs, args.index_file)
    end_time = time.perf_counter()
    spent_time = end_time - start_time
    print(f"total time spent: {spent_time}")