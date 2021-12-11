import argparse
import multiprocessing
import os
import cv2

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


# 筛选有效图片
def get_valid_imgs(records):
    valid_data = []
    for record in records:
        im_file, _ = record
        img = cv2.imread(im_file)
        if img is not None:
            valid_data.append(record)
    return valid_data

# 组 batch
def get_batch(list_temp, batch_size):
    for i in range(0, len(list_temp), batch_size):
        yield list_temp[i:i + batch_size]

if __name__ == '__main__':

    n_process = args.num_proc


            
    batch_size = len(raw_file_list) // n_process
    print(f"batch_size: {batch_size}, n_process: {n_process}")


    import multiprocessing
    import os
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
