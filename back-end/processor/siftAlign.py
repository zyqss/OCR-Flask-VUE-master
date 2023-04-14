import cv2
import numpy as np
import os


def show(name ,img):
    img = cv2.resize(img, None, fx=0.3, fy=0.3)  # 看情况调用
    cv2.imshow(name, img)
    # 等待时间 毫秒级 0表示任意键终止
    cv2.waitKey(500)
    cv2.destroyAllWindows()

def sift_kp(image):

    if image is None:
        print("img is none")

    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # sift = cv2.xfeatures2d_SIFT.create()
    sift = cv2.SIFT_create()
    # sift = cv2.xfeatures2d.SIFT_create()
    kp,des = sift.detectAndCompute(image,None)
    kp_image = cv2.drawKeypoints(gray_image,kp,None)
    return kp_image,kp,des

def surf_kp(image):
    '''SIFT(surf)特征点检测(速度比sift快)'''
    height, width = image.shape[:2]
    size = (int(width * 0.2), int(height * 0.2))
    shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    gray_image = cv2.cvtColor(shrink,cv2.COLOR_BGR2GRAY)
    surf = cv2.xfeatures2d_SURF.create()
    kp, des = surf.detectAndCompute(gray_image, None)
    return kp,des

def get_good_match(des1,des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return good

# 特征点匹配和透视变换的核心代码
def siftImageAlignment(img1,img2):

   _,kp1,des1 = sift_kp(img1)
   _,kp2,des2 = sift_kp(img2)

   goodMatch = get_good_match(des1,des2)
   if len(goodMatch) > 4:
       ptsA= np.float32([kp1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
       ptsB = np.float32([kp2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
       ransacReprojThreshold = 4
       H, status =cv2.findHomography(ptsA,ptsB,cv2.RANSAC,ransacReprojThreshold);


       imgOut = cv2.warpPerspective(img2, H, (img1.shape[1],img1.shape[0]),flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
       return imgOut,H,status


def get_sandard_card(img):
    """
    :param img: 传入待摆正的图片
    :param ctype: 传入一个整数,0代表身份证背面，1代表身份证正面 2代表社保卡背面 3代表社保卡反面
    :return: 返回一个图片
    """

    img1 = cv2.imread(r'./template/idb_template.png')


    result, h, status = siftImageAlignment(img1,img)
    result, h, status = siftImageAlignment(img1,result)
    #保存中间结果
    cv2.imwrite('./standard_pic/'+'aobama.jpg',result)
    return result







