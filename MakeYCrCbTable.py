#!/usr/bin/env python
# -*- coding=utf-8 -*-

import argparse
import glob
import os.path
import cv2
import numpy as np

def calculateAvg(img):
    return img.mean(axis = 0).mean(axis = 0)

def makeTable(inputDir):
    fileList = glob.glob(os.path.join(inputDir, '*.jpg'))
    msgList = []
    for f in fileList:
        msg = os.path.basename(f)
        img = cv2.imread(f)
        if cv2.__version__ > '3':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        else:
            img = cv2.cvtColor(img, cv2.cv.CV_BGR2YCrCb)
        mean = calculateAvg(img)
        for i in mean:
            msg = msg + ', ' + str(i)

        msg = msg + '\n'
        msgList.append(msg)

    print 'Calculate %d pics.' % len(msgList)

    with open(os.path.join(inputDir, 'table.txt'),'w') as tableFile:
        tableFile.writelines(msgList)



def main():
    parser = argparse.ArgumentParser(
            description = 'Step2: Make a YCrCb table into a file\n' +
            '第二步：把小圖片資料庫裡面的照片進行標記\n' +
            '會把每張照片從RGB轉到YCrCb的色彩空間\n' +
            '再取整張照片YCrCb的平均值 最後寫入table.txt的檔案')
    parser.add_argument('-i', '--input',
            help = 'input dir that has lots of images 輸入小圖片資料庫',
            required = True)
    #args.add_argument('-o', '--output',
    #        help = 'output file will has lists of information')

    args = parser.parse_args()
    #print args
    makeTable(args.input)



if __name__ == '__main__':
    main()
