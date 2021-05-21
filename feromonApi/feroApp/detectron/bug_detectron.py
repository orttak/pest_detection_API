from detectron2.data.datasets import register_coco_instances
from detectron2.data import MetadataCatalog
from detectron2.data import DatasetCatalog
from detectron2.utils.visualizer import Visualizer
import random
import cv2
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
import os
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import GenericMask
import numpy as np
from detectron2.projects.point_rend import ColorAugSSDTransform, add_pointrend_config
import json
from detectron2.structures import Boxes, BoxMode, pairwise_iou

import os
import urllib.request

img_list=['https://doktar.azureedge.net/feromon/PheromoneTrap_14021014_20210123200213.jpg',
    'https://doktar.azureedge.net/feromon/PheromoneTrap_14021014_20210122200203.jpg']
JSON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'inputJson/a1.json')



def get_bug(img_url):
    #img_list=['https://doktar.azureedge.net/feromon/PheromoneTrap_14021014_20210123200213.jpg',
    #'https://doktar.azureedge.net/feromon/PheromoneTrap_14021014_20210122200203.jpg']
    
    data_path = os.path.dirname(os.path.realpath(__file__))
    dataset_name = "denmark_dataset"
    if dataset_name in DatasetCatalog.list():
        DatasetCatalog.remove(dataset_name)
    pth_images = os.path.join(os.path.dirname(os.path.realpath(__file__)),"BUG_COCO/images/14022407_Input")
    pth_json = os.path.join(os.path.dirname(os.path.realpath(__file__)),"BUG_COCO/annotations/14022407_Input.json")
    register_coco_instances(dataset_name , {}, pth_json , pth_images )
  

    dataset_metadata = MetadataCatalog.get(dataset_name)
    dataset_dicts = DatasetCatalog.get(dataset_name)

    cfg = get_cfg()
    cfgFile = "/home/appuser/detectron2_repo/detectron2/model_zoo/configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
    cfg.merge_from_file(cfgFile)
    cfg.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'weights_fldr2')
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.2  
    cfg.DATASETS.TEST = (dataset_name, )
    predictor = DefaultPredictor(cfg)

    pth_images_test = "./input_image/"

    with open('./mycat2.json') as json_file:
        mycat2 = json.load(json_file)['categories']

    img_name=img_url.split('/')[-1]
    input_jpeg=urllib.request.urlretrieve(img_url,'input.jpeg') 
    im = cv2.imread(input_jpeg[0])
    print(input_jpeg)
    outputs = predictor(im)
    predictions = outputs["instances"].to("cpu")
    h,w,c = im.shape
    v = Visualizer(im[:, :, ::-1],metadata=dataset_metadata, scale=0.8)
    for box in predictions.pred_boxes.to('cpu'):
        v.draw_box(box)
    v2 = v.get_output()
    #if you want to save the result image open below code blocks
    #output_img_path=os.path.join(data_path,'out/res_' + img_name+'.jpg')
    #cv2.imwrite(output_img_path,v2.get_image()[:, :, ::-1]) 
      
    instances = predictions 
    results = []
    boxes = instances.pred_boxes.tensor.numpy()
    boxes = BoxMode.convert(boxes, BoxMode.XYXY_ABS, BoxMode.XYWH_ABS)
    boxes = boxes.tolist()
    scores = instances.scores.tolist()
    classes = instances.pred_classes.tolist()	

    for k in range(len(instances)):
        x,y,bh,bw = boxes[k]
        x1 = x
        x2 = x +  bh
        y1 = y
        y2 = y + bw
        result = {
            "id": k,
            "iscrowd": 0,
            "image_id": 1,
            "category_id":902,# classes[k],
            "bbox": boxes[k],
            "M_BBOX": [x1,y1,x2,y1,x2,y2,x1,y2],
        }
        results.append(result)
    #break
    my_coco_json = { "info":{"description":"my-project-name"},"licenses":[],"images":[{"id": 1, "width":w,"height":h,"file_name":img_name} ],"annotations":results,"categories":mycat2}
    json_name = str(img_name)+ '_res_new22.json'
    with open('out/' + json_name, 'w') as outfile:
         print('done!')
         json.dump(my_coco_json , outfile)
    return my_coco_json


import sys
if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = None

    return_val = get_bug(arg)
