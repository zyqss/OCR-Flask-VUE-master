import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import shutil
from PIL import Image

font = cv2.FONT_HERSHEY_SIMPLEX

# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False,
                rec_model_dir='./models/ch_ppocr_server_v2.0_rec_infer/',
                cls_model_dir='./models/ch_ppocr_mobile_v2.0_cls_infer/',
                det_model_dir='./models/ch_ppocr_server_v2.0_det_infer/')  # need to run only once to download and load model into memory

# 销售方字典
purchaser_dict = ['purchaserName', 'purchaserCode', 'purchaserAddrTel', 'purchaserBankCode']
seller_dict = ['sellerName', 'sellerCode', 'sellerAddrTel', 'sellerBankCode']
invoice_dict = ['invoiceCode', 'invoiceNumber', 'invoiceDate', 'checkCode']

# 截取图片中部分区域图像-字段
crop_range_list_name = ['invoice', 'purchaser', 'seller',
                        'totalExpense', 'totalTax', 'totalTaxExpenseZh', 'totalTaxExpense',
                        'remark', 'title', 'machineCode']
# 截取图片中部分区域图像-坐标
crop_range_list_data = [[1700, 20, 600, 250], [420, 280, 935, 220], [420, 1030, 935, 230],
                        [1500, 880, 390, 75], [2000, 880, 330, 75], [750, 960, 600, 65], [1870, 960, 300, 70],
                        [1455, 1045, 400, 180], [760, 50, 900, 110], [280, 200, 250, 75]]

# 后续生成票据图像时的大小，按照标准增值税发票版式240mmX140mm来设定
height_resize = 1400
width_resize = 2400

def resizeImg(image, height=height_resize):
    h, w = image.shape[:2]
    pro = height / h
    size = (int(w * pro), int(height))
    img = cv2.resize(image, size)
    return img

# 边缘检测
def getCanny(image):
    # 高斯模糊
    binary = cv2.GaussianBlur(image, (3, 3), 2, 2)
    # 边缘检测
    binary = cv2.Canny(binary, 60, 240, apertureSize=3)
    # 膨胀操作，尽量使边缘闭合
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)

    # 二值图
    # cv2.imwrite('result/binary.jpg', binary)
    return binary

# 求出面积最大的轮廓
def findMaxContour(image):
    # 寻找边缘
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 计算面积
    max_area = 0.0
    max_contour = []
    for contour in contours:
        current_area = cv2.contourArea(contour)
        if current_area > max_area:
            max_area = current_area
            max_contour = contour
    return max_contour, max_area

# 多边形拟合凸包的四个顶点
def getBoxPoint(contour):
    # 多边形拟合凸包
    hull = cv2.convexHull(contour)
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(hull, epsilon, True)
    approx = approx.reshape((len(approx), 2))
    return approx

# 适配原四边形点集
def adapPoint(box, pro):
    box_pro = box
    if pro != 1.0:
        box_pro = box / pro
    box_pro = np.trunc(box_pro)
    return box_pro

# 四边形顶点排序，[top-left, top-right, bottom-right, bottom-left]
def orderPoints(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

# 计算长宽
def pointDistance(a, b):
    return int(np.sqrt(np.sum(np.square(a - b))))


# 透视变换
def warpImage(image, box):
    w, h = pointDistance(box[0], box[1]), \
           pointDistance(box[1], box[2])
    dst_rect = np.array([[0, 0],
                         [w - 1, 0],
                         [w - 1, h - 1],
                         [0, h - 1]], dtype='float32')
    M = cv2.getPerspectiveTransform(box, dst_rect)
    warped = cv2.warpPerspective(image, M, (w, h))
    return warped

# 根据四点画四边形
def drawRect(img, pt1, pt2, pt3, pt4, color, line_width):
    cv2.line(img, pt1, pt2, color, line_width)
    cv2.line(img, pt2, pt3, color, line_width)
    cv2.line(img, pt3, pt4, color, line_width)
    cv2.line(img, pt1, pt4, color, line_width)

# 统合图片预处理
def imagePreProcessing(path):
    image = cv2.imread(path)
    # 转灰度、降噪
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # image = cv2.GaussianBlur(image, (3,3), 0)

    # 边缘检测、寻找轮廓、确定顶点
    ratio = height_resize / image.shape[0]
    img = resizeImg(image)
    binary_img = getCanny(img)
    max_contour, max_area = findMaxContour(binary_img)
    box = getBoxPoint(max_contour)
    boxes = adapPoint(box, ratio)
    boxes = orderPoints(boxes)
    # 透视变化
    warped = warpImage(image, boxes)
    # 调整最终图片大小
    size = (width_resize, height_resize)
    warped = cv2.resize(warped, size, interpolation=cv2.INTER_CUBIC)

    # 画边缘框
    drawRect(image, tuple(boxes[0]), tuple(boxes[1]), tuple(boxes[2]), tuple(boxes[3]), (0, 0, 255), 2)
    # cv2.imwrite("result1/outline.jpg", image)

    return warped

# 截取区域图片
def cropImage_test(img, crop_range):
    xpos, ypos, width, height = crop_range
    crop = img[ypos:ypos + height, xpos:xpos + width]
    return crop



# paddleOCR识别截取图片信息
def get_receipt_info(filename):
    text_crop = ''

    if not os.path.exists('./ocr_result'):
        os.mkdir('./ocr_result')
    else:
        shutil.rmtree('./ocr_result')
        os.mkdir('./ocr_result')

    font = cv2.FONT_HERSHEY_SIMPLEX


    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False,
                    rec_model_dir='./models/ch_ppocr_server_v2.0_rec_infer/',
                    cls_model_dir='./models/ch_ppocr_mobile_v2.0_cls_infer/',
                    det_model_dir='./models/ch_ppocr_server_v2.0_det_infer/')
    results = ocr.ocr(filename, cls=True)

    image = Image.open(filename).convert('RGB')
    boxes = [line[0] for line in results]
    txts = [line[1][0] for line in results]
    scores = [line[1][1] for line in results]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
    im_show = Image.fromarray(im_show)

    # 置信度
    # a = sum(scores)
    # b = len(scores)
    # conf_all = a / b


    text_crop_list = txts

    for i in range(len(text_crop_list)):
        ocr_text = ''.join(text_crop_list[i]).split(':')[-1].split(';')[-1]
        if '-' in ocr_text or '—' in ocr_text or '_' in ocr_text or '―' in ocr_text:
            continue
        text_crop = text_crop + ocr_text + ','
    # text_crop = ''.join(text_crop_list)

    return text_crop, scores







