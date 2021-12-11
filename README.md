# cv_utils

## Deps
```shell
pip isntall -r requirement.txt -i http://mirrors.cloud.aliyuncs.com/pypi/simple/
```
## Download-Image (Multi-Process)
1. prerequisite  
   You should have file that has img urls. e.g. `imgs_list.csv`
   
2. quick start  
   ```shell
   # clean useless files.
   rm -rf data_file.txt data_file.txt.bak gallery
   
   # Do not check img is valid after img downloded.
   python download_imgs.py --num_proc 4 --save_dir './gallery' --index_file './imgs_list.csv'

   # Will filter out damaged pictures after img downloaded.
   python download_imgs.py --num_proc 4 --save_dir './gallery' --index_file './imgs_list.csv' --use_validator
   ```
## Filter-Dmaged-Image (MultiProcess)
1. prerequisite  
    You should have file that has img local paths. e.g. `data_file.txt`  
    *Tips: the file you can get it by executing `Download-Image`*  

2. quick start  
    ```shell
    python filter_damaged_imgs.py --num_proc 4 --index_file 'data_file.txt'
    ```
