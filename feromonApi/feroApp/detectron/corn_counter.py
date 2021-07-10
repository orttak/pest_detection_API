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
import os 
import json
import time  
import urllib.request


def to_coco(g_mask,h,w,im_name):

    results = []
    k=0
    for k,poly in enumerate(g_mask.polygons):
        x = np.min(poly[0::2])
        y = np.min(poly[1::2])
        h_y = np.max(poly[1::2]) - y
        w_x = np.max(poly[0::2]) - x
        
        result = {
            "id": k,
            "iscrowd": 0,
            "image_id": 1,
            "category_id": 0,
            "bbox": [x,y,w_x,h_y],
            "segmentation": [poly.tolist()]
            }
        results.append(result)
    my_coco_json = { "info":{"description":"my-project-name"},"licenses":[],"images":[{"id": 1, "width":w,"height":h,"file_name":im_name } ],"annotations":results,"categories":[{"id":0,"name":"kernel"}]}
    #with open(pth_images_test +  im_name.split('.')[0] + '.json', 'w') as outfile:
        #json.dump(my_coco_json , outfile)
    
    # bu k+1 sebebi nedir
    return my_coco_json,k
        
  



def corn_inference_width(img_url,im_name,resize_factor = 0.5,kernel_size = 3,itt_size = 15):

    cfg = get_cfg()
    cfgFile = "/home/appuser/detectron2_repo/detectron2/model_zoo/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    cfg.merge_from_file(cfgFile)
    cfg.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'corn_counter_weights/corn_halves')
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")   
    cfg.MODEL.DEVICE = "cuda"
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = (512) 
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8
    cfg.TEST.DETECTIONS_PER_IMAGE = 100
    predictor = DefaultPredictor(cfg)

    
    input_jpeg=urllib.request.urlretrieve(img_url,'input2.jpeg') 
    im = cv2.imread(input_jpeg[0])
    
    outputs = predictor(im)
    H_og,W_og,c = im.shape
    predictions = outputs["instances"].to("cpu")    
    masks = np.asarray(predictions.pred_masks)
    mask = np.sum(masks.astype(np.uint8), axis=0)>0
    g_mask = GenericMask(mask, H_og, W_og)    
    json_file,k = to_coco(g_mask,W_og,H_og,im_name)

    #cv2.imwrite(out_path + str(img_dir).split('.')[0] + 'res_mask.jpg',mask*255  )
    #cv2.imwrite(out_path + str(img_dir).split('.')[0] +'res_masked.jpg',np.dstack((1-mask,1-mask,1-mask))*img  )
    return json_file,k

    
    
def corn_inference_hight(img_url,im_name,resize_factor = 0.5,kernel_size = 3,itt_size = 15):
    cfg = get_cfg()
    cfgFile = "/home/appuser/detectron2_repo/detectron2/model_zoo/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    cfg.merge_from_file(cfgFile)
    cfg.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'corn_counter_weights/corn_frontside')
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")   
    cfg.MODEL.DEVICE = "cuda"
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = (1) 
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.425
    cfg.TEST.DETECTIONS_PER_IMAGE = 200
    predictor = DefaultPredictor(cfg)
    kernel = np.ones((kernel_size,kernel_size),np.uint8)

    input_jpeg=urllib.request.urlretrieve(img_url,'input2.jpeg') 
    im = cv2.imread(input_jpeg[0])   

    H_og,W_og,c = im.shape
    img = cv2.resize(im, (0,0), fx=resize_factor, fy=resize_factor,interpolation = cv2.INTER_LANCZOS4 )

    #bu kisim hic bir yerde kullanilmamis
    #im_og = img.copy()
    # alt blok iki tane var. gereksiz gibi
    #img = cv2.resize(img, (0,0), fx=resize_factor, fy=resize_factor,interpolation = cv2.INTER_LANCZOS4 )
    outputs = predictor(img)
    h,w,c = img.shape
    predictions = outputs["instances"].to("cpu")
    masks = np.asarray(predictions.pred_masks)
    mask = np.sum(masks.astype(np.uint8), axis=0)>0
    mask = mask.astype(np.uint8)
    mask = cv2.erode(mask,kernel,iterations = 1)
    mask_tot = mask.copy().astype(np.uint8)
    
    for i in range(itt_size):  
        img = np.dstack((1-mask,1-mask,1-mask))*img
        img = img.astype(np.uint8)

        outputs = predictor(img)
        predictions = outputs["instances"].to("cpu")
        masks = np.asarray(predictions.pred_masks)
        mask = np.sum(masks.astype(np.uint8), axis=0)>0
        mask = mask.astype(np.uint8)
        mask = cv2.erode(mask,kernel,iterations = 1)
        mask_tot =   mask_tot + mask.astype(np.uint8)
   
    if(np.max(mask_tot) > 0):
        mask_tot = mask_tot/np.max(mask_tot)
        
    #cv2.imwrite(out_path + str(img_dir).split('.')[0] + 'res_mask.jpg',mask_tot*255  )
    #cv2.imwrite(out_path + str(img_dir).split('.')[0] +'res_masked.jpg',np.dstack((1-mask,1-mask,1-mask))*img  )
    

    mask_fullsize = cv2.resize(mask_tot, (W_og,H_og))
    g_mask = GenericMask(mask_fullsize>0, H_og, W_og)
    json_file,k = to_coco(g_mask,W_og,H_og,im_name)
    
    return json_file,k
    

def corn_inference(img_h_url,img_w_url):
    #img_h = cv2.imread(pth_images_test_h + '/' + img_dir_h)
    try:
        img_name_h=img_h_url.split('/')[-1]
    except:
        img_name_h='img_name_h'

    json_h, k_h = corn_inference_hight(img_url=img_h_url,im_name=img_name_h)

    #img_w = cv2.imread(pth_images_test_w + '/' + img_dir_w)  
    try:
        img_name_w=img_w_url.split('/')[-1]
    except:
        img_name_w='img_name_w'  
    json_w, k_w = corn_inference_width(img_url=img_w_url,im_name=img_name_w)
    
    return json_h,json_w,k_h

#print(corn_inference('https://doktar.azureedge.net/yieldestimationphoto/9b5c8f5f-220c-4990-afdb-b6dd74cc23c4.jpg','https://doktar.azureedge.net/yieldestimationphoto/7041ebf5-1ff8-4d33-a296-5381d94d134e.jpg'))