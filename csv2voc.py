################what this script does##########
#1. convert annotation in csv to voc xml format
#2. convert normalized (0-1) bounding box positions to conventional coordinate system
################################

import pandas as pd
import glob
import cv2
from xml.etree.ElementTree import Element, SubElement, Comment, tostring,ElementTree
import os


anns=glob.glob("/home/shchang/scratch/cvpr/data/ann/*bbox.csv")
imgs=glob.glob("/home/shchang/scratch/cvpr/data/train_0*/*.jpg")
out_ann="/home/shchang/scratch/cvpr/data/ann/voc"
out_img="/home/shchang/scratch/cvpr/data/img"

for idx,path in enumerate(anns):
    ann=pd.read_csv(path,delimiter=",")
    for iidx,ipath in enumerate(imgs):
        
        img=cv2.imread(ipath,-1)
        img_id=ipath.split("/")[-1].split(".")[0]
        filename=ipath.split("/")[-1]
        w=img.shape[1]
        h=img.shape[0]
        
        x=ann[ann['ImageID'] == img_id]
        
        #child_lel
        top = Element('annotation')
        child_1_fname = SubElement(top, 'filename')
        child_1_fname.text= filename
        child_1_path = SubElement(top, 'path')
        child_1_path.text= ipath
        child_1_size= SubElement(top,'size')
        child_2_width=SubElement(child_1_size,'width')
        child_2_width.text=w
        child_2_height=SubElement(child_1_size,'height')
        child_2_height.text=h
        child_2_channel=SubElement(child_1_size,'depth')
        child_2_channel.text=img.shape[2]
        child_1_obj=SubElement(top,'object')
        for xi,row in x.iterrows():
            child_2_label=SubElement(child_1_obj,'name')
            child_2_label.text=row['LabelName']
            child_2_bnd=SubElement(child_1_obj,'bndbox')
            child_3_xmax=SubElement(child_2_bnd,'xmax')
            child_3_xmax.text=str(w*row['XMax'])
            child_3_xmin=SubElement(child_2_bnd,'xmin')
            child_3_xmin.text=str(w*row['XMin'])
            child_3_ymax=SubElement(child_2_bnd,'ymax')
            child_3_ymax.text=str(h*row['YMax'])
            child_3_ymin=SubElement(child_2_bnd,'ymin')
            child_3_ymin.text=str(h*row['Ymin'])
            
        path_ann=out_ann+"/"+img_id+".xml"
        ElementTree(top).write(path_ann)
        path_img=out_img+"/"+filename
        cv2.imwrite(path_img,img)
        os.remove(ipath)
        
        
        
