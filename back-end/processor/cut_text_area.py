import sys
import numpy as np
import cv2



def cut_text(img,pts):
    pts = pts.tolist()
    minx = 99999
    miny = 99999
    maxx = -11
    maxy = -11


    for pt in pts:
        maxy = max(maxy,pt[1])
        maxx = max(maxx,pt[0])
        minx = min(minx,pt[0])
        miny = min(miny,pt[1])



    return img[miny:maxy,minx:maxx]



def get_boxs(img):
    backup = img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化图片
    ret, th = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    kernel = np.ones((10, 20), np.uint8)
    # 开运算
    closing = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    # 腐蚀
    kernel = np.ones((5, 10), np.uint8)
    dilation = cv2.erode(closing, kernel, iterations=1)
    #  查找和筛选文字区域
    region = []
    #  查找轮廓
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 利用以上函数可以得到多个轮廓区域，存在一个列表中。
    #  筛选那些面积小的
    for i in range(len(contours)):
        # 遍历所有轮廓
        # cnt是一个点集
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)
        # 面积小的都筛选掉、这个300可以按照效果自行设置
        if (area < 300):
            continue
        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        # 筛选那些太细的矩形，留下扁的
        if (height > width):
            continue
        region.append(box)
    return region



def getvalue(pts):
    pts = pts.tolist()
    minx = 99999
    miny = 99999
    maxx = -11
    maxy = -11


    for pt in pts:
        maxy = max(maxy, pt[1])
        maxx = max(maxx, pt[0])
        minx = min(minx, pt[0])
        miny = min(miny, pt[1])

    return miny



def get_text_area(img):
    mask = cv2.imread('./masks/idbmask0.png')
    mask = cv2.resize(mask, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC) #大小
    boxs = get_boxs(mask)

    names = ['name','sexual','nation','date','addr','id']
    #按坐标排序
    boxs= sorted(boxs, key=getvalue)
    idx = 0;
    img_dict = {}
    for pt in boxs:
        # 保存到本地，方便查看中间结果
        img_dict[names[idx]] = cut_text(img, pt)
        idx += 1
    return img_dict


