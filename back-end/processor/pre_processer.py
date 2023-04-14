from .cut_text_area import get_text_area
from .siftAlign import get_sandard_card
import cv2
import os
from PIL import Image
from paddleocr import PaddleOCR,draw_ocr
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"



""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def get_pic_info(filename):


    font = cv2.FONT_HERSHEY_SIMPLEX


    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False,
                    rec_model_dir='./models/ch_ppocr_server_v2.0_rec_infer/',
                    cls_model_dir='./models/ch_ppocr_mobile_v2.0_cls_infer/',
                    det_model_dir='./models/ch_ppocr_server_v2.0_det_infer/')
    results = ocr.ocr(filename, cls=True)

    # 文本识别信息
    image = Image.open(filename).convert('RGB')
    boxes = [line[0] for line in results]
    txts = [line[1][0] for line in results]
    scores = [line[1][1] for line in results]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
    im_show = Image.fromarray(im_show)

    # 置信度
    a = sum(scores)
    b = len(scores)
    conf_all = a/b

    return txts, conf_all

def formated(res):
    if '姓名' in res:
        res = 'name: ' + res[2:]
    elif '性别' in res:
        res = 'sex: ' + res[2:]
    elif '民族' in res:
        res = 'nation: ' + res[2:]
    elif '出生' in res:
        res = 'born: ' + res[2:]
    elif '住址' in res :
        res = 'address: ' + res[2:]
    elif '公民身份号码' in res:
        res = 'id: ' + res[6:]
    return  res

def formated1(res):
    if '姓名' in res:
        res = ' ' + res[2:]
    elif '性别' in res:
        res = ' ' + res[2:]
    elif '民族' in res:
        res = ' ' + res[2:]
    elif '出生' in res:
        res = ' ' + res[2:]
    elif '住址' in res :
        res = ' ' + res[2:]
    elif '公民身份号码' in res:
        res = ' ' + res[6:]
    return  res

# 按排列顺序
idb_info_list = ['name', 'sexual', 'nation', 'date', 'addr', 'id']


def pre_processer1(path):
    # 0. 摆正身份证背面
    img = cv2.imread(path)
    # img0是摆正好的图片
    
    standimg = get_sandard_card(img)


    #获取文字区域
    res_dict = get_text_area(standimg)

    tmplist = idb_info_list

    # 按顺序保存
    for i in range(len(tmplist)):
        name = tmplist[i]
        img = res_dict[name]
        cv2.imwrite('output'+'\\'+str(i)+'.jpg',img)






