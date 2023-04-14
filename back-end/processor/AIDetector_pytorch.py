import paddlehub as hub
import shutil
import os
import numpy as np
from .pre_processer import pre_processer1, formated, get_pic_info, formated1
from .fapiao_detector import imagePreProcessing, cropImage_test, get_receipt_info
from .ticket_detector import imagePreProcessing1, cropImage_test1,get_ticket_info,get_ticket_info2
from  .business_detector import  imagePreProcessing2,cropImage_test,get_business_info
import cv2

class Detector(object):

    def __init__(self):
        self.init_model()

    def init_model(img):

        # ****************采用paddlehub预测文字区域************/
        model = hub.Module(name="chinese_ocr_db_crnn_mobile")
        # 服务端可以加载大模型，效果更好
        # ocr = hub.Module(name="chinese_ocr_db_crnn_server")
        # 读取照片路径
        np_images = [cv2.imread(img)]

        results = model.recognize_text(
            images=np_images,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
            output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
            visualization=True,  # 是否将识别结果保存为图片文件；
            box_thresh=0.5,  # 检测文本框置信度的阈值；
            text_thresh=0.5)  # 识别中文文本置信度的阈值；

        # 预测 paddleocr/切割预测
        pre_processer1(img)
        records_list = []
        image_info = {}
        id_info = {}
        data = []
        key = '身份证信息'
        count = 0
        for i in range(6):
            info, conf_all = get_pic_info('./output/' + str(i) + '.jpg')
            res = ''
            for item in info:
                res += item
                count += 1
            data.append(formated1(res))
            records_list.append(formated(res))
        for filename in os.listdir('./ocr_result'):
            im = cv2.imread('./ocr_result' + "/" + filename)
        image_info[key] = [np.round(float(conf_all), 3), records_list]
        id_info[data[0]] = [data[1], data[2], data[3], data[4], data[5]]

        print("识别成功")

        return im, image_info, id_info


    def main_model(img):
        # 待预测图片
        # 加载移动端预训练模型
        model = hub.Module(name="chinese_ocr_db_crnn_mobile")
        # 服务端可以加载大模型，效果更好
        # ocr = hub.Module(name="chinese_ocr_db_crnn_server")

        # 读取照片路径
        np_images = [cv2.imread(img)]
        # 清空文件夹
        if not os.path.exists('./ocr_result'):
            os.mkdir('./ocr_result')
        else:
            shutil.rmtree('./ocr_result')
            os.mkdir('./ocr_result')

        results = model.recognize_text(
            images=np_images,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
            output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
            visualization=True,  # 是否将识别结果保存为图片文件；
            box_thresh=0.5,  # 检测文本框置信度的阈值；
            text_thresh=0.5)  # 识别中文文本置信度的阈值；

        records_list = []
        #字典用"{ }"标识。字典由索引(key)和它对应的值value组成。
        image_info = {}
        id_info = {}
        count = 0
        sum = 0
        key = '其它'

        for result in results:
            record = {}
            data = result['data']
            save_path = result['save_path']
            for infomation in data:
                # image_info.append(infomation['text'])
                records_list.append(infomation['text'])
                if "身份号码" in infomation['text']:
                    key = '身份证信息'
                if "发票" in infomation['text']:
                    key = '发票信息'
                if "车" in infomation['text']:
                    key = '车票信息'
                if "营业执照" in infomation['text']:
                    key = '营业执照信息'
                count += 1
                conf = infomation['confidence']
                sum = sum + conf

        conf_all = sum / count
        result1 = ''.join(records_list)
        image_info[key] = [np.round(float(conf_all), 3), result1]
        print(image_info)
        for filename in os.listdir('./ocr_result'):
            im = cv2.imread('./ocr_result' + "/" + filename)



        return im, image_info

    # *******************发票采用位置的方法分割*******************
    # def fapiao__model(img):
    #     crop_range_list_data = [[1700, 20, 600, 250], [420, 280, 935, 220], [420, 1030, 935, 230],
    #                             [1500, 880, 390, 75], [2000, 880, 330, 75], [750, 960, 600, 65], [1870, 960, 300, 70],
    #                             [1455, 1045, 400, 180], [760, 50, 900, 110], [280, 200, 250, 75]]
    #     warped = imagePreProcessing(img)
    #     data = []
    #     data1 = []
    #     receipt ={}
    #     image_info = {}
    #     receipt_info = {}
    #     key = '发票信息'
    #
    #     for i in range(len(crop_range_list_data)):
    #         crop = cropImage_test(warped, crop_range_list_data[i])
    #         cv2.imwrite('output' + '\\' + str(i) + '.jpg', crop)
    #         crop_text, conf_all = get_receipt_info('./output/' + str(i) + '.jpg')
    #         crop_text = crop_text.replace('o', '0').replace(' ', '').replace('l', '1').replace('O', '0').split(':')[-1]
    #         data.append(crop_text)
    #         data1.append(crop_text)
    #         test = data[i]
    #         if i == 1:
    #             data[i] = "购买方名称：{0[0]},纳税人识别号：{0[1]}".format(test)
    #         elif i == 2:
    #             data[i] = "销售方名称{0[0]},纳税人识别号{0[1]},地址、电话{0[2]},开户行及账号{0[3]}".format(test)
    #         elif i == 3:
    #             data[i] = "金额{0[0]}".format(test)
    #         elif i == 4:
    #             data[i] = "税额{0[0]}".format(test)
    #         elif i == 5:
    #             data[i] = "价税合计大写{0[0]}".format(test)
    #         elif i == 6:
    #             data[i] = "价税合计小写{0[0]}".format(test)
    #         elif i == 7:
    #             data[i] = "备注无".format(test)
    #         elif i == 8:
    #             data[i] = "发票类型：{0[0]}".format(test)
    #         elif i == 9:
    #             data[i] = "机器编号：{0[0]}".format(test)
    #
    #     image_info[key] = [np.round(float(conf_all), 3), data]
    #     # print(image_info)
    #     # receipt_info['0']= ['1','2','3','4','5','6','7','8','9']
    #     receipt_info['发票'] = [data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[9]]
    #     for i in range(len(crop_range_list_data)):
    #         warped = cv2.rectangle(warped, (crop_range_list_data[i][0], crop_range_list_data[i][1]),
    #                                (crop_range_list_data[i][0] + crop_range_list_data[i][2],
    #                                 crop_range_list_data[i][1] + crop_range_list_data[i][3]),
    #                                (0, 0, 255), 2)
    #     cv2.imwrite('show_pic/result.jpg', warped)
    #     for filename in os.listdir('./show_pic'):
    #         im = cv2.imread('./show_pic' + "/" + filename)
    #
    #     return im, image_info, receipt_info

    def fapiao__model(img):
        crop_range_list_data = [[1700, 20, 600, 250], [420, 280, 935, 220], [420, 1030, 935, 230],
                                [1500, 880, 390, 75], [2000, 880, 330, 75], [750, 960, 600, 65], [1870, 960, 300, 70],
                                [1455, 1045, 400, 180], [760, 50, 900, 110], [280, 200, 250, 75]]
        # 销售方字典
        purchaser_dict = ['purchaserName', 'purchaserCode', 'purchaserAddrTel', 'purchaserBankCode']
        seller_dict = ['sellerName', 'sellerCode', 'sellerAddrTel', 'sellerBankCode']
        invoice_dict = ['invoiceCode', 'invoiceNumber', 'invoiceDate', 'checkCode']

        # 截取图片中部分区域图像-字段
        crop_range_list_name = ['invoice', 'purchaser', 'seller',
                                'totalExpense', 'totalTax', 'totalTaxExpenseZh', 'totalTaxExpense',
                                'remark', 'title', 'machineCode']
        warped = imagePreProcessing(img)
        data = []
        data1 = []
        receipt = {}
        image_info = {}
        receipt_info = {}
        key1 = '发票信息'
        a = 0

        for i in range(len(crop_range_list_data)):
            crop = cropImage_test(warped, crop_range_list_data[i])
            cv2.imwrite('output' + '\\' + str(i) + '.jpg', crop)
            crop_text, scores = get_receipt_info('./output/' + str(i) + '.jpg')
            crop_text = crop_text.replace('o', '0').replace(' ', '').replace('l', '1').replace('O', '0').split(':')[-1]

            # 计算置信度
            a = a + sum(scores)

            # crop_text = crop_text.replace('o', '0').replace(' ', '').replace('l', '1').replace('O', '0').split(':')[-1]

            if crop_range_list_name[i] == 'seller':
                crop_text = crop_text.split(',')
                for i in range(4):
                    if i < len(crop_text):
                        receipt.update({seller_dict[i]: crop_text[i]})

                    else:
                        receipt.update({seller_dict[i]: ''})

            elif crop_range_list_name[i] == 'invoice':
                crop_text = crop_text.split(',')
                for i in range(4):
                    if i < len(crop_text):
                        receipt.update({invoice_dict[i]: crop_text[i]})

                    else:
                        receipt.update({invoice_dict[i]: ''})

            elif crop_range_list_name[i] == 'purchaser':
                crop_text = crop_text.split(',')
                for i in range(4):
                    if i < len(crop_text):
                        receipt.update({purchaser_dict[i]: crop_text[i]})

                    else:
                        receipt.update({purchaser_dict[i]: ''})

            else:
                if crop_range_list_name[i] == 'title':
                    crop_text = crop_text[0:2] + '增值税普通发票'
                receipt.update({crop_range_list_name[i]: crop_text})


        # 三行表格部分
        receipt['sellerCode'] = receipt['sellerCode'].replace('工', '1').replace('.', '')
        receipt['purchaserCode'] = receipt['purchaserCode'].replace('工', '1').replace('.', '')
        for key in receipt:
            print(key + ':' + receipt[key])
        receipt.update({"serviceDetails": []})

        # 计算置信度
        conf_all = a / 15

        # 筛选部分的输出
        receipt_info[receipt['title']] = [receipt['checkCode'], receipt['invoiceCode'], receipt['invoiceDate'], receipt['invoiceNumber'],
                                          receipt['purchaserName'], receipt['purchaserCode'],receipt['purchaserAddrTel'], receipt['purchaserBankCode'],
                                          receipt['sellerName'], receipt['sellerCode'], receipt['sellerAddrTel'], receipt['sellerBankCode'],
                                          receipt['totalTaxExpenseZh'],receipt['totalTaxExpense'], receipt['totalExpense'], receipt['totalTax'],
                                          receipt['remark'], receipt['machineCode'] ]
        image_info[key1] = [np.round(float(conf_all), 3), receipt]
        print("识别成功")

        # 显示图片
        for i in range(len(crop_range_list_data)):
            warped = cv2.rectangle(warped, (crop_range_list_data[i][0], crop_range_list_data[i][1]),
                                   (crop_range_list_data[i][0] + crop_range_list_data[i][2],
                                    crop_range_list_data[i][1] + crop_range_list_data[i][3]),
                                   (0, 0, 255), 2)
        cv2.imwrite('show_pic/result.jpg', warped)
        # for filename in os.listdir('./show_pic'):
        #     im = cv2.imread('./show_pic' + "/" + filename)
        im = cv2.imread('./show_pic/result.jpg')


        return im, image_info, receipt_info

    def ticket__model(img):
        crop_range_list_data = [[50, 50, 130,60],[320,50,130,60],[180,50,140,60],
                                [30,120,280,50],[310,120,190,50],
                                [30,230,300,60]]
        # 字典
        passenger_dict = ['name', 'id']

        # 截取图片中部分区域图像-字段
        crop_range_list_name = ['startStation', 'endStation', 'trainID',
                                'startTime', 'seatLocation',
                                'passengerName&ID']

        warped = imagePreProcessing1(img)
        ticket = {}
        image_info = {}
        ticket_info = {}
        key = '车票信息'
        a = 0
        for i in range(len(crop_range_list_data)):
            crop = cropImage_test(warped, crop_range_list_data[i])
            cv2.imwrite('output' + '\\' + str(i) + '.jpg', crop)
            crop_text, scores = get_ticket_info('./output/' + str(i) + '.jpg')

            # 计算置信度
            a = a + sum(scores)

            crop_text = crop_text.replace(',', '').replace(' ', '').replace('l', '1').replace('O', '0').split(':')[-1]

            if crop_range_list_name[i] == 'startStation':
                ticket.update({crop_range_list_name[i]: crop_text})

            elif crop_range_list_name[i] == 'endStation':
                ticket.update({crop_range_list_name[i]: crop_text})

            elif crop_range_list_name[i] == 'trainID':
                ticket.update({crop_range_list_name[i]: crop_text})

            elif crop_range_list_name[i] == 'startTime':
                ticket.update({crop_range_list_name[i]: crop_text})

            elif crop_range_list_name[i] == 'seatLocation':
                ticket.update({crop_range_list_name[i]: crop_text})

            elif crop_range_list_name[i] == 'passengerName&ID':
                crop_text = crop_text.split(',')
                for i in range(2):
                    if i < len(crop_text):
                        ticket.update({passenger_dict[i]: crop_text[i]})

                    else:
                        ticket.update({passenger_dict[i]: ''})


        conf_all = a / 7

        image_info[key] = [np.round(float(conf_all), 3), ticket]
        ticket_info[ticket['startStation']] = [ticket['endStation'], ticket['trainID'],
                                               ticket['startTime'], ticket['seatLocation'],
                                               ticket['name'], ticket['id']]

        for i in range(len(crop_range_list_data)):
            warped = cv2.rectangle(warped, (crop_range_list_data[i][0], crop_range_list_data[i][1]),
                                   (crop_range_list_data[i][0] + crop_range_list_data[i][2],
                                    crop_range_list_data[i][1] + crop_range_list_data[i][3]),
                                   (0, 0, 255), 2)
        cv2.imwrite('show_pic/result.jpg', warped)
        for filename in os.listdir('./show_pic'):
            im = cv2.imread('./show_pic' + "/" + filename)

        return im, image_info, ticket_info


    # 由于营业执照的信息过于密切，导致识别精度差，此处可以考虑自己训练数据集。
    # 营业执照采用身份证的切割方式会导致识别不成功，所以采取对识别文本进行关键词区分，但该办法存在很大误差，需要进一步完善。
    def business__model(img):
        crop_range_list_data = [[180,950,3100,1000]]

        # 字典
        crop_range_list_name = ['information']

        warped = imagePreProcessing2(img)
        data = []
        image_info = {}
        business_info = {}
        key = '营业执照'
        a = 0
        count = 0
        for i in range(len(crop_range_list_data)):
            crop = cropImage_test(warped, crop_range_list_data[i])
            cv2.imwrite('output' + '\\' + str(i) + '.jpg', crop)
            crop_text, scores = get_business_info('./output/' + str(i) + '.jpg')

            crop_text = crop_text.replace(',', '').replace(',', '').replace('l', '1').replace('O', '0').split(':')[-1]
            print(crop_text)
            if '名称' in crop_text:
                name = crop_text.split('名称')
            elif '名' in crop_text:
                name = crop_text.split('名')
            elif '称' in crop_text:
                name = crop_text.split('称')

            if '米型' in crop_text:
                name1 = name[1].split('米型')
            elif '类型' in crop_text:
                name1 = name[1].split('类型')
            elif '型' in crop_text:
                name1 = name[1].split('型')
            elif '类' in crop_text:
                name1 = name[1].split('类')

            type = name1[1].split('住所')
            if '法表定代人' in crop_text:
                address = type[1].split('法表定代人')
            elif '法定代表人' in crop_text:
                address = type[1].split('法定代表人')

            if '注资册本' in crop_text:
                register = address[1].split('注资册本')
            elif '注本册资' in crop_text:
                register = address[1].split('注本册资')
            elif '注册资本' in crop_text:
                register = address[1].split('注册资本')
            elif '注资本' in crop_text:
                register = address[1].split('注资本')
            elif '注册资' in crop_text:
                register = address[1].split('注册资')
            elif '注资本册' in crop_text:
                register = address[1].split('注资本册')
            elif '资本册' in crop_text:
                register = address[1].split('资本册')
            elif '册本资注' in crop_text:
                register = address[1].split('册本资注')

            if '成立日期' in crop_text:
                fund = register[1].split('成立日期')
            elif '立成日期' in crop_text:
                fund = register[1].split('立成日期')
            elif '成立' in crop_text:
                fund = register[1].split('成立')
            elif '立日成期' in crop_text:
                fund = register[1].split('立日成期')

            if '营期限' in crop_text:
                date = fund[1].split('营期限')
            elif '营业期限' in crop_text:
                date = fund[1].split('营业期限')

            if '经营范围' in crop_text:
                time = date[1].split('经营范围')
            elif '营范经围' in crop_text:
                time = date[1].split('营范经围')
            elif '营范围经' in crop_text:
                time = date[1].split('营范围经')
            elif '经营范' in crop_text:
                time = date[1].split('经营范')

            including = time[1]

            data = {
                'name': name1[0],
                'type': type[0],
                'address': address[0],
                'register': register[0],
                'fund': fund[0],
                'date': date[0],
                'time': time[0],
                'including': including
            }

            print("识别成功")


        image_info[key] = [np.round(float(scores), 3), data]

        business_info[data['name']] = [data['type'], data['address'], data['register'],
                                       data['fund'], data['date'], data['time'], data['including'] ]


        for i in range(len(crop_range_list_data)):
            warped = cv2.rectangle(warped, (crop_range_list_data[i][0], crop_range_list_data[i][1]),
                                   (crop_range_list_data[i][0] + crop_range_list_data[i][2],
                                    crop_range_list_data[i][1] + crop_range_list_data[i][3]),
                                   (0, 0, 255), 2)
        cv2.imwrite('show_pic/result.jpg', warped)
        for filename in os.listdir('./show_pic'):
            im = cv2.imread('./show_pic' + "/" + filename)

        return im, image_info, business_info















