# cv_utils

## Deps
```shell
pip isntall -r requirement.txt -i http://mirrors.cloud.aliyuncs.com/pypi/simple/
```
## Download-Image (Multi-Process)
1. prerequirement
   You should have file that has img urls. e.g. `imgs_list.csv`
   
2. quick start
   ```shell`
   python download_imgs.py --num_proc 4 --save_dir './gallery' --index_file './imgs_list.csv'
   ```
## Valid-Image-Filter (MultiProcess)
1. prerequirement
    You should have file that has img local paths. e.g. `data_file.txt`
    *Tips: the file you can get it by executing `Download-Image`*

2. quick start
    ```shell
    python valid_imgs_filter.py --num_proc 4 --index_file 'data_file.txt'
    ```
