#!/usr/bin/env python
# -*- coding=utf-8 -*-
import argparse
import cv2
import os
import os.path
import hashlib
import glob

def getSquare(img):
    rows, cols = img.shape[:2]
    if rows > cols:
        return img[(rows - cols)/2:(rows + cols)/2, :]
    elif cols > rows:
        return img[:, (cols - rows)/2:(cols + rows)/2]

    return img

def processImage(inputPath, outputPath, size):
    if not os.path.exists(outputPath):
        try:
            print 'try to make output directory: ', outputPath
            os.mkdir(outputPath)
            print 'make output directory success'
        except OSError as ex:
            print 'Cannot make directory'


    if os.path.isfile(inputPath):
        videoin = cv2.VideoCapture(inputPath)
        if videoin.isOpened():
            hasPic = True
            img = None
            while hasPic:
                for i in range(60):
                    videoin.grab()

                hasPic, img = videoin.read()
                if not hasPic:
                    break
                squareRoi = getSquare(img)
                smallPic = cv2.resize(squareRoi, (size,size))
                fileName = hashlib.md5(smallPic.data).hexdigest()
                filepath = os.path.join(outputPath, fileName + ".jpg")
                cv2.imwrite(filepath, smallPic)
                print 'Write file:', filepath
                #break

    elif os.path.isdir(inputPath):
        filenames = glob.glob(os.path.join(inputPath, '*.jpg'))
        for f in filenames:
            img = cv2.imread(f)
            squareRoi = getSquare(img)
            smallPic = cv2.resize(squareRoi, (size, size))
            fileName = hashlib.md5(smallPic.data).hexdigest()
            filepath = os.path.join(outputPath, fileName + ".jpg")
            cv2.imwrite(filepath, smallPic)
            print 'Write file:', filepath

def main():
    parser = argparse.ArgumentParser(
            description='Step1: make image into small pictures\n' +
            '第一步：把一個影片分割成很多張小圖片 做成一個小圖片資料庫')
    parser.add_argument('-i', '--input',
            help = 'input video or input folder\n輸入的影片檔',
            required = True)
    parser.add_argument('-o', '--output',
            help = 'output folder to put images\n小圖片要放置的資料夾',
            required = True)
    parser.add_argument('-s', '--size',
            help = 'output picture size * size\n輸出的圖片大小 預設100*100',
            default = '100',
            type = int)

    args = parser.parse_args()

    print 'image size = ', str(args.size)
    processImage(args.input, args.output, args.size)




if '__main__' == __name__:
    main()
