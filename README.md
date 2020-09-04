This is a repo forked from https://github.com/ultralytics/yolov3 with modifications made by this project. 

This repo contains Ultralytics inference and training code for YOLOv3 in PyTorch. The code works on Linux, MacOS and Windows. Credit to Joseph Redmon for YOLO  https://pjreddie.com/darknet/yolo/ and YOLO-v3 https://github.com/ultralytics/yolov3.


## Requirements

Python 3.7 or later with all `requirements.txt` dependencies installed, including `torch >= 1.5`. To install run:
```bash
$ pip install -U -r requirements.txt
```


## Training

```bash
$ python3 train.py --data cfg/custom.data --weights '' --cfg cfg/yolov3-spp-3cls.cfg
```



## Inference
Detection using deep neural network model
```bash
python3 detect.py --source ... # 0 for webcam
```

Detection using contextual information
```bash
python3 detect.py /path/to/label/file/xxx.xlsx /path/to/image/folder/
```

## Pretrained Checkpoints provided by [yolov3](https://github.com/ultralytics/yolov3)

Download from: [https://drive.google.com/open?id=1LezFG5g3BCW6iYaV89B2i64cqEUZD7e0](https://drive.google.com/open?id=1LezFG5g3BCW6iYaV89B2i64cqEUZD7e0)

## Fine-tuned Checkpoints provided by this project

Download from [here]()


## Self collected dataset

Download from [here](https://drive.google.com/open?id=1LezFG5g3BCW6iYaV89B2i64cqEUZD7e0)




## Citation

[![DOI](https://zenodo.org/badge/146165888.svg)](https://zenodo.org/badge/latestdoi/146165888)



