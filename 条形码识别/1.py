#!/usr/bin/env python
# -*- coding: utf-8 -*-


# opencv读取的图片是BGR
import cv2                              # 导入opencv库
from PIL import Image                   # 导入Pillow库
import numpy as np                      # 导入numpy库
import pyzbar.pyzbar as pyzbar          # 导入pyzbar库
from pyzbar.pyzbar import ZBarSymbol    # 导入pyzbar库中的条形码类别库

if __name__ == "__main__":
    video = cv2.VideoCapture(0)
    last_result = 0                     # 初始化last_result，防止输出重复信息

    while (video.isOpened()):           # 如果摄像头打开
        ret, frame = video.read()       # 读取每一帧图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将图像转化为灰度图，便于识别
        barcodes = pyzbar.decode(frame, symbols=[ZBarSymbol.CODE128])  # CODE128表示仅识别CODE128型条形码

        cv2.imshow('1', frame)
        if cv2.waitKey(50) & 0xff == 27:  # 27是Esc键的键码，按下Esc键退出程序
            break

        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")  # 将识别到条形码信息转化为utf-8字符集中的字符
            barcodeType = barcode.type  # 记录识别到的条形码类型，即CODE128

            if (last_result == 0) or (last_result != barcodeData):  # 避免输出重复信息

                (x, y, w, h) = barcode.rect  # 记录条形码在图像的位置
                if h > 30 and w > 30:        # 避免定位到的条形码框太小
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)  # 画出条形码区域
                    img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    img_PIL.save('Identification_results.jpg')  # 保存识别图像
                    # 输出识别信息
                    print("Recognize result>>> type： {0}  content： {1}".format(barcodeType, barcodeData))
                    last_result = barcodeData
        if frame is None:
            break
    video.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 销毁窗口

