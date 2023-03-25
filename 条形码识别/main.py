#!/usr/bin/env python
# -*- coding: utf-8 -*-

# opencv读取的图片是BGR
import cv2
from PIL import Image, ImageDraw, ImageFont
# import matplotlib.pyplot as plt
# import numpy as np
import pyzbar.pyzbar as pyzbar
from pyzbar.pyzbar import ZBarSymbol

if __name__ == "__main__":
    video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    last_result = 0
    if video.isOpened():
        ret, frame = video.read()
    else:
        ret = False

    while ret:
        ret, frame = video.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # barcodes = pyzbar.decode(gray, symbols=[ZBarSymbol.CODE128])
        barcodes = pyzbar.decode(frame, symbols=[ZBarSymbol.CODE128])
        cv2.imshow('1', frame)
        if cv2.waitKey(5) & 0xff == 27:
            break

        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            if (last_result == 0) or (last_result != barcodeData):

                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

                # if w > 255 and h > 50:
                img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                font = ImageFont.truetype('arialbd.ttf', 25)
                fillColor = (0, 255, 0)
                position = (x, y - 25)

                draw = ImageDraw.Draw(img_PIL)
                draw.text(position, barcodeData, font=font, fill=fillColor)
                img_PIL.save('Identification_results.jpg')
                print("Recognize result>>> type： {0}  content： {1}".format(barcodeType, barcodeData))

                last_result = barcodeData
        if frame is None:
            break
    video.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 销毁窗口
