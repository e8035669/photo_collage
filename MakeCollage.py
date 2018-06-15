#!/usr/bin/env python
# -*- coding=utf-8 -*-
import cv2
import argparse
import numpy as np
import os.path
import sys

def calError(c1, c2):
    e1 = ((int(c1[0]) - int(c2[0])) ** 2) * 1
    e2 = ((int(c1[1]) - int(c2[1])) ** 2) * 0.5
    e3 = ((int(c1[2]) - int(c2[2])) ** 2) * 0.5
    return e1 + e2 + e3

def makePicture(img, dbDir, fileNames, colors):
    dbImgSize = cv2.imread(os.path.join(dbDir, fileNames[0])).shape[0]
    print 'found dbImgSize = ', str(dbImgSize)
    if cv2.__version__ > '3':
        yccPic = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    else:
        yccPic = cv2.cvtColor(img, cv2.cv.CV_BGR2YCrCb)
    selectedIndex = np.zeros((img.shape[0], img.shape[1]), np.int32)
    bigPic = np.zeros((img.shape[0] * dbImgSize, img.shape[1] * dbImgSize, 3), np.uint8)
    print 'calculate errors...'
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            #func = lambda c: calError(yccPic[y,x], c)
            #tmpArr = np.apply_along_axis(func, 1, colors)
            #index = np.argmin(tmpArr)
            #print tmpArr[index]

            index = 0
            error = calError(yccPic[y,x], colors[0,:])
            for i in range(len(fileNames)):
                e = calError(yccPic[y,x], colors[i,:])
                if e < error:
                    index = i
                    error = e
            selectedIndex[y,x] = index

        string = '\rprocessing... %.2f%%' % ((y+1) * 100.0 /img.shape[0])
        sys.stdout.write(string)
        sys.stdout.flush()

    print ''
    print 'combine pictures...'
    imgList = [None] * len(fileNames)

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            index = selectedIndex[y,x]
            if imgList[index] is None:
                imgList[index] = cv2.imread(os.path.join(dbDir, fileNames[index]))

            bigPic[y*dbImgSize : (y+1)*dbImgSize, x*dbImgSize:(x+1)*dbImgSize,:] = imgList[index]

    return bigPic


def parseRawFile(data):
    fileNames = []
    colors = np.zeros((len(data), 3))
    index = 0
    for item in data:
        tmp = item.split(',')
        if len(tmp) == 4:
            fileNames.append(tmp[0])
            colors[index, 0] = float(tmp[1])
            colors[index, 1] = float(tmp[2])
            colors[index, 2] = float(tmp[3])
        else:
            raise RuntimeError("invalid data")
        index = index + 1
    return fileNames, colors



def makeCollage(inputPic, scale, database, outputPic = None):
    img = cv2.imread(inputPic)
    rawFile = None
    with open(os.path.join(database, 'table.txt')) as f:
        rawFile = f.readlines()

    fileNames, colors = parseRawFile(rawFile)
    print 'imput image scale = ', str(scale)
    img = cv2.resize(img, None, fx = scale, fy = scale)
    bigPic = makePicture(img, database, fileNames, colors)
    if outputPic == None:
        outputPic = 'output.jpg'

    cv2.imwrite(outputPic, bigPic)
    print 'Save picture to: ', outputPic



def main():
    parser = argparse.ArgumentParser(description = 'Step3: Collage pictures into a big picture\n' +
            '第三步：輸入一張照片還有小圖片資料庫 會用小圖片去拼貼成這張大圖片')
    parser.add_argument('-i', '--input',
            help = 'input a picture 輸入一張圖片', required = True)
    parser.add_argument('-o', '--output',
            help = 'where to put your picture 拼貼的照片輸出的位置',
            default = None)
    parser.add_argument('-d', '--database',
            help = 'dir of image database 小圖片資料庫的資料夾位置', required = True)
    parser.add_argument('-s', '--scale',
            help = 'scale of input image 這會將輸入的圖片縮小 預設0.1倍',
            default = 0.1, type = float)
    args = parser.parse_args()
    makeCollage(args.input, args.scale, args.database, args.output)





if __name__ == '__main__':
    main()
