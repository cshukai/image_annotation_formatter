import os
import glob
from pyspark.sql import SparkSession
from xml.etree.ElementTree import Element, SubElement, Comment, tostring,ElementTree
import xml.etree.ElementTree as ET

spark = SparkSession.builder.master("local[20]").appName('cvpr').getOrCreate()

voclist=glob.glob("voc/*.xml")

def getBoxAndSize(path):
    tree = ET.parse(path)
    root = tree.getroot()
    xmaxs=[]
    for xmax in root.iter('xmax'):
        xmax=int(xmax.text) # need change for multiple xmax
        xmaxs.append(xmax)    
    xmins=[]
    for xmin in root.iter('xmin'):
        xmin=int(xmin.text)
        xmins.append(xmin) 
    ymaxs=[]   
    for ymax in root.iter('ymax'):
        ymax=int(ymax.text)
        ymaxs.append(ymax)
    ymins=[]    
    for ymin in root.iter('ymin'):
        ymin=int(ymin.text)         
        ymins.append(ymin)
        
    for width in root.iter('width'):
        width=int(width.text) 
    
    for height in root.iter('height'):
        height=int(height.text) 
    
    filename=root.find('filename').text
    
    return(width,height,xmaxs,xmins,ymaxs,ymins,filename)


def findWrongBndBox(width,height,xmaxs,xmins,ymaxs,ymins,filename):
    badImgList=[]
    for idx,xmax in enumerate(xmaxs):
        if xmax > width:
            badImgList.append(filename)
        if  xmins[idx]<0:
            badImgList.append(filename)
        if  ymins[idx]<0:
            badImgList.append(filename)
        if  ymaxs[idx]>height :
            badImgList.append(filename)
    if badImgList==[] :
       badImgList.append("not_found")
    return(badImgList)        

vocrdd=spark.sparkContext.parallelize(voclist)
bnds_imgs=vocrdd.map(lambda path:getBoxAndSize(path))
badfilerdd=bnds_imgs.map(lambda bnd_img:findWrongBndBox(bnd_img[0],bnd_img[1],bnd_img[2],bnd_img[3],bnd_img[4],bnd_img[5],bnd_img[6])).filter(lambda x:x!=['not_found'])

badfilerdd.saveAsTextFile("badfiles.txt")
