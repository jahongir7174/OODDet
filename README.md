This is the source code of 2<sup>nd</sup> place solution for Object Detection track in [ECCV 2022 | OOD-CV](https://www.ood-cv.org/challenge.html) Workshop Challenge

#### Steps

* Download [ROBIN](https://github.com/eccv22-ood-workshop/ROBIN-dataset) dataset
* Convert annotation from `csv` format to `coco` using [CSV2COCO](https://github.com/jahongir7174/ROBIN) converter
* Run `bash ./main.sh ./nets/exp01.py $ --train` for training

#### Dataset structure
    ├── ROBINv1.1 
        ├── train
            ├── images
            ├── train.json
        ├── iid_test
            ├── images
            ├── iid_test.json