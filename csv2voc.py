################what this script does##########
#1. convert annotation in csv to voc xml format
#2. convert normalized (0-1) bounding box positions to conventional coordinate system

###############################################


import pandas as pd
import glob
import xml.etree.ElementTree as ET

anns=glob.glob("/home/shchang/scratch/cvpr/data/ann/*bbox.csv")
imgs=glob.glob("/home/shchang/scratch/cvpr/data/train_0*/*.jpg")
for idx,path in enumerate(anns):
    ann=pd.read_csv(path,delimiter=",")
    
